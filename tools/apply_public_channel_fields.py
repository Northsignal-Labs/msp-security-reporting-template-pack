#!/usr/bin/env python3
"""Apply reviewer-supplied public channel fields to APPROVAL-HANDOFF-FIELDS.json.

Filesystem-only approval friction reducer. It reads a JSON object shaped like
PUBLIC-CHANNEL-FIELDS-TEMPLATE.json after the reviewer has replaced placeholders
with concrete no-spend public channel metadata. By default it dry-runs and prints
what would be copied. With --apply it updates only APPROVAL-HANDOFF-FIELDS.json
so the existing validator/cutover gates can run next.

It does not infer a URL, publish, upload, authenticate, create accounts, contact
services, add analytics/forms, collect data, start payment/KYC/quote/invoice
workflows, or spend money.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
TEXT_FIELDS = [
    "approved_channel",
    "public_base_url",
    "account_repository_display_name",
    "account_repository_metadata_constraints",
    "final_reviewer",
]
BOOLEAN_CONFIRMATIONS = [
    "spend_confirmation",
    "financial_workflow_confirmation",
    "data_collection_confirmation",
    "claims_identity_approval",
]
PLACEHOLDER_PATTERNS = [
    r"REPLACE-WITH",
    r"YYYY-MM-DD",
    r"selected reviewer identifier",
    r"template_only",
    r"example\.com",
    r"northsignal-labs\.local",
    r"localhost",
    r"127\.0\.0\.1",
]
FORBIDDEN_PUBLIC_FIELD_PATTERNS = [
    r"\b" + "R" + "P" + r"\b",
    r"private contact",
    r"personal account",
    r"fake founder",
    r"customer testimonial",
    r"payment",
    r"payout",
    r"tax/KYC",
    r"quote",
    r"invoice",
    r"analytics",
    r"contact form",
    r"newsletter",
]


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - CLI should produce clear gate failure.
        raise ValueError(f"could not read JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def normalized_required_fields(data: dict) -> dict:
    required = data.get("required_fields")
    if not isinstance(required, dict):
        raise ValueError("source JSON must contain required_fields object")
    return required


def validate_source(data: dict) -> list[str]:
    errors: list[str] = []
    required = data.get("required_fields") if isinstance(data.get("required_fields"), dict) else {}

    if data.get("approved_for_cutover") is not True:
        errors.append("source approved_for_cutover must be true; template/hold-state files cannot be applied")

    for field in TEXT_FIELDS:
        value = required.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing required text field: {field}")
            continue
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, value, flags=re.IGNORECASE):
                errors.append(f"placeholder value detected in {field}: /{pattern}/")
        for pattern in FORBIDDEN_PUBLIC_FIELD_PATTERNS:
            if field != "account_repository_metadata_constraints" and re.search(pattern, value, flags=re.IGNORECASE):
                errors.append(f"unsafe public field wording detected in {field}: /{pattern}/")

    public_base_url = required.get("public_base_url")
    if isinstance(public_base_url, str):
        parsed = urlparse(public_base_url.strip())
        if parsed.scheme != "https":
            errors.append("public_base_url must use https")
        if not parsed.netloc:
            errors.append("public_base_url must include a host")
        if parsed.query or parsed.fragment:
            errors.append("public_base_url must not include query strings or fragments")
        if not public_base_url.strip().endswith("/"):
            errors.append("public_base_url must end with '/'")
        host = parsed.hostname or ""
        if host in {"northsignal-labs.local", "localhost", "127.0.0.1"}:
            errors.append(f"public_base_url uses blocked placeholder host: {host}")

    for field in BOOLEAN_CONFIRMATIONS:
        if required.get(field) is not True:
            errors.append(f"required confirmation must be true: {field}")

    constraints = str(required.get("account_repository_metadata_constraints", ""))
    # Accept equivalent long-form constraints from the existing template even if capitalization differs.
    constraints_lower = constraints.lower()
    if "personal" not in constraints_lower or "identity" not in constraints_lower:
        errors.append("account_repository_metadata_constraints must explicitly block personal identity exposure")
    if "paid" not in constraints_lower and "spend" not in constraints_lower:
        errors.append("account_repository_metadata_constraints must explicitly preserve no-spend/no-paid constraints")
    if "analytics" not in constraints_lower and "data" not in constraints_lower:
        errors.append("account_repository_metadata_constraints must explicitly block analytics/data-collection drift")
    if "payment" not in constraints_lower and "financial" not in constraints_lower:
        errors.append("account_repository_metadata_constraints must explicitly block payment/financial workflow drift")

    return errors


def build_updated_handoff(current: dict, source: dict) -> dict:
    updated = deepcopy(current)
    required = normalized_required_fields(source)
    updated["status"] = "public_channel_fields_supplied_pending_url_cutover"
    updated["approved_for_cutover"] = True
    updated["last_reviewed_at"] = source.get("last_reviewed_at") or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    updated_required = deepcopy(updated.get("required_fields") or {})
    for field in TEXT_FIELDS + BOOLEAN_CONFIRMATIONS:
        updated_required[field] = required[field]
    updated["required_fields"] = updated_required
    updated["current_hold_reason"] = "Concrete reviewer-supplied public channel fields have been applied locally. Run tools/validate_approval_handoff.py, then tools/perform_public_url_cutover.py as a dry run before any --apply cutover. This file still does not authorize account creation, upload, public posting, analytics/forms, payment/KYC/quote/invoice/sales workflows, or spend."
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply approved public channel fields to approval handoff JSON")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="autonomous-lab root directory")
    parser.add_argument("--source", default="PUBLIC-CHANNEL-FIELDS-TEMPLATE.json", help="source JSON path, relative to root unless absolute")
    parser.add_argument("--apply", action="store_true", help="write APPROVAL-HANDOFF-FIELDS.json; default is dry-run only")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    source_path = Path(args.source)
    if not source_path.is_absolute():
        source_path = root / source_path
    handoff_path = root / "APPROVAL-HANDOFF-FIELDS.json"

    errors: list[str] = []
    try:
        source = load_json(source_path)
        current = load_json(handoff_path)
        errors.extend(validate_source(source))
    except Exception as exc:  # noqa: BLE001
        errors.append(str(exc))
        source = {}
        current = {}

    print("Northsignal Labs public channel fields apply")
    print(f"source: {source_path}")
    print(f"target: {handoff_path}")
    print(f"mode: {'apply' if args.apply else 'dry_run'}")
    print(f"errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print("state: blocked")
        return 1

    updated = build_updated_handoff(current, source)
    if args.apply:
        handoff_path.write_text(json.dumps(updated, indent=2) + "\n", encoding="utf-8")
        print("state: applied_to_approval_handoff_fields")
        print("next: run tools/validate_approval_handoff.py, then dry-run tools/perform_public_url_cutover.py")
    else:
        print("state: dry_run_ready")
        print("next: rerun with --apply only if the source fields were supplied/approved by the reviewer")
    required = updated.get("required_fields", {})
    print(f"public_base_url: {required.get('public_base_url', '')}")
    print("guardrail: filesystem-only; no URL inference, upload, account creation, public posting, analytics/forms, payment/KYC/quote/invoice/sales workflow, or spend")
    return 0


if __name__ == "__main__":
    sys.exit(main())
