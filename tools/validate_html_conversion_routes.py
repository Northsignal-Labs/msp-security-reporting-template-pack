#!/usr/bin/env python3
"""Validate visitor conversion routes across Northsignal Labs HTML entry pages.

Filesystem-only guardrail. It checks that every public HTML entry/asset page routes
visitors toward the highest-value next step: the browser start/download guide,
sample-output proof page, request-signal guide, full README, and (where useful)
the MSP monthly reporting anchor. This protects approved-launch conversion and
aggregate template-request/commercial-fit signal without publishing, analytics,
forms, contact capture, payment/KYC, quote/invoice workflows, or spend.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HTML_ROUTE_REQUIREMENTS: dict[str, list[str]] = {
    "index.html": [
        "msp-monthly-security-report-template.html",
        "download.html",
        "generator-quickstart.html",
        "sample-outputs.html",
        "request-signal.html",
        "REQUEST-ROADMAP.md",
        "README.md",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
    "download.html": [
        "msp-monthly-security-report-template.html",
        "generator-quickstart.html",
        "sample-outputs.html",
        "request-signal.html",
        "REQUEST-ROADMAP.md",
        "README.md",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
    "sample-outputs.html": [
        "download.html",
        "generator-quickstart.html",
        "request-signal.html",
        "README.md",
    ],
    "generator-quickstart.html": [
        "download.html",
        "sample-outputs.html",
        "request-signal.html",
        "README.md",
        "REQUEST-ROADMAP.md",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
    "request-signal.html": [
        "download.html",
        "README.md",
        "REQUEST-ROADMAP.md",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
    "msp-monthly-security-report-template.html": [
        "download.html",
        "sample-outputs.html",
        "request-signal.html",
        "README.md",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
    "nis2-readiness-checklist.html": [
        "download.html",
        "sample-outputs.html",
        "request-signal.html",
        "README.md",
        "msp-monthly-security-report-template.html",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
    "m365-secure-score-executive-report-template.html": [
        "download.html",
        "sample-outputs.html",
        "request-signal.html",
        "README.md",
        "msp-monthly-security-report-template.html",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
    "cyber-insurance-evidence-checklist.html": [
        "download.html",
        "sample-outputs.html",
        "request-signal.html",
        "README.md",
        "msp-monthly-security-report-template.html",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
    "vciso-qbr-agenda-template.html": [
        "download.html",
        "sample-outputs.html",
        "request-signal.html",
        "README.md",
        "msp-monthly-security-report-template.html",
        ".github/ISSUE_TEMPLATE/template-request.yml",
        ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    ],
}

REQUIRED_ROUTE_COPY = [
    "approved",
    "template-request",
    "commercial-fit",
]

FORBIDDEN_CONVERSION_RISK_TOKENS = [
    "<form",
    "google" + "-analytics",
    "gtag" + "(",
    "plausible" + ".io",
    "stripe" + ".com",
    "paypal" + ".com",
    "mailto:",
    "quote request",
    "sales contact",
    "book a call",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for rel_path, required_links in sorted(HTML_ROUTE_REQUIREMENTS.items()):
        path = ROOT / rel_path
        text = read_text(path)
        if not text:
            errors.append(f"missing or unreadable HTML route page: {rel_path}")
            continue
        lowered = text.lower()
        for link in required_links:
            if f'href="{link}"' not in text and f"href='{link}'" not in text:
                errors.append(f"{rel_path} does not link to required conversion/signal route: {link}")
        for token in REQUIRED_ROUTE_COPY:
            if token not in lowered:
                errors.append(f"{rel_path} does not mention required route/signal copy token: {token}")
        for token in FORBIDDEN_CONVERSION_RISK_TOKENS:
            if token in lowered:
                errors.append(f"{rel_path} contains forbidden conversion-risk token: {token}")
        if "no form" not in lowered and "without forms" not in lowered and "forms" not in lowered:
            warnings.append(f"{rel_path} may be missing explicit no-forms/data-collection copy")

    print("Northsignal Labs HTML conversion route validation")
    print(f"html pages checked: {len(HTML_ROUTE_REQUIREMENTS)}")
    print(f"required route links checked: {sum(len(v) for v in HTML_ROUTE_REQUIREMENTS.values())}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
