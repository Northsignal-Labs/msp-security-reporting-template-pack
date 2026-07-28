#!/usr/bin/env python3
"""Post-approval live public URL smoke test for Northsignal Labs.

This helper is intentionally blocked while APPROVAL-HANDOFF-FIELDS.json is in
hold state. After an approved public URL has been supplied, local URL cutover has
run, and a reviewer-controlled upload has made the static pack public, it checks
only a small allowlist of public pages over HTTPS and writes an aggregate result.

It does not authenticate, create accounts, upload, post, collect visitor data,
read issue bodies, add analytics, create forms/contact workflows, start payment
or KYC/quote/invoice/sales workflows, or spend money.
"""
from __future__ import annotations

import argparse
import html.parser
import json
import ssl
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
FIELDS_PATH = ROOT / "APPROVAL-HANDOFF-FIELDS.json"
OUT = ROOT / "public-url-smoke-test.json"
BLOCKED_HOSTS = {"northsignal-labs.local", "localhost", "127.0.0.1"}
MAX_BYTES = 1_000_000
DEFAULT_PATHS = [
    "",
    "README.md",
    "download.html",
    "generator-quickstart.html",
    "DOWNLOAD.md",
    "llms.txt",
    "CHECKSUMS.txt",
    "sample-outputs.html",
    "SAMPLE-OUTPUTS.md",
    "request-signal.html",
    "REQUEST-ROADMAP.md",
    "msp-monthly-security-report-template.html",
    "nis2-readiness-checklist.html",
    "m365-secure-score-executive-report-template.html",
    "cyber-insurance-evidence-checklist.html",
    "vciso-qbr-agenda-template.html",
    "generated/msp-monthly-security-report.sample.html",
    "generated/nis2-readiness-summary.sample.html",
    "generated/m365-secure-score-report.sample.html",
    "generated/cyber-insurance-gap-register.sample.html",
    "generated/vciso-qbr-summary.sample.html",
    "robots.txt",
    "sitemap.xml",
    ".github/labels.yml",
    ".github/ISSUE_TEMPLATE/template-request.yml",
    ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
]
RISK_TOKENS = [
    "northsignal-labs.local",
    "localhost",
    "127.0.0.1",
    "<form",
    "google" + "-analytics",
    "google" + "tagmanager",
    "plausible" + ".io",
    "stripe" + ".com",
    "paypal" + ".com",
]


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_fields() -> dict:
    if not FIELDS_PATH.exists():
        return {}
    return json.loads(FIELDS_PATH.read_text(encoding="utf-8"))


def approved_public_base_url(fields: dict) -> str | None:
    required = fields.get("required_fields") if isinstance(fields, dict) else {}
    base_url = (required or {}).get("public_base_url")
    if fields.get("approved_for_cutover") is not True or not isinstance(base_url, str):
        return None
    parsed = urlparse(base_url)
    if parsed.scheme != "https" or not parsed.netloc or (parsed.hostname or "") in BLOCKED_HOSTS:
        return None
    if not base_url.endswith("/"):
        return None
    return base_url


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.forms = 0
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "form":
            self.forms += 1
        if tag.lower() == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def fetch_url(url: str, timeout: int) -> tuple[int, str, bytes]:
    req = Request(url, headers={"User-Agent": "NorthsignalLabsPublicSmoke/0.1"})
    context = ssl.create_default_context()
    with urlopen(req, timeout=timeout, context=context) as response:  # noqa: S310 - approved public HTTPS only.
        status = int(getattr(response, "status", response.getcode()))
        content_type = response.headers.get("content-type", "")
        body = response.read(MAX_BYTES + 1)
        return status, content_type, body


def check_body(rel_path: str, url: str, content_type: str, body: bytes) -> list[str]:
    errors: list[str] = []
    if len(body) == 0:
        errors.append("empty response body")
    if len(body) > MAX_BYTES:
        errors.append(f"response exceeds max smoke-test size {MAX_BYTES} bytes")
    text = body[:MAX_BYTES].decode("utf-8", errors="replace")
    lowered = text.lower()
    for token in RISK_TOKENS:
        if token in lowered:
            errors.append(f"public response contains blocked token: {token}")
    if rel_path.endswith(".html") or rel_path == "":
        parser = LinkParser()
        parser.feed(text)
        if parser.forms:
            errors.append("HTML contains form tags; first validation must not use forms/contact capture")
    if rel_path == "robots.txt" and "sitemap:" not in lowered:
        errors.append("robots.txt does not advertise a sitemap")
    if rel_path == "sitemap.xml" and "<urlset" not in lowered:
        errors.append("sitemap.xml does not look like a sitemap urlset")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke-test approved live public static URL after reviewer-controlled upload.")
    parser.add_argument("--base-url", help="Optional explicit approved HTTPS base URL; must match APPROVAL-HANDOFF-FIELDS.json unless --allow-override-match-check is used.")
    parser.add_argument("--allow-override-match-check", action="store_true", help="For disposable tests only; do not use for launch review.")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()

    fields = load_fields()
    approved_base = approved_public_base_url(fields)
    base_url = args.base_url or approved_base
    errors: list[str] = []
    warnings: list[str] = []
    results: list[dict] = []

    if not approved_base:
        state = "blocked_until_approved_public_base_url"
        summary = {
            "project": "Northsignal Labs MSP Security Reporting Template Pack",
            "checked_at": iso_now(),
            "state": state,
            "approved_public_base_url": None,
            "requests_checked": 0,
            "errors": [],
            "warnings": ["APPROVAL-HANDOFF-FIELDS.json is not ready_for_reviewer_cutover; no public URL was inferred or fetched."],
            "guardrail": "No network request, upload, account creation, contact capture, analytics, payment/KYC, quote/invoice/sales workflow, or spend occurred.",
        }
        OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Northsignal Labs live public URL smoke test")
        print(f"state: {state}")
        print("requests checked: 0")
        print("errors: 0")
        print("warnings: 1")
        return 0

    if args.base_url and not args.allow_override_match_check and args.base_url != approved_base:
        errors.append("--base-url must match APPROVAL-HANDOFF-FIELDS.json public_base_url")

    parsed_base = urlparse(base_url or "")
    if parsed_base.scheme != "https" or not parsed_base.netloc or (parsed_base.hostname or "") in BLOCKED_HOSTS or not (base_url or "").endswith("/"):
        errors.append("base URL must be the approved HTTPS public_base_url ending in / and not a placeholder/local host")

    if not errors:
        for rel_path in DEFAULT_PATHS:
            url = urljoin(base_url, rel_path)
            item = {"path": rel_path or "index", "url": url, "status": None, "bytes": 0, "errors": []}
            try:
                status, content_type, body = fetch_url(url, timeout=args.timeout)
                item.update({"status": status, "content_type": content_type, "bytes": len(body)})
                if status != 200:
                    item["errors"].append(f"expected HTTP 200, got {status}")
                item["errors"].extend(check_body(rel_path, url, content_type, body))
            except Exception as exc:  # noqa: BLE001 - CLI should report fetch failures cleanly.
                item["errors"].append(f"fetch failed: {exc}")
            if item["errors"]:
                errors.extend(f"{item['path']}: {msg}" for msg in item["errors"])
            results.append(item)

    state = "passed" if not errors else "failed"
    summary = {
        "project": "Northsignal Labs MSP Security Reporting Template Pack",
        "checked_at": iso_now(),
        "state": state,
        "approved_public_base_url": approved_base,
        "requests_checked": len(results),
        "paths_checked": DEFAULT_PATHS,
        "results": results,
        "errors": errors,
        "warnings": warnings,
        "guardrail": "Approved public HTTPS GET checks only; no auth, upload, posting, analytics, forms/contact capture, issue-body/user data collection, payment/KYC, quote/invoice/sales workflow, or spend.",
    }
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Northsignal Labs live public URL smoke test")
    print(f"state: {state}")
    print(f"requests checked: {len(results)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    for error in errors[:20]:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
