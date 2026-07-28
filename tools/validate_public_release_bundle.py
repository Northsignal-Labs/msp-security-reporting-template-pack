#!/usr/bin/env python3
"""Validate public-release bundle completeness for Northsignal Labs.

Filesystem-only launch-risk guardrail. It verifies that the manifest-approved
static package still includes the assets needed to move from an approved public
URL to measurable validation signal: visitor entry points, reuse/license files,
GitHub Pages/static deployment handoff, structured request/commercial-fit signal
hooks, aggregate-only signal tooling, and public-safe contribution/security
boundaries. It also verifies that internal approval packets and generated ZIP
artifacts are not accidentally included in the public manifest.

It does not publish, upload, authenticate, contact services, collect data, add
analytics, create accounts, create payment/KYC/quote/invoice workflows, or spend
money.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "RELEASE-MANIFEST.json"
README = ROOT / "README.md"
TOOLS_README = ROOT / "tools" / "README.md"
PUBLIC_PACKET = ROOT / "PUBLIC-LAUNCH-APPROVAL-PACKET.md"
CHECKSUMS = ROOT / "CHECKSUMS.txt"
COMMERCIAL_FIT_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "commercial-fit-signal.yml"
TEMPLATE_REQUEST_TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "template-request.yml"
PUBLIC_URL_CUTOVER_TOOL = ROOT / "tools" / "perform_public_url_cutover.py"
ASSET_SCORES = ROOT / "asset-scores.json"

# These files directly shorten approval-to-launch or launch-to-signal time.
REQUIRED_SIGNAL_AND_LAUNCH_FILES = {
    "README.md": "repository entry point and conversion routing",
    "llms.txt": "AI/search discovery summary for accurate pack routing and guardrails",
    "CHECKSUMS.txt": "public file integrity hashes for reviewer/upload verification",
    "download.html": "browser-friendly visitor start/download guide",
    "generator-quickstart.html": "browser-friendly one-command generator proof guide",
    "DOWNLOAD.md": "visitor start/download guide",
    "SAMPLE-OUTPUTS.md": "sample output preview page for faster visitor evaluation",
    "sample-outputs.html": "browser-friendly sample output gallery for faster visitor evaluation",
    "request-signal.html": "browser-friendly public-safe request/commercial-fit signal routing",
    "REQUEST-ROADMAP.md": "public-safe request roadmap for no-spend follow-up prioritization",
    "LICENSE": "explicit reuse permission for forks/copies/internal MSP use",
    ".nojekyll": "GitHub Pages static serving compatibility",
    "index.html": "HTML entry point",
    "robots.txt": "post-approval public URL discovery placeholder",
    "sitemap.xml": "post-approval public URL discovery placeholder",
    "REPOSITORY-METADATA.md": "copy/paste repository about/release metadata",
    "REPOSITORY-METADATA.json": "machine-readable repository metadata for copy/paste-safe approved launch setup",
    "SECURITY.md": "public-safe sensitive-data boundary",
    "CONTRIBUTING.md": "public-safe contribution rules",
    "APPROVAL-HANDOFF-FIELDS.json": "machine-readable approved URL/account fields",
    "PUBLIC-URL-CUTOVER-CHECKLIST.md": "post-approval URL cutover sequence",
    "SIGNAL-TRACKING.md": "aggregate-only measurement rules",
    "FIRST-7-DAY-VALIDATION-PLAN.md": "post-approval week-one demand validation plan",
    "APPROVED-GITHUB-PAGES-LAUNCH-RUNBOOK.md": "post-approval GitHub Pages day-0 launch sequence",
    "manual-aggregate-counters.example.json": "non-GitHub aggregate fallback fixture",
    "asset-signal-scores.example.json": "aggregate-only asset scoring fixture for post-launch revenue-validation decisions",
    ".github/ISSUE_TEMPLATE/template-request.yml": "structured demand-validation hook",
    ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml": "non-binding monetization-learning hook",
    ".github/ISSUE_TEMPLATE/config.yml": "blank issue disablement",
    ".github/labels.yml": "label metadata for aggregate request/commercial-fit counts",
    ".github/workflows/static-pages.yml": "post-approval GitHub Pages deployment handoff",
    "GITHUB-LABEL-SETUP.md": "label setup handoff for aggregate measurement",
    "GITHUB-PAGES-SETUP.md": "privacy-safe approved repository setup notes",
    "DISTRIBUTION-MESSAGE-BANK.md": "post-approval no-spam distribution copy",
    "tools/collect_public_signal_snapshot.py": "aggregate-only public signal collection",
    "tools/smoke_test_public_url.py": "post-upload live public URL smoke test for approved HTTPS launch",
    "tools/decide_next_revenue_validation_action.py": "money-first next-action decision",
    "tools/run_all_sample_generators.py": "one-command local proof run for all generated sample outputs",
    "tools/write_release_checksums.py": "public file checksum generation for stale artifact detection",
    "tools/apply_public_channel_fields.py": "reviewer-supplied public channel fields application helper",
    "tools/perform_public_url_cutover.py": "validator-gated public URL reference cutover",
    "tools/validate_approval_handoff.py": "approval field preflight",
    "tools/validate_github_signal_labels.py": "signal-label alignment guardrail",
    "tools/validate_github_pages_workflow.py": "Pages workflow guardrail",
    "tools/validate_public_launch_packet_sync.py": "approval packet freshness guardrail",
    "tools/validate_html_conversion_routes.py": "HTML entry/asset conversion route guardrail",
    "tools/validate_public_release_bundle.py": "this bundle completeness guardrail",
    "tools/run_approved_launch_preflight.py": "one-command post-approval local cutover/gate/package preflight",
}

# These files are useful internally, but should not be manifest-approved public files.
MUST_NOT_BE_PUBLIC_MANIFEST_FILES = {
    "PUBLIC-LAUNCH-APPROVAL-PACKET.md",
    "GO-LIVE-PACKAGE.json",
    "northsignal-labs-msp-security-reporting-template-pack-v0.1.zip",
    "release-readiness-telemetry.json",
    "post-launch-signal-snapshot.json",
    "revenue-validation-decision.json",
    "status.json",
    "PUBLIC-URL-CUTOVER-LOG.json",
    "APPROVED-LAUNCH-PREFLIGHT.json",
}

REQUIRED_README_REFERENCES = [
    "DOWNLOAD.md",
    "download.html",
    "generator-quickstart.html",
    "llms.txt",
    "SAMPLE-OUTPUTS.md",
    "sample-outputs.html",
    "request-signal.html",
    "REQUEST-ROADMAP.md",
    "REPOSITORY-METADATA.md",
    ".github/ISSUE_TEMPLATE/template-request.yml",
    ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
    "tools/collect_public_signal_snapshot.py",
    "tools/smoke_test_public_url.py",
    "tools/decide_next_revenue_validation_action.py",
    "FIRST-7-DAY-VALIDATION-PLAN.md",
    "APPROVED-GITHUB-PAGES-LAUNCH-RUNBOOK.md",
    "asset-signal-scores.example.json",
    "CHECKSUMS.txt",
    "tools/validate_public_release_bundle.py",
    "tools/validate_html_conversion_routes.py",
    "tools/run_all_sample_generators.py",
    "tools/write_release_checksums.py",
    "tools/apply_public_channel_fields.py",
    "tools/run_approved_launch_preflight.py",
]

REQUIRED_TOOLS_README_REFERENCES = [
    "tools/validate_public_release_bundle.py",
    "tools/validate_public_launch_packet_sync.py",
    "tools/validate_html_conversion_routes.py",
    "tools/run_all_sample_generators.py",
    "tools/validate_github_pages_workflow.py",
    "tools/validate_github_signal_labels.py",
    "tools/collect_public_signal_snapshot.py",
    "tools/smoke_test_public_url.py",
    "tools/decide_next_revenue_validation_action.py",
    "tools/run_approved_launch_preflight.py",
]

REQUIRED_COMMERCIAL_FIT_TEMPLATE_TOKENS = [
    "id: strongest-paid-path",
    "id: urgency",
    "id: value-band",
    "id: buyer-workflow",
    "id: monetization-trigger",
    "id: missing-piece",
    "not a purchase, quote, invoice, sales contact",
    "Do not include client names",
]

REQUIRED_TEMPLATE_REQUEST_TOKENS = [
    "id: asset",
    "id: role-context",
    "id: request-intent",
    "id: operational-urgency",
    "id: requested-improvement",
    "New template for the same MSP/security reporting workflow",
    "Local generator or import/export support",
    "How soon would this help with a real operational workflow?",
    "Do not include client names",
]

REQUIRED_PUBLIC_URL_SMOKE_PATHS = [
    "download.html",
    "generator-quickstart.html",
    "llms.txt",
    "CHECKSUMS.txt",
    "sample-outputs.html",
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
    ".github/labels.yml",
    ".github/ISSUE_TEMPLATE/template-request.yml",
    ".github/ISSUE_TEMPLATE/commercial-fit-signal.yml",
]

REQUIRED_PUBLIC_URL_SMOKE_GUARDRAILS = [
    "northsignal-labs.local",
    "<form",
    '"stripe" + ".com"',
    '"paypal" + ".com"',
    "requests_checked",
    "no auth, upload, posting, analytics, forms/contact capture",
]

REQUIRED_SCHEMA_ID_FILES = [
    "schemas/msp-monthly-security-report.schema.json",
    "schemas/nis2-readiness-summary.schema.json",
    "schemas/m365-secure-score-report.schema.json",
    "schemas/cyber-insurance-gap-register.schema.json",
    "schemas/vciso-qbr-summary.schema.json",
]

REQUIRED_ASSET_SCORE_GENERATOR_FIELDS = {
    "msp-monthly-security-report-template": {
        "schema_path": "autonomous-lab/schemas/msp-monthly-security-report.schema.json",
        "generator_path": "autonomous-lab/tools/msp_monthly_security_report_generator.py",
        "sample_input_path": "autonomous-lab/samples/msp-monthly-security-report.sample.json",
        "sample_output_path": "autonomous-lab/generated/msp-monthly-security-report.sample.md",
        "sample_html_output_path": "autonomous-lab/generated/msp-monthly-security-report.sample.html",
    },
    "nis2-readiness-checklist": {
        "schema_path": "autonomous-lab/schemas/nis2-readiness-summary.schema.json",
        "generator_path": "autonomous-lab/tools/nis2_readiness_summary_generator.py",
        "sample_input_path": "autonomous-lab/samples/nis2-readiness-summary.sample.json",
        "sample_output_path": "autonomous-lab/generated/nis2-readiness-summary.sample.md",
        "sample_html_output_path": "autonomous-lab/generated/nis2-readiness-summary.sample.html",
    },
    "m365-secure-score-executive-report-template": {
        "schema_path": "autonomous-lab/schemas/m365-secure-score-report.schema.json",
        "generator_path": "autonomous-lab/tools/m365_secure_score_report_generator.py",
        "sample_input_path": "autonomous-lab/samples/m365-secure-score-report.sample.json",
        "sample_output_path": "autonomous-lab/generated/m365-secure-score-report.sample.md",
        "sample_html_output_path": "autonomous-lab/generated/m365-secure-score-report.sample.html",
    },
    "cyber-insurance-evidence-checklist": {
        "schema_path": "autonomous-lab/schemas/cyber-insurance-gap-register.schema.json",
        "generator_path": "autonomous-lab/tools/cyber_insurance_gap_register_generator.py",
        "sample_input_path": "autonomous-lab/samples/cyber-insurance-gap-register.sample.json",
        "sample_output_path": "autonomous-lab/generated/cyber-insurance-gap-register.sample.md",
        "sample_html_output_path": "autonomous-lab/generated/cyber-insurance-gap-register.sample.html",
    },
    "vciso-qbr-agenda-template": {
        "schema_path": "autonomous-lab/schemas/vciso-qbr-summary.schema.json",
        "generator_path": "autonomous-lab/tools/vciso_qbr_summary_generator.py",
        "sample_input_path": "autonomous-lab/samples/vciso-qbr-summary.sample.json",
        "sample_output_path": "autonomous-lab/generated/vciso-qbr-summary.sample.md",
        "sample_html_output_path": "autonomous-lab/generated/vciso-qbr-summary.sample.html",
    },
}

REQUIRED_CUTOVER_DOC_TOKENS = {
    "APPROVAL-HANDOFF.md": [
        "generator JSON Schema `$id` references",
        "stale schema identifier",
    ],
    "PUBLIC-URL-CUTOVER-CHECKLIST.md": [
        "generator JSON Schema `$id` references",
        "dist/schemas/*.schema.json",
    ],
    "GITHUB-PAGES-SETUP.md": [
        "generator JSON Schema `$id` values",
        "tools/perform_public_url_cutover.py",
    ],
    "RELEASE-RISK-DIGEST.md": [
        "generator JSON Schema `$id` references",
        "stale schema identifiers",
    ],
    "DISTRIBUTION-READINESS-SCOREBOARD.md": [
        "generator JSON Schema `$id` values",
        "approved HTTPS public base URL",
    ],
    "RELEASE-SUMMARY.md": [
        "generator JSON Schema `$id` values",
        "approved HTTPS public base URL",
    ],
}

# Exact stale phrases that have previously implied analytics, commission/referral,
# sponsorship, or premature monetization paths in public-facing package copy.
# These are intentionally narrow so ordinary no-go guardrail wording remains allowed.
PUBLIC_COPY_RISK_TOKENS = {
    "index.html": [
        "Track visits/downloads/conversions",
        "outreach replies/pilot signal",
    ],
    "PUBLISHING-ROUTES.md": [
        "search-console impressions",
        "If analytics are added",
        "Keep " + "aff" + "iliate/referral placeholders inactive",
    ],
    "SIGNAL-TRACKING.md": [
        "search console",
        "search-console",
        "impressions/clicks",
        "Release/download count if available",
        "Community mentions if discovered manually",
    ],
    "README.md": [
        "simple public interest in downloads",
        "downloads, stars/forks",
    ],
    "CHANGELOG.md": [
        "approved search-console observations",
    ],
    "PUBLICATION-CHECKLIST.md": [
        "Any future analytics are free",
        "not affiliate/referral links unless approved",
        "inactive placeholders until compliant accounts",
    ],
    "PUBLIC-URL-CUTOVER-CHECKLIST.md": [
        "referral, payment, contact, and analytics placeholders remain inactive",
    ],
    "RELEASE-RISK-DIGEST.md": [
        "organic visits, clones, downloads",
    ],
    "REPOSITORY-METADATA.md": [
        "downloads/clones",
        "Manual download/clone/release interest",
    ],
    "DISTRIBUTION-MESSAGE-BANK.md": [
        "stars/forks/clones",
        "safe template requests, or public comments",
    ],
    "assets/msp-monthly-security-report-template.md": [
        "aff" + "iliate links to security tools",
    ],
    "assets/nis2-readiness-checklist.md": [
        "aff" + "iliate/legal referral " + "links",
    ],
    "assets/m365-secure-score-executive-report-template.md": [
        "disclosed " + "aff" + "iliate/referral " + "links",
    ],
    "assets/cyber-insurance-evidence-checklist.md": [
        "broker/MSP referral",
    ],
    "assets/vciso-qbr-agenda-template.md": [
        "sponsored MSP operations resources",
    ],
}


def load_manifest() -> dict:
    if not MANIFEST.exists():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"__json_error__": str(exc)}
    return value if isinstance(value, dict) else {"__json_error__": "top-level JSON value must be an object"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_checksum_rows(text: str) -> dict[str, tuple[str, int]]:
    rows: dict[str, tuple[str, int]] = {}
    for line in text.splitlines():
        match = re.match(r"\| `([0-9a-f]{64})` \| (\d+) \| `([^`]+)` \|", line.strip())
        if match:
            rows[match.group(3)] = (match.group(1), int(match.group(2)))
    return rows


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    manifest = load_manifest()
    required_files = manifest.get("required_files") or []
    required_set = set(required_files)

    if not required_set:
        errors.append("RELEASE-MANIFEST.json has no required_files list")

    for rel_path, reason in sorted(REQUIRED_SIGNAL_AND_LAUNCH_FILES.items()):
        if rel_path not in required_set:
            errors.append(f"missing from manifest: {rel_path} ({reason})")
        elif not (ROOT / rel_path).exists():
            errors.append(f"manifest-listed launch/signal file missing on disk: {rel_path}")

    for rel_path in sorted(required_set):
        path = ROOT / rel_path
        if path.is_symlink():
            errors.append(f"manifest-approved public file must not be a symlink: {rel_path}")

    for rel_path in sorted(MUST_NOT_BE_PUBLIC_MANIFEST_FILES):
        if rel_path in required_set:
            errors.append(f"internal/generated file must not be public manifest-approved: {rel_path}")

    readme_text = read_text(README)
    if not readme_text:
        errors.append("README.md is missing or unreadable")
    else:
        for token in REQUIRED_README_REFERENCES:
            if token not in readme_text:
                errors.append(f"README.md does not reference launch/signal guardrail: {token}")

    tools_readme_text = read_text(TOOLS_README)
    if not tools_readme_text:
        errors.append("tools/README.md is missing or unreadable")
    else:
        for token in REQUIRED_TOOLS_README_REFERENCES:
            if token not in tools_readme_text:
                errors.append(f"tools/README.md does not reference tool: {token}")

    commercial_fit_template_text = read_text(COMMERCIAL_FIT_TEMPLATE)
    if not commercial_fit_template_text:
        errors.append("commercial-fit issue template is missing or unreadable")
    else:
        for token in REQUIRED_COMMERCIAL_FIT_TEMPLATE_TOKENS:
            if token not in commercial_fit_template_text:
                errors.append(f"commercial-fit issue template missing required monetization-learning guardrail: {token}")

    template_request_text = read_text(TEMPLATE_REQUEST_TEMPLATE)
    if not template_request_text:
        errors.append("template-request issue template is missing or unreadable")
    else:
        for token in REQUIRED_TEMPLATE_REQUEST_TOKENS:
            if token not in template_request_text:
                errors.append(f"template-request issue template missing required demand-quality field/guardrail: {token}")

    repo_metadata = load_json_file(ROOT / "REPOSITORY-METADATA.json")
    if not repo_metadata:
        errors.append("REPOSITORY-METADATA.json is missing or unreadable")
    elif repo_metadata.get("__json_error__"):
        errors.append(f"REPOSITORY-METADATA.json is invalid: {repo_metadata['__json_error__']}")
    else:
        repo = repo_metadata.get("repository") if isinstance(repo_metadata.get("repository"), dict) else {}
        topics = repo.get("topics") if isinstance(repo.get("topics"), list) else []
        metrics = repo_metadata.get("first_validation_metrics") if isinstance(repo_metadata.get("first_validation_metrics"), list) else []
        forbidden = repo_metadata.get("forbidden_before_separate_approval") if isinstance(repo_metadata.get("forbidden_before_separate_approval"), list) else []
        for token in ["Northsignal Labs", "MSP Security Reporting Template Pack"]:
            if token not in str(repo.get("display_name", "")):
                errors.append(f"REPOSITORY-METADATA.json display_name missing token: {token}")
        for topic in ["msp", "cybersecurity", "security-reporting", "m365", "nis2", "vciso", "qbr", "templates", "static-site", "python"]:
            if topic not in topics:
                errors.append(f"REPOSITORY-METADATA.json missing repository topic: {topic}")
        for metric in ["aggregate_public_stars", "aggregate_public_forks", "aggregate_public_watchers", "aggregate_public_open_issues", "aggregate_template_request_label_count", "aggregate_commercial_fit_label_count"]:
            if metric not in metrics:
                errors.append(f"REPOSITORY-METADATA.json missing first-validation metric: {metric}")
        forbidden_text = "\n".join(str(item).lower() for item in forbidden)
        for token in ["payment", "analytics", "contact", "personal identity"]:
            if token not in forbidden_text:
                errors.append(f"REPOSITORY-METADATA.json forbidden workflow list missing guardrail token: {token}")
        homepage_policy = str(repo.get("homepage_url_policy", "")).lower()
        if "approved https" not in homepage_policy or "northsignal-labs.local" not in homepage_policy:
            errors.append("REPOSITORY-METADATA.json homepage_url_policy must require approved HTTPS URL and block northsignal-labs.local")

    asset_scores = load_json_file(ASSET_SCORES)
    if not asset_scores:
        errors.append("asset-scores.json is missing or unreadable")
    elif asset_scores.get("__json_error__"):
        errors.append(f"asset-scores.json is invalid: {asset_scores['__json_error__']}")
    else:
        score_items = asset_scores.get("items") if isinstance(asset_scores.get("items"), list) else []
        by_slug = {item.get("slug"): item for item in score_items if isinstance(item, dict)}
        for slug, required_fields in sorted(REQUIRED_ASSET_SCORE_GENERATOR_FIELDS.items()):
            item = by_slug.get(slug)
            if not item:
                errors.append(f"asset-scores.json missing scored generator-backed asset: {slug}")
                continue
            if item.get("status") != "publish_ready_local_with_generator_prototype":
                errors.append(f"asset-scores.json stale status for generator-backed asset {slug}")
            for field, expected in sorted(required_fields.items()):
                if item.get(field) != expected:
                    errors.append(f"asset-scores.json {slug}.{field} must be {expected}")
                rel_path = expected.replace("autonomous-lab/", "", 1)
                if rel_path not in required_set:
                    errors.append(f"asset-scores.json points to non-manifest generator proof file for {slug}: {expected}")
                if not (ROOT / rel_path).exists():
                    errors.append(f"asset-scores.json points to missing generator proof file for {slug}: {expected}")

    public_url_smoke_text = read_text(ROOT / "tools" / "smoke_test_public_url.py")
    if not public_url_smoke_text:
        errors.append("tools/smoke_test_public_url.py is missing or unreadable")
    else:
        for path in REQUIRED_PUBLIC_URL_SMOKE_PATHS:
            if f'\"{path}\"' not in public_url_smoke_text:
                errors.append(f"live public URL smoke test does not check required launch path: {path}")
        for token in REQUIRED_PUBLIC_URL_SMOKE_GUARDRAILS:
            if token not in public_url_smoke_text:
                errors.append(f"live public URL smoke test missing guardrail token: {token}")

    for rel_path in REQUIRED_SCHEMA_ID_FILES:
        schema_text = read_text(ROOT / rel_path)
        if not schema_text:
            errors.append(f"schema file is missing or unreadable: {rel_path}")
            continue
        try:
            schema = json.loads(schema_text)
        except json.JSONDecodeError as exc:
            errors.append(f"schema file is not valid JSON: {rel_path}: {exc}")
            continue
        schema_id = schema.get("$id")
        expected_suffix = "/" + rel_path
        if not isinstance(schema_id, str) or not schema_id.startswith("https://") or not schema_id.endswith(expected_suffix):
            errors.append(f"schema $id must be an HTTPS URL ending in {expected_suffix}: {rel_path}")

    cutover_tool_text = read_text(PUBLIC_URL_CUTOVER_TOOL)
    if not cutover_tool_text:
        errors.append("tools/perform_public_url_cutover.py is missing or unreadable")
    else:
        for rel_path in ["sitemap.xml", "robots.txt", *REQUIRED_SCHEMA_ID_FILES]:
            tokens = rel_path.split("/")
            if not all(token in cutover_tool_text for token in tokens):
                errors.append(f"public URL cutover tool does not target public URL reference file: {rel_path}")

    for rel_path, required_tokens in sorted(REQUIRED_CUTOVER_DOC_TOKENS.items()):
        text = read_text(ROOT / rel_path)
        if not text:
            errors.append(f"public URL cutover documentation is missing or unreadable: {rel_path}")
            continue
        for token in required_tokens:
            if token not in text:
                errors.append(f"public URL cutover documentation missing schema-$id guardrail in {rel_path}: {token}")

    for rel_path, risky_tokens in sorted(PUBLIC_COPY_RISK_TOKENS.items()):
        text = read_text(ROOT / rel_path)
        if not text:
            errors.append(f"public copy risk scan target is missing or unreadable: {rel_path}")
            continue
        lowered = text.lower()
        for token in risky_tokens:
            if token.lower() in lowered:
                errors.append(
                    f"public copy contains stale analytics/commission/referral/monetization-risk wording in {rel_path}: {token}"
                )

    checksums_text = read_text(CHECKSUMS)
    if not checksums_text:
        errors.append("CHECKSUMS.txt is missing or unreadable")
    else:
        checksum_rows = parse_checksum_rows(checksums_text)
        checksum_paths = set(checksum_rows)
        expected_checksum_paths = required_set - {"CHECKSUMS.txt"}
        missing_checksum_paths = sorted(expected_checksum_paths - checksum_paths)
        extra_checksum_paths = sorted(checksum_paths - expected_checksum_paths)
        if missing_checksum_paths:
            errors.append("CHECKSUMS.txt is missing manifest-approved paths: " + ", ".join(missing_checksum_paths[:10]))
        if extra_checksum_paths:
            errors.append("CHECKSUMS.txt contains non-manifest paths: " + ", ".join(extra_checksum_paths[:10]))
        for rel_path in sorted(expected_checksum_paths & checksum_paths):
            path = ROOT / rel_path
            expected_hash, expected_size = checksum_rows[rel_path]
            if path.stat().st_size != expected_size:
                errors.append(f"CHECKSUMS.txt byte count is stale for {rel_path}")
                continue
            if sha256_file(path) != expected_hash:
                errors.append(f"CHECKSUMS.txt SHA-256 is stale for {rel_path}")
        if "no account creation, upload, public posting, analytics, forms, contact capture, payment/KYC, quote/invoice workflow, or spend" not in checksums_text:
            warnings.append("CHECKSUMS.txt may be missing no-upload/no-spend guardrail wording")

    packet_text = read_text(PUBLIC_PACKET)
    if packet_text:
        for phrase in [
            "not authorization to upload",
            "no account, upload, post, analytics, payment workflow, contact collection, or spend",
            "concrete public URL/account fields",
        ]:
            if phrase not in packet_text:
                warnings.append(f"PUBLIC-LAUNCH-APPROVAL-PACKET.md may be missing guardrail phrase: {phrase}")
    else:
        warnings.append("PUBLIC-LAUNCH-APPROVAL-PACKET.md is absent; dashboard approval handoff may be less direct")

    print("Northsignal Labs public release bundle validation")
    print(f"manifest required files: {len(required_files)}")
    print(f"launch/signal files required: {len(REQUIRED_SIGNAL_AND_LAUNCH_FILES)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
