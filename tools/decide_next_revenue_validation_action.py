#!/usr/bin/env python3
"""Decide the next no-spend revenue-validation action from aggregate public signal.

This helper turns the post-launch aggregate snapshot into an explicit next action so
Northsignal Labs does not drift into low-ROI polish or premature payment setup.
It is intentionally local-only: it reads JSON files, writes one JSON decision, and
never contacts services, authenticates, publishes, creates accounts, collects
personal data, starts payment/KYC, or spends money.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = ROOT / "post-launch-signal-snapshot.json"
DEFAULT_OUTPUT = ROOT / "revenue-validation-decision.json"

ASSET_LABELS = {
    "msp_monthly_security_report": "MSP monthly security report template",
    "nis2_readiness_checklist": "NIS2 readiness checklist",
    "m365_secure_score_report": "M365 Secure Score executive report/generator",
    "cyber_insurance_evidence": "Cyber-insurance evidence checklist/gap-register generator",
    "vciso_qbr_agenda": "vCISO QBR agenda template",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def aggregate_score(aggregate: dict[str, Any]) -> int:
    stars = int(aggregate.get("stars") or 0)
    forks = int(aggregate.get("forks") or 0)
    watchers = int(aggregate.get("watchers") or 0)
    open_issues = int(aggregate.get("open_issues") or 0)
    template_requests = int(aggregate.get("template_requests") or 0)
    commercial_fit_signals = int(aggregate.get("commercial_fit_signals") or 0)
    return stars + watchers + forks * 2 + open_issues * 3 + template_requests * 4 + commercial_fit_signals * 5


def normalize_asset_scores(raw: dict[str, Any] | None) -> dict[str, int]:
    if not raw:
        return {}
    normalized: dict[str, int] = {}
    for key, value in raw.items():
        if key not in ASSET_LABELS:
            continue
        try:
            score = int(value)
        except (TypeError, ValueError):
            continue
        normalized[key] = max(0, min(3, score))
    return normalized


def asset_scores_from_label_counts(snapshot: dict[str, Any]) -> dict[str, int]:
    """Convert aggregate asset label counts into 0..3 decision scores.

    The source is label totals only, not issue bodies, authors, comments, contact
    details, analytics, or private text. One labeled issue is some asset signal;
    two or more is meaningful enough to steer the next no-spend validation step.
    """
    raw_counts = snapshot.get("asset_label_counts") or {}
    derived: dict[str, int] = {}
    for key in ASSET_LABELS:
        try:
            count = int(raw_counts.get(key) or 0)
        except (TypeError, ValueError):
            count = 0
        if count >= 2:
            derived[key] = 3
        elif count == 1:
            derived[key] = 2
        else:
            derived[key] = 0
    return derived


def strongest_asset(asset_scores: dict[str, int]) -> tuple[str | None, int]:
    if not asset_scores:
        return None, 0
    ranked = sorted(asset_scores.items(), key=lambda item: (-item[1], item[0]))
    key, score = ranked[0]
    return key, score


def build_decision(snapshot: dict[str, Any], asset_scores: dict[str, int]) -> dict[str, Any]:
    aggregate = snapshot.get("aggregate_signal") or {}
    signal_score = aggregate_score(aggregate)
    collection_state = str(snapshot.get("collection_state", "unknown"))
    asset_key, asset_score = strongest_asset(asset_scores)
    asset_label = ASSET_LABELS.get(asset_key or "", "not selected")

    guardrail = (
        "no-spend local decision only; no account creation, publishing, posting, analytics, forms, "
        "contact capture, sensitive-data collection, payment/KYC, quote/invoice workflow, or spend"
    )

    if collection_state.startswith("blocked_until"):
        state = "blocked_until_public_url"
        recommendation = "Do not build more assets or payment workflow yet; unblock concrete approved public URL/account fields first."
        fastest_money_path = (
            "A reviewer supplies APPROVAL-HANDOFF-FIELDS.json public_base_url/account metadata, then rerun approval validation, "
            "URL cutover, release telemetry/staging/review/package gates, publish through the approved no-spend channel, "
            "and collect the first aggregate snapshot."
        )
        next_action = "Keep public-channel-fields blocker prominent; no external action is permitted from this local hold state."
    elif signal_score >= 10 or asset_score >= 3:
        state = "meaningful_signal_prioritize_monetization_learning"
        recommendation = (
            "Meaningful early signal: prioritize learning which monetization path is strongest before more distribution. "
            f"Focus first on {asset_label} if manual asset scores are current."
        )
        fastest_money_path = (
            "Use template-request/commercial-fit issue patterns to choose between expanded pack, local generator bundle, "
            "starter kit, evidence/QBR workflow pack, or a productized pilot path; request separate approval before any "
            "payment, quote, invoice, KYC, payout, or sales workflow."
        )
        next_action = "Improve the strongest requested asset or monetization-framing copy locally; do not add paid conversion or contact capture."
    elif signal_score >= 3 or asset_score >= 2:
        state = "some_signal_improve_conversion_path"
        recommendation = (
            "Some signal: improve the conversion path around the asset/request flow that produced interest, then continue careful no-spend distribution."
        )
        fastest_money_path = (
            "Tighten README/landing-page path to the strongest asset and structured GitHub request/commercial-fit templates, "
            "then re-measure aggregate public counters before any monetization build."
        )
        next_action = "Make one local conversion improvement tied to the leading asset/request path and rerun release gates."
    else:
        state = "weak_or_no_signal_prioritize_distribution_metadata"
        recommendation = "Weak/no signal: do not create payment infrastructure or more templates; improve discovery/distribution metadata first."
        fastest_money_path = (
            "After approved launch and one concrete safe venue/manual-post approval, use the existing public-safe message bank for at most one relevant no-spam share; "
            "otherwise limit work to no-spend local snippets/metadata. Wait for aggregate stars/forks/issues/template requests before monetization work."
        )
        next_action = "Improve launch snippets/search/social metadata or channel-specific README wording before building new assets; do not post externally until one venue/manual-post path is approved."

    return {
        "project": "Northsignal Labs MSP Security Reporting Template Pack",
        "generated_at": utc_now(),
        "source_snapshot_state": collection_state,
        "aggregate_signal": {
            "stars": int(aggregate.get("stars") or 0),
            "forks": int(aggregate.get("forks") or 0),
            "watchers": int(aggregate.get("watchers") or 0),
            "open_issues": int(aggregate.get("open_issues") or 0),
            "template_requests": int(aggregate.get("template_requests") or 0),
            "commercial_fit_signals": int(aggregate.get("commercial_fit_signals") or 0),
        },
        "weighted_signal_score": signal_score,
        "manual_asset_scores": asset_scores,
        "leading_asset": {"key": asset_key, "label": asset_label, "score": asset_score},
        "decision_state": state,
        "recommended_next_action": next_action,
        "recommendation": recommendation,
        "fastest_money_path": fastest_money_path,
        "guardrail": guardrail,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Write next no-spend revenue-validation decision from aggregate signal.")
    parser.add_argument("--snapshot", default=str(DEFAULT_SNAPSHOT), help="Path to post-launch-signal-snapshot.json")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Decision JSON output path")
    parser.add_argument(
        "--asset-scores-json",
        help="Optional JSON object with 0..3 weekly asset scores keyed by msp_monthly_security_report, nis2_readiness_checklist, m365_secure_score_report, cyber_insurance_evidence, vciso_qbr_agenda",
    )
    parser.add_argument(
        "--asset-scores-file",
        help="Optional JSON file containing either an asset_scores object or direct 0..3 asset scores for the same keys; use only aggregate public-safe category totals, not issue bodies or personal/client data",
    )
    args = parser.parse_args()

    if args.asset_scores_json and args.asset_scores_file:
        print("use either --asset-scores-json or --asset-scores-file, not both", file=sys.stderr)
        return 2

    snapshot_path = Path(args.snapshot)
    if not snapshot_path.exists():
        print(f"missing snapshot: {snapshot_path}", file=sys.stderr)
        return 2

    snapshot = load_json(snapshot_path)
    raw_asset_scores = None
    if args.asset_scores_json:
        raw_asset_scores = json.loads(args.asset_scores_json)
    elif args.asset_scores_file:
        asset_scores_payload = load_json(Path(args.asset_scores_file))
        raw_asset_scores = asset_scores_payload.get("asset_scores", asset_scores_payload)
    asset_scores = normalize_asset_scores(raw_asset_scores) if raw_asset_scores is not None else asset_scores_from_label_counts(snapshot)
    decision = build_decision(snapshot, asset_scores)
    output = Path(args.output)
    write_json(output, decision)

    print(f"wrote {output}")
    print(f"decision_state: {decision['decision_state']}")
    print(f"weighted_signal_score: {decision['weighted_signal_score']}")
    print(f"recommended_next_action: {decision['recommended_next_action']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
