#!/usr/bin/env python3
"""Generate a Northsignal Labs M365 Secure Score executive report.

No network, no paid services, no account dependency. This is intentionally
small and stdlib-only so the autonomous lab can run it in cron or locally.
It performs pragmatic validation against the companion JSON schema's required
fields/enums/ranges, then writes Markdown and optional standalone HTML.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

POSTURE_ORDER = {"Green": 0, "Amber": 1, "Red": 2}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Input file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("Input JSON must be an object at the top level")
    return data


def validate(data: dict[str, Any]) -> None:
    required = [
        "client_name",
        "reporting_period",
        "prepared_by",
        "secure_score_percent",
        "points_achieved",
        "points_available",
        "overall_posture",
        "top_recommendation",
    ]
    errors: list[str] = []
    for field in required:
        if field not in data or data[field] in (None, ""):
            errors.append(f"missing required field: {field}")

    score = data.get("secure_score_percent")
    if not isinstance(score, (int, float)) or not 0 <= score <= 100:
        errors.append("secure_score_percent must be a number from 0 to 100")
    prev = data.get("previous_score_percent")
    if prev is not None and (not isinstance(prev, (int, float)) or not 0 <= prev <= 100):
        errors.append("previous_score_percent must be null or a number from 0 to 100")
    if not isinstance(data.get("points_achieved"), (int, float)) or data.get("points_achieved", -1) < 0:
        errors.append("points_achieved must be a non-negative number")
    if not isinstance(data.get("points_available"), (int, float)) or data.get("points_available", 0) <= 0:
        errors.append("points_available must be a positive number")
    if data.get("overall_posture") not in POSTURE_ORDER:
        errors.append("overall_posture must be one of: Green, Amber, Red")

    for collection, required_keys in {
        "control_areas": ["area", "status", "evidence_source", "executive_note"],
        "completed_improvements": ["action_completed", "risk_reduced"],
        "recommended_actions": ["priority", "action", "expected_impact", "owner", "target_date", "decision_needed"],
        "exceptions": ["exception", "reason", "owner", "review_date"],
    }.items():
        value = data.get(collection, [])
        if value is None:
            continue
        if not isinstance(value, list):
            errors.append(f"{collection} must be an array")
            continue
        for idx, item in enumerate(value, start=1):
            if not isinstance(item, dict):
                errors.append(f"{collection}[{idx}] must be an object")
                continue
            for key in required_keys:
                if item.get(key) in (None, ""):
                    errors.append(f"{collection}[{idx}] missing {key}")
            if "status" in item and item.get("status") not in POSTURE_ORDER:
                errors.append(f"{collection}[{idx}].status must be Green, Amber, or Red")

    if errors:
        raise SystemExit("Validation failed:\n- " + "\n- ".join(errors))


def fmt_percent(value: Any) -> str:
    if value is None:
        return "not recorded"
    return f"{float(value):.1f}%".replace(".0%", "%")


def posture_sentence(data: dict[str, Any]) -> str:
    score = float(data["secure_score_percent"])
    posture = data["overall_posture"]
    previous = data.get("previous_score_percent")
    if previous is None:
        movement = "No previous-period score was provided, so trend should be established in the next reporting cycle."
    else:
        delta = score - float(previous)
        if delta > 0:
            movement = f"Score improved by {delta:.1f} percentage points since the previous period."
        elif delta < 0:
            movement = f"Score decreased by {abs(delta):.1f} percentage points since the previous period and should be reviewed."
        else:
            movement = "Score is unchanged since the previous period."
    return f"Current posture is **{posture}** at **{fmt_percent(score)}**. {movement}"


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "_None recorded._\n"
    header = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |" for row in rows]
    return "\n".join([header, sep, *body]) + "\n"


def generate_markdown(data: dict[str, Any]) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tenant = data.get("tenant_name") or "not specified"
    controls = sorted(data.get("control_areas", []) or [], key=lambda item: POSTURE_ORDER.get(item.get("status"), 9), reverse=True)

    lines = [
        f"# M365 Secure Score Executive Report — {data['client_name']}",
        "",
        "Prepared by Northsignal Labs / independent automation lab",
        f"Generated: {generated_at}",
        "",
        "> This report is an operational reporting aid. It is not legal advice, does not imply Microsoft affiliation, and does not certify that an environment is secure or compliant.",
        "",
        "## Executive summary",
        "",
        f"- **Client:** {data['client_name']}",
        f"- **Tenant:** {tenant}",
        f"- **Reporting period:** {data['reporting_period']}",
        f"- **Prepared by:** {data['prepared_by']}",
        f"- **Secure Score:** {fmt_percent(data['secure_score_percent'])} ({data['points_achieved']} / {data['points_available']} points)",
        f"- **Previous score:** {fmt_percent(data.get('previous_score_percent'))}",
        f"- **Overall posture:** {data['overall_posture']}",
        f"- **Top recommendation:** {data['top_recommendation']}",
        "",
        posture_sentence(data),
        "",
        "## Control areas",
        "",
        md_table(["Area", "Status", "Evidence source", "Executive note"], [[c.get("area", ""), c.get("status", ""), c.get("evidence_source", ""), c.get("executive_note", "")] for c in controls]),
        "## Completed improvements this period",
        "",
        md_table(["Action completed", "Score impact", "Risk reduced", "Evidence location"], [[i.get("action_completed", ""), i.get("score_impact", ""), i.get("risk_reduced", ""), i.get("evidence_location", "")] for i in data.get("completed_improvements", []) or []]),
        "## Recommended next actions",
        "",
        md_table(["Priority", "Action", "Expected impact", "Owner", "Target date", "Decision needed"], [[a.get("priority", ""), a.get("action", ""), a.get("expected_impact", ""), a.get("owner", ""), a.get("target_date", ""), a.get("decision_needed", "")] for a in sorted(data.get("recommended_actions", []) or [], key=lambda item: item.get("priority", 999))]),
        "## Exceptions / accepted risks",
        "",
        md_table(["Exception", "Reason", "Compensating control", "Owner", "Review date"], [[e.get("exception", ""), e.get("reason", ""), e.get("compensating_control", ""), e.get("owner", ""), e.get("review_date", "")] for e in data.get("exceptions", []) or []]),
        "## Suggested MSP follow-up",
        "",
        "1. Confirm whether any Red/Amber items need leadership approval, budget, or change-window planning.",
        "2. Attach screenshots or exported evidence from Microsoft 365 Defender / Entra / admin portals.",
        "3. Re-run this report next month to show trend, decisions, and completed improvements.",
        "",
    ]
    return "\n".join(lines)


def markdown_to_html(markdown: str, title: str) -> str:
    # Minimal readable renderer; keeps tables/preformatted Markdown intact.
    escaped = html.escape(markdown)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <style>
    body{{margin:0;background:#f6f8fb;color:#162033;font-family:Inter,system-ui,sans-serif;line-height:1.55}}
    main{{max-width:980px;margin:auto;padding:32px 20px}}
    pre{{white-space:pre-wrap;background:white;border:1px solid #dbe3ef;border-radius:16px;padding:22px;box-shadow:0 8px 24px rgba(18,32,51,.06)}}
  </style>
</head>
<body><main><pre>{escaped}</pre></main></body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an M365 Secure Score executive report from JSON input.")
    parser.add_argument("input", type=Path, help="Path to input JSON matching schemas/m365-secure-score-report.schema.json")
    parser.add_argument("--markdown-out", type=Path, required=True, help="Output Markdown path")
    parser.add_argument("--html-out", type=Path, help="Optional standalone HTML output path")
    args = parser.parse_args()

    data = load_json(args.input)
    validate(data)
    markdown = generate_markdown(data)

    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.write_text(markdown, encoding="utf-8")
    print(f"wrote {args.markdown_out}")

    if args.html_out:
        args.html_out.parent.mkdir(parents=True, exist_ok=True)
        args.html_out.write_text(markdown_to_html(markdown, f"M365 Secure Score Report — {data['client_name']}"), encoding="utf-8")
        print(f"wrote {args.html_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
