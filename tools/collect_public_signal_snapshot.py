#!/usr/bin/env python3
"""Collect aggregate-only public validation signal after an approved launch.

This helper is intentionally conservative:
- It reads only public repository counters and label-level issue counts from
  GitHub's public API, a local fixture supplied with --fixture, or a reviewer
  supplied manual aggregate JSON for non-GitHub approved free static channels.
- It writes aggregate counts only; no personal data, issue bodies, comments,
  author names, emails, IPs, analytics IDs, cookies, or contact details.
- It does not publish, post, authenticate, spend money, create accounts, or start
  payment/KYC/lead-capture workflows.
- If APPROVAL-HANDOFF-FIELDS.json is still in hold state, live collection stays
  blocked and the helper writes a blocked snapshot instead of guessing a target.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
APPROVAL_PATH = ROOT / "APPROVAL-HANDOFF-FIELDS.json"
DEFAULT_OUTPUT = ROOT / "post-launch-signal-snapshot.json"
USER_AGENT = "Northsignal-Labs-public-signal-snapshot/0.1 (aggregate-only no-auth)"

ASSET_LABELS = {
    "msp_monthly_security_report": "asset:msp-monthly-report",
    "nis2_readiness_checklist": "asset:nis2-readiness",
    "m365_secure_score_report": "asset:m365-secure-score",
    "cyber_insurance_evidence": "asset:cyber-insurance-evidence",
    "vciso_qbr_agenda": "asset:vciso-qbr",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def derive_github_repo_from_public_base_url(public_base_url: str) -> tuple[str, str] | None:
    """Derive owner/repo from a GitHub Pages URL when possible.

    Supported examples:
    - https://northsignal-labs.github.io/msp-security-reporting-template-pack/
      -> northsignal-labs / msp-security-reporting-template-pack
    - https://northsignal-labs.github.io/
      -> northsignal-labs / northsignal-labs.github.io
    """
    parsed = urlparse(public_base_url)
    host = parsed.netloc.lower()
    if parsed.scheme != "https" or not host.endswith(".github.io"):
        return None
    owner = host[: -len(".github.io")]
    path_parts = [part for part in parsed.path.split("/") if part]
    repo = path_parts[0] if path_parts else f"{owner}.github.io"
    if not owner or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,38}", owner):
        return None
    if not repo or not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", repo):
        return None
    return owner, repo


def approval_target(approval_path: Path) -> tuple[dict[str, Any], tuple[str, str] | None]:
    approval = load_json(approval_path)
    required = approval.get("required_fields", {})
    if not approval.get("approved_for_cutover"):
        return approval, None
    public_base_url = str(required.get("public_base_url", "")).strip()
    return approval, derive_github_repo_from_public_base_url(public_base_url)


def fetch_json(url: str, timeout: int) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    with urlopen(request, timeout=timeout) as response:  # nosec B310: public aggregate GitHub API only
        return json.loads(response.read().decode("utf-8"))


def fetch_github_repo(owner: str, repo: str, timeout: int) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    return fetch_json(url, timeout)


def fetch_public_issue_label_count(owner: str, repo: str, label: str, timeout: int) -> int:
    """Return GitHub Search API total_count for public issues with one label.

    The query returns only an aggregate count. The snapshot does not persist issue
    titles, bodies, authors, comments, URLs, or timestamps.
    """
    query = f"repo:{owner}/{repo} is:issue label:{label}"
    from urllib.parse import quote_plus

    payload = fetch_json(f"https://api.github.com/search/issues?q={quote_plus(query)}&per_page=1", timeout)
    return int(payload.get("total_count") or 0)


def non_negative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a non-negative integer, not a boolean")
    try:
        converted = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a non-negative integer") from exc
    if converted < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return converted


def aggregate_from_repo_payload(repo_payload: dict[str, Any]) -> dict[str, int]:
    labeled_counts = repo_payload.get("labeled_issue_counts") or {}
    return {
        "stars": int(repo_payload.get("stargazers_count") or 0),
        "forks": int(repo_payload.get("forks_count") or repo_payload.get("forks") or 0),
        "watchers": int(repo_payload.get("subscribers_count") or repo_payload.get("watchers_count") or 0),
        "open_issues": int(repo_payload.get("open_issues_count") or 0),
        "template_requests": int(labeled_counts.get("template-request") or repo_payload.get("template_requests") or 0),
        "commercial_fit_signals": int(labeled_counts.get("commercial-fit") or repo_payload.get("commercial_fit_signals") or 0),
    }


def asset_label_counts_from_repo_payload(repo_payload: dict[str, Any]) -> dict[str, int]:
    labeled_counts = repo_payload.get("labeled_issue_counts") or {}
    return {asset_key: int(labeled_counts.get(label) or 0) for asset_key, label in ASSET_LABELS.items()}


def aggregate_from_manual_payload(manual_payload: dict[str, Any]) -> dict[str, int]:
    """Read reviewer-supplied aggregate counters for non-GitHub channels.

    This mode is intentionally narrow: it accepts only integer counters and
    does not persist URLs beyond the already-approved public_base_url, referrers,
    usernames, emails, issue text, comments, IPs, or contact details.
    """
    counters = manual_payload.get("aggregate_signal", manual_payload)
    if not isinstance(counters, dict):
        raise ValueError("manual aggregate payload must be a JSON object")
    empty = empty_aggregate_signal()
    return {key: non_negative_int(counters.get(key, 0), key) for key in empty}


def build_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    generated_at = utc_now()
    guardrail = (
        "aggregate public counters only; no issue bodies, comments, authors, emails, IPs, "
        "analytics, forms, cookies, contact capture, payment/KYC, account creation, posting, or spend"
    )

    if args.fixture:
        fixture_path = Path(args.fixture)
        fixture = load_json(fixture_path)
        repo_payload = fixture.get("github_repo_payload", fixture)
        aggregate = aggregate_from_repo_payload(repo_payload)
        return {
            "project": "Northsignal Labs MSP Security Reporting Template Pack",
            "generated_at": generated_at,
            "mode": "fixture",
            "collection_state": "fixture_aggregate_snapshot_written",
            "source": str(fixture_path),
            "target": {
                "platform": "github_fixture",
                "owner": str(repo_payload.get("owner", {}).get("login", "fixture-owner")),
                "repo": str(repo_payload.get("name", "fixture-repo")),
            },
            "aggregate_signal": aggregate,
            "asset_label_counts": asset_label_counts_from_repo_payload(repo_payload),
            "guardrail": guardrail,
            "next_decision_hint": decision_hint(aggregate),
        }

    approval, target = approval_target(Path(args.approval_path))
    required = approval.get("required_fields", {})
    public_base_url = str(required.get("public_base_url", "")).strip()

    if args.manual_aggregate:
        if not approval.get("approved_for_cutover") or not public_base_url:
            return {
                "project": "Northsignal Labs MSP Security Reporting Template Pack",
                "generated_at": generated_at,
                "mode": "manual_aggregate",
                "collection_state": "blocked_until_approved_public_base_url_for_manual_aggregate",
                "source": str(args.manual_aggregate),
                "approval_status": approval.get("status", "unknown"),
                "approved_for_cutover": bool(approval.get("approved_for_cutover")),
                "public_base_url_present": bool(public_base_url),
                "aggregate_signal": empty_aggregate_signal(),
                "asset_label_counts": empty_asset_label_counts(),
                "guardrail": guardrail,
                "blocker": "Manual aggregate counters require a completed approved public_base_url first; do not record pre-launch or guessed signal.",
            }
        try:
            manual_payload = load_json(Path(args.manual_aggregate))
            aggregate = aggregate_from_manual_payload(manual_payload)
            state = "manual_aggregate_snapshot_written"
            error = None
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            aggregate = empty_aggregate_signal()
            state = "manual_aggregate_invalid_no_data_recorded"
            error = f"{type(exc).__name__}: {exc}"
        snapshot = {
            "project": "Northsignal Labs MSP Security Reporting Template Pack",
            "generated_at": generated_at,
            "mode": "manual_aggregate",
            "collection_state": state,
            "source": str(args.manual_aggregate),
            "target": {"platform": "approved_non_github_or_manual_channel", "public_base_url": public_base_url},
            "aggregate_signal": aggregate,
            "asset_label_counts": empty_asset_label_counts(),
            "guardrail": guardrail,
            "next_decision_hint": decision_hint(aggregate),
        }
        if error:
            snapshot["error"] = error
        return snapshot

    if target is None:
        return {
            "project": "Northsignal Labs MSP Security Reporting Template Pack",
            "generated_at": generated_at,
            "mode": "live_public_api",
            "collection_state": "blocked_until_approved_github_pages_public_base_url",
            "source": str(args.approval_path),
            "approval_status": approval.get("status", "unknown"),
            "approved_for_cutover": bool(approval.get("approved_for_cutover")),
            "public_base_url_present": bool(public_base_url),
            "aggregate_signal": empty_aggregate_signal(),
            "asset_label_counts": empty_asset_label_counts(),
            "guardrail": guardrail,
            "blocker": "Complete APPROVAL-HANDOFF-FIELDS.json with an approved GitHub Pages HTTPS URL before live signal collection.",
        }

    owner, repo = target
    try:
        repo_payload = fetch_github_repo(owner, repo, args.timeout)
        repo_payload["labeled_issue_counts"] = {
            "template-request": fetch_public_issue_label_count(owner, repo, "template-request", args.timeout),
            "commercial-fit": fetch_public_issue_label_count(owner, repo, "commercial-fit", args.timeout),
            **{label: fetch_public_issue_label_count(owner, repo, label, args.timeout) for label in ASSET_LABELS.values()},
        }
        aggregate = aggregate_from_repo_payload(repo_payload)
        state = "live_aggregate_snapshot_written"
        error = None
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        aggregate = empty_aggregate_signal()
        state = "live_collection_failed_no_data_recorded"
        error = f"{type(exc).__name__}: {exc}"

    snapshot: dict[str, Any] = {
        "project": "Northsignal Labs MSP Security Reporting Template Pack",
        "generated_at": generated_at,
        "mode": "live_public_api",
        "collection_state": state,
        "source": f"https://api.github.com/repos/{owner}/{repo}",
        "target": {"platform": "github", "owner": owner, "repo": repo, "public_base_url": public_base_url},
        "aggregate_signal": aggregate,
        "asset_label_counts": asset_label_counts_from_repo_payload(repo_payload) if state == "live_aggregate_snapshot_written" else empty_asset_label_counts(),
        "guardrail": guardrail,
        "next_decision_hint": decision_hint(aggregate),
    }
    if error:
        snapshot["error"] = error
    return snapshot


def decision_hint(aggregate: dict[str, int]) -> str:
    score = (
        aggregate.get("stars", 0)
        + aggregate.get("forks", 0) * 2
        + aggregate.get("open_issues", 0) * 3
        + aggregate.get("template_requests", 0) * 4
        + aggregate.get("commercial_fit_signals", 0) * 5
    )
    if score >= 10:
        return "Meaningful early signal: prioritize monetization-path selection and the strongest requested asset before new distribution."
    if score >= 3:
        return "Some signal: improve the asset/request path that generated it and continue no-spend distribution carefully."
    return "No/weak signal: after launch, improve distribution metadata/snippets before building payment or payout workflows."


def empty_aggregate_signal() -> dict[str, int]:
    return {
        "stars": 0,
        "forks": 0,
        "watchers": 0,
        "open_issues": 0,
        "template_requests": 0,
        "commercial_fit_signals": 0,
    }


def empty_asset_label_counts() -> dict[str, int]:
    return {asset_key: 0 for asset_key in ASSET_LABELS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Write aggregate-only post-launch public signal snapshot.")
    parser.add_argument("--approval-path", default=str(APPROVAL_PATH), help="Path to APPROVAL-HANDOFF-FIELDS.json")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Snapshot JSON output path")
    parser.add_argument("--fixture", help="Local GitHub repository payload fixture for offline tests")
    parser.add_argument(
        "--manual-aggregate",
        help=(
            "Reviewer-supplied aggregate-only JSON counters for an approved non-GitHub/equivalent free channel; "
            "requires APPROVAL-HANDOFF-FIELDS.json to be approved and stores no visitor/user/contact details"
        ),
    )
    parser.add_argument("--timeout", type=int, default=10, help="Network timeout in seconds for live public GitHub API")
    args = parser.parse_args()

    snapshot = build_snapshot(args)
    output = Path(args.output)
    write_json(output, snapshot)
    print(f"wrote {output}")
    print(f"collection_state: {snapshot.get('collection_state')}")
    print(f"aggregate_signal: {snapshot.get('aggregate_signal')}")
    return 0 if snapshot.get("collection_state") not in {"live_collection_failed_no_data_recorded", "manual_aggregate_invalid_no_data_recorded"} else 2


if __name__ == "__main__":
    sys.exit(main())
