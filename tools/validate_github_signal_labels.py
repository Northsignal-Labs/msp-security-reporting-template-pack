#!/usr/bin/env python3
"""Validate GitHub labels needed for aggregate demand signal measurement.

This checker is filesystem-only. It reads the future GitHub issue templates and
.github/labels.yml, then verifies that every issue-template label needed by the
post-launch aggregate snapshot helper is defined before an approved public
release. It does not call GitHub, create labels, publish, upload, authenticate,
collect data, create accounts, start payment/KYC workflows, or spend money.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABELS_PATH = ROOT / ".github" / "labels.yml"
ISSUE_TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
REQUIRED_SIGNAL_LABELS = {"template-request", "commercial-fit", "demand-signal"}
REQUIRED_ASSET_SIGNAL_LABELS = {
    "asset:msp-monthly-report",
    "asset:nis2-readiness",
    "asset:m365-secure-score",
    "asset:cyber-insurance-evidence",
    "asset:vciso-qbr",
}


def extract_issue_template_labels(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    labels: set[str] = set()
    for match in re.finditer(r"^labels:\s*\[([^\]]*)\]\s*$", text, flags=re.MULTILINE):
        labels.update(part.strip().strip('"\'') for part in match.group(1).split(",") if part.strip())
    for match in re.finditer(r"^labels:\s*([^\n#]+)\s*$", text, flags=re.MULTILINE):
        raw = match.group(1).strip()
        if raw.startswith("["):
            continue
        labels.update(part.strip().strip('"\'') for part in raw.split(",") if part.strip())
    return labels


def extract_declared_labels(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"^\s*-\s*name:\s*['\"]?([^'\"\n]+?)['\"]?\s*$", text, flags=re.MULTILINE))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not LABELS_PATH.exists():
        errors.append("missing .github/labels.yml")
        declared_labels: set[str] = set()
    else:
        declared_labels = extract_declared_labels(LABELS_PATH)

    template_paths = sorted(ISSUE_TEMPLATE_DIR.glob("*.yml"))
    if not template_paths:
        errors.append("missing GitHub issue templates")

    template_labels: set[str] = set()
    for path in template_paths:
        if path.name == "config.yml":
            continue
        labels = extract_issue_template_labels(path)
        if not labels:
            warnings.append(f"no labels declared in {path.relative_to(ROOT)}")
        template_labels.update(labels)

    missing_required = sorted((REQUIRED_SIGNAL_LABELS | REQUIRED_ASSET_SIGNAL_LABELS) - declared_labels)
    missing_template_labels = sorted(template_labels - declared_labels)
    allowed_measurement_only = {"demand-signal"} | REQUIRED_ASSET_SIGNAL_LABELS
    unused_declared = sorted((declared_labels - template_labels) - allowed_measurement_only)

    for label in missing_required:
        errors.append(f"required signal label not declared in .github/labels.yml: {label}")
    for label in missing_template_labels:
        errors.append(f"issue-template label missing from .github/labels.yml: {label}")
    for label in unused_declared:
        warnings.append(f"declared label is not used by current signal issue templates: {label}")

    print("Northsignal Labs GitHub signal label validation")
    print(f"root: {ROOT}")
    print(f"declared labels: {len(declared_labels)}")
    print(f"issue-template labels: {len(template_labels)}")
    print(f"required signal labels: {len(REQUIRED_SIGNAL_LABELS)}")
    print(f"required asset signal labels: {len(REQUIRED_ASSET_SIGNAL_LABELS)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
