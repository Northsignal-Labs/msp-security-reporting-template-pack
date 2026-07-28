#!/usr/bin/env python3
"""Apply an approved Northsignal Labs public URL cutover.

Filesystem-only helper. It reads APPROVAL-HANDOFF-FIELDS.json, requires the
existing approval validator to report a ready cutover state, and then replaces
the placeholder base URL in public discovery/reference files: sitemap.xml,
robots.txt, and JSON Schema $id values. It does not publish, upload, create
accounts, contact services, spend money, add analytics, collect personal data,
or create payment/KYC/quote/invoice workflows.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
FIELDS_PATH = ROOT / "APPROVAL-HANDOFF-FIELDS.json"
VALIDATOR_PATH = ROOT / "tools" / "validate_approval_handoff.py"
PLACEHOLDER_BASE_URL = "https://northsignal-labs.local/"
CUTOVER_LOG_PATH = ROOT / "PUBLIC-URL-CUTOVER-LOG.json"
TARGET_PATHS = [
    ROOT / "sitemap.xml",
    ROOT / "robots.txt",
    ROOT / "schemas" / "msp-monthly-security-report.schema.json",
    ROOT / "schemas" / "nis2-readiness-summary.schema.json",
    ROOT / "schemas" / "m365-secure-score-report.schema.json",
    ROOT / "schemas" / "cyber-insurance-gap-register.schema.json",
    ROOT / "schemas" / "vciso-qbr-summary.schema.json",
]


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"missing required file: {path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def approved_public_base_url(fields: dict) -> str:
    required = fields.get("required_fields") or {}
    value = required.get("public_base_url")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("required_fields.public_base_url is blank")
    value = value.strip()
    if not value.endswith("/"):
        raise ValueError("public_base_url must end with '/'")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("public_base_url must be an HTTPS URL with a host")
    if parsed.hostname in {"northsignal-labs.local", "localhost", "127.0.0.1"}:
        raise ValueError(f"public_base_url uses a blocked/placeholder host: {parsed.hostname}")
    if parsed.query or parsed.fragment:
        raise ValueError("public_base_url must not include query strings or fragments")
    return value


def run_validator() -> tuple[int, str]:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    combined = "\n".join(part.strip() for part in [completed.stdout, completed.stderr] if part.strip())
    return completed.returncode, combined


def replace_placeholder(path: Path, public_base_url: str, *, apply: bool) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"missing required release file: {path.relative_to(ROOT)}")
    before = path.read_text(encoding="utf-8")
    replacement_count = before.count(PLACEHOLDER_BASE_URL)
    if replacement_count == 0:
        if "northsignal-labs.local" in before:
            raise ValueError(f"{path.relative_to(ROOT)} contains northsignal-labs.local but not the exact base URL placeholder")
        if public_base_url not in before:
            raise ValueError(f"{path.relative_to(ROOT)} contains neither the placeholder nor approved public_base_url")
        after = before
    else:
        after = before.replace(PLACEHOLDER_BASE_URL, public_base_url)
        if apply:
            path.write_text(after, encoding="utf-8")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "placeholder_replacements": replacement_count,
        "changed": before != after,
        "approved_public_base_url_present_after": public_base_url in after,
        "placeholder_host_present_after": "northsignal-labs.local" in after,
    }


def write_log(public_base_url: str, results: list[dict], *, apply: bool, validator_output: str) -> None:
    fields = load_json(FIELDS_PATH)
    required = fields.get("required_fields") or {}
    log = {
        "project": "Northsignal Labs MSP Security Reporting Template Pack",
        "generated_at": iso_now(),
        "operation": "public_url_cutover_apply" if apply else "public_url_cutover_dry_run",
        "publication_status": "local_only_not_published",
        "approved_channel": required.get("approved_channel", ""),
        "public_base_url": public_base_url,
        "final_reviewer": required.get("final_reviewer", ""),
        "files_checked": results,
        "validator_tail": validator_output.splitlines()[-12:],
        "guardrails": [
            "Local public URL reference replacement only: sitemap.xml, robots.txt, and JSON Schema $id values",
            "No upload, account creation, public posting, paid service, analytics, forms, contact workflow, payment/KYC, quote/invoice workflow, or spend",
            "Run release telemetry, staging, staged-review, ZIP packaging, and human metadata review after any applied cutover before public upload",
        ],
    }
    if apply:
        CUTOVER_LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run or apply the approved public URL cutover after approval validation passes."
    )
    parser.add_argument("--apply", action="store_true", help="Actually rewrite public URL references. Without this, only dry-run.")
    args = parser.parse_args(argv)

    try:
        fields = load_json(FIELDS_PATH)
        public_base_url = approved_public_base_url(fields)
    except Exception as exc:  # noqa: BLE001 - CLI gate should be explicit.
        print(f"ERROR: approval fields are not ready for cutover: {exc}", file=sys.stderr)
        return 1

    validator_code, validator_output = run_validator()
    if validator_code != 0 or "cutover_state: ready_for_reviewer_cutover" not in validator_output:
        print("ERROR: approval handoff validator did not report ready_for_reviewer_cutover", file=sys.stderr)
        if validator_output:
            print(validator_output)
        return 1

    try:
        results = [replace_placeholder(path, public_base_url, apply=args.apply) for path in TARGET_PATHS]
        if args.apply:
            # Re-read after writing and fail closed if any placeholder host remains.
            for path in TARGET_PATHS:
                text = path.read_text(encoding="utf-8")
                if "northsignal-labs.local" in text:
                    raise ValueError(f"placeholder host remains after apply: {path.relative_to(ROOT)}")
                if public_base_url not in text:
                    raise ValueError(f"approved public_base_url missing after apply: {path.relative_to(ROOT)}")
        write_log(public_base_url, results, apply=args.apply, validator_output=validator_output)
    except Exception as exc:  # noqa: BLE001 - CLI should print clear failures.
        print(f"ERROR: cutover failed: {exc}", file=sys.stderr)
        return 1

    print("Northsignal Labs public URL cutover")
    print(f"mode: {'apply' if args.apply else 'dry_run'}")
    print(f"public_base_url: {public_base_url}")
    print("publication_status: local_only_not_published")
    for result in results:
        print(
            f"{result['path']}: replacements={result['placeholder_replacements']} "
            f"changed={result['changed']} placeholder_remaining={result['placeholder_host_present_after']}"
        )
    if args.apply:
        print(f"wrote {CUTOVER_LOG_PATH.relative_to(ROOT)}")
        print("next: run telemetry/staging/review/package gates before any approved upload")
    else:
        print("dry run only; pass --apply after reviewer approval validation to rewrite local files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
