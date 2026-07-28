#!/usr/bin/env python3
"""Validate that PUBLIC-LAUNCH-APPROVAL-PACKET.md matches GO-LIVE-PACKAGE.json.

Filesystem-only guardrail for Northsignal Labs. The public launch approval packet
is the one-screen artifact a reviewer can use to supply the missing public URL
and account fields. If its ZIP file count, byte size, or SHA-256 drift from the
latest verified GO-LIVE-PACKAGE.json, approval could be granted against a stale
artifact. This helper fails closed before any approved upload handoff.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_JSON = ROOT / "GO-LIVE-PACKAGE.json"
PACKET_MD = ROOT / "PUBLIC-LAUNCH-APPROVAL-PACKET.md"
ZIP_NAME = "northsignal-labs-msp-security-reporting-template-pack-v0.1.zip"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def contains(pattern: str, text: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    package = load_json(PACKAGE_JSON)
    packet_text = PACKET_MD.read_text(encoding="utf-8") if PACKET_MD.exists() else ""

    if not package:
        errors.append(f"missing or unreadable package manifest: {PACKAGE_JSON.relative_to(ROOT)}")
    if not packet_text:
        errors.append(f"missing or empty approval packet: {PACKET_MD.relative_to(ROOT)}")

    file_count = package.get("file_count")
    byte_size = package.get("bytes")
    sha256 = package.get("sha256")
    zip_verified = package.get("zip_verified_against_staged_manifest")
    zip_errors = package.get("zip_verification_errors") or []

    if zip_verified is not True:
        errors.append("GO-LIVE-PACKAGE.json does not report zip_verified_against_staged_manifest=true")
    if zip_errors:
        errors.append(f"GO-LIVE-PACKAGE.json has ZIP verification errors: {zip_errors}")
    if not isinstance(file_count, int) or file_count <= 0:
        errors.append("GO-LIVE-PACKAGE.json file_count is missing or invalid")
    if not isinstance(byte_size, int) or byte_size <= 0:
        errors.append("GO-LIVE-PACKAGE.json bytes is missing or invalid")
    if not isinstance(sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", sha256):
        errors.append("GO-LIVE-PACKAGE.json sha256 is missing or invalid")

    if packet_text and isinstance(file_count, int):
        if not contains(rf"Current file count:\s*{file_count}\s+manifest-approved files", packet_text):
            errors.append(f"approval packet does not show current file count {file_count}")
    if packet_text and isinstance(byte_size, int):
        if not contains(rf"Current byte size:\s*{byte_size}\b", packet_text):
            errors.append(f"approval packet does not show current byte size {byte_size}")
    if packet_text and isinstance(sha256, str):
        if sha256 not in packet_text:
            errors.append("approval packet does not show the current GO-LIVE-PACKAGE.json SHA-256")
    if packet_text and ZIP_NAME not in packet_text:
        errors.append(f"approval packet does not name expected ZIP {ZIP_NAME}")
    if packet_text and "review anchor, not authorization to upload" not in packet_text:
        warnings.append("approval packet is missing explicit review-anchor/not-upload-authorization wording")
    if packet_text and "no account, upload, post, analytics, payment workflow, contact collection, or spend" not in packet_text:
        warnings.append("approval packet status line may be missing no-account/no-upload/no-spend guardrail wording")

    print("Northsignal Labs public launch packet sync validation")
    print(f"package manifest: {PACKAGE_JSON.relative_to(ROOT)}")
    print(f"approval packet: {PACKET_MD.relative_to(ROOT)}")
    print(f"package file count: {file_count}")
    print(f"package bytes: {byte_size}")
    print(f"package sha256: {sha256}")
    print(f"zip verified: {zip_verified}")
    print(f"errors: {len(errors)}")
    for item in errors:
        print(f"ERROR: {item}")
    print(f"warnings: {len(warnings)}")
    for item in warnings:
        print(f"WARNING: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
