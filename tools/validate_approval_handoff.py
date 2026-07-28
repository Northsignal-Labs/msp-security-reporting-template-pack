#!/usr/bin/env python3
"""Validate Northsignal Labs approval handoff fields before URL cutover.

Filesystem-only guardrail. This helper reads APPROVAL-HANDOFF-FIELDS.json and
checks whether a future public-URL cutover is blocked or sufficiently approved.
It does not publish, upload, create accounts, contact services, spend money,
replace sitemap/robots hosts, enable analytics, or create a payment workflow.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
FIELDS_PATH = ROOT / "APPROVAL-HANDOFF-FIELDS.json"
SITEMAP_PATH = ROOT / "sitemap.xml"
ROBOTS_PATH = ROOT / "robots.txt"
PLACEHOLDER_HOST = "northsignal-labs.local"
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
FORBIDDEN_TEXT_PATTERNS = [
    r"\b" + "R" + "P" + r"\b",
    r"fake founder",
    r"customer testimonial",
]


def load_fields() -> dict:
    if not FIELDS_PATH.exists():
        raise FileNotFoundError(f"missing {FIELDS_PATH.relative_to(ROOT)}")
    return json.loads(FIELDS_PATH.read_text(encoding="utf-8"))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def validate_public_url(value: str, schemes: list[str], blocked_hosts: list[str]) -> list[str]:
    errors: list[str] = []
    parsed = urlparse(value)
    if parsed.scheme not in schemes:
        errors.append("public_base_url must use an approved scheme: " + ", ".join(schemes))
    if not parsed.netloc:
        errors.append("public_base_url must include a host")
    host = parsed.hostname or ""
    if host in blocked_hosts:
        errors.append(f"public_base_url must not use blocked/placeholder host: {host}")
    if parsed.query or parsed.fragment:
        errors.append("public_base_url must not include query strings or fragments")
    if value and not value.endswith("/"):
        errors.append("public_base_url must end with '/' so sitemap/robots replacement is deterministic")
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = load_fields()
    except Exception as exc:  # noqa: BLE001 - CLI should print clear gate failures.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    approved_for_cutover = data.get("approved_for_cutover") is True
    required = data.get("required_fields") or {}
    schemes = data.get("allowed_public_base_url_schemes") or ["https"]
    blocked_hosts = data.get("blocked_public_base_url_hosts") or [PLACEHOLDER_HOST]

    if not isinstance(required, dict):
        errors.append("required_fields must be an object")
        required = {}

    for field in TEXT_FIELDS:
        value = required.get(field)
        if approved_for_cutover and not (isinstance(value, str) and value.strip()):
            errors.append(f"missing required approval text field for cutover: {field}")
        if isinstance(value, str):
            for pattern in FORBIDDEN_TEXT_PATTERNS:
                if re.search(pattern, value, flags=re.IGNORECASE):
                    errors.append(f"forbidden wording /{pattern}/ found in approval field: {field}")

    public_base_url = required.get("public_base_url")
    if approved_for_cutover or public_base_url:
        if not isinstance(public_base_url, str):
            errors.append("public_base_url must be a string")
        else:
            errors.extend(validate_public_url(public_base_url.strip(), list(schemes), list(blocked_hosts)))

    for field in BOOLEAN_CONFIRMATIONS:
        value = required.get(field)
        if approved_for_cutover and value is not True:
            errors.append(f"required confirmation must be true for cutover: {field}")
        elif value not in (True, False):
            warnings.append(f"confirmation field should be boolean: {field}")

    sitemap = text(SITEMAP_PATH)
    robots = text(ROBOTS_PATH)
    placeholder_present = PLACEHOLDER_HOST in sitemap and PLACEHOLDER_HOST in robots
    if approved_for_cutover:
        if placeholder_present:
            warnings.append("approval fields appear complete, but sitemap.xml/robots.txt still contain the placeholder host until cutover is performed")
    else:
        if not placeholder_present:
            errors.append("approved_for_cutover is false, but sitemap.xml and robots.txt do not both contain the placeholder host")

    print("Northsignal Labs approval handoff validation")
    print(f"root: {ROOT}")
    print(f"approved_for_cutover: {approved_for_cutover}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    print("cutover_state: " + ("ready_for_reviewer_cutover" if approved_for_cutover and not errors else "hold_public_release"))
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
