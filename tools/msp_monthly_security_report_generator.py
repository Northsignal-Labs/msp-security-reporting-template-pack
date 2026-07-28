#!/usr/bin/env python3
"""Generate a monthly MSP security report from local JSON.

Northsignal Labs filesystem-only utility: no network calls, no paid services,
no account dependency, no publishing, and no client data upload. The output is
an operational reporting aid, not legal, audit, insurance, compliance, or
professional-services advice.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

VALID_POSTURES = {"Green", "Amber", "Red"}
VALID_TRENDS = {"up", "down", "flat", "new", "not_tracked"}
VALID_SEVERITY = {"Low", "Medium", "High", "Critical"}
VALID_STATUS = {"open", "in_progress", "closed", "accepted", "deferred"}
POSTURE_ORDER = {"Red": 0, "Amber": 1, "Green": 2}
SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
RISK_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("input JSON must be an object")
    return data


def as_list(data: dict[str, Any], field: str) -> list[Any]:
    value = data.get(field, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    return value


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ["client_name", "reporting_period", "prepared_by", "overall_posture", "top_recommendation"]:
        if data.get(field) in (None, ""):
            errors.append(f"missing required field: {field}")
    if data.get("overall_posture") not in VALID_POSTURES:
        errors.append("overall_posture must be one of: Green, Amber, Red")

    list_fields = ["areas", "metrics", "changes", "incidents", "risks", "evidence", "recommended_actions", "decision_log"]
    for field in list_fields:
        try:
            items = as_list(data, field)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for idx, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"{field}[{idx}] must be an object")
                continue
            if field == "areas":
                if not item.get("area"):
                    errors.append(f"areas[{idx}] missing area")
                if item.get("status") not in VALID_POSTURES:
                    errors.append(f"areas[{idx}].status must be Green, Amber, or Red")
            if field == "metrics":
                if not item.get("metric"):
                    errors.append(f"metrics[{idx}] missing metric")
                if item.get("trend", "not_tracked") not in VALID_TRENDS:
                    errors.append(f"metrics[{idx}].trend must be one of: {', '.join(sorted(VALID_TRENDS))}")
            if field == "incidents":
                if not item.get("summary"):
                    errors.append(f"incidents[{idx}] missing summary")
                if item.get("severity", "Low") not in VALID_SEVERITY:
                    errors.append(f"incidents[{idx}].severity must be Low, Medium, High, or Critical")
            if field == "risks":
                if not item.get("risk"):
                    errors.append(f"risks[{idx}] missing risk")
                if item.get("likelihood", "Medium") not in RISK_ORDER:
                    errors.append(f"risks[{idx}].likelihood must be Low, Medium, or High")
                if item.get("status", "open") not in VALID_STATUS:
                    errors.append(f"risks[{idx}].status must be one of: {', '.join(sorted(VALID_STATUS))}")
            if field == "recommended_actions" and not item.get("action"):
                errors.append(f"recommended_actions[{idx}] missing action")
            if field == "decision_log" and not item.get("decision_needed"):
                errors.append(f"decision_log[{idx}] missing decision_needed")
    return errors


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "_None recorded._\n"
    safe_rows = [[str(cell).replace("|", "\\|").replace("\n", " ") for cell in row] for row in rows]
    header = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in safe_rows]
    return "\n".join([header, sep, *body]) + "\n"


def sort_areas(areas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(areas, key=lambda item: (POSTURE_ORDER.get(item.get("status"), 9), str(item.get("area", ""))))


def summarize(data: dict[str, Any]) -> str:
    areas = as_list(data, "areas")
    counts = {posture: sum(1 for item in areas if item.get("status") == posture) for posture in ["Red", "Amber", "Green"]}
    incident_count = len(as_list(data, "incidents"))
    open_risks = sum(1 for item in as_list(data, "risks") if item.get("status", "open") in {"open", "in_progress", "deferred"})
    return (
        f"Overall posture is **{data['overall_posture']}**. "
        f"Area status count: Red={counts['Red']}, Amber={counts['Amber']}, Green={counts['Green']}. "
        f"Recorded incidents/alerts: {incident_count}. Open or deferred risks: {open_risks}."
    )


def generate_markdown(data: dict[str, Any]) -> str:
    today = date.today().isoformat()
    areas = sort_areas(as_list(data, "areas"))
    metrics = as_list(data, "metrics")
    incidents = sorted(as_list(data, "incidents"), key=lambda item: SEVERITY_ORDER.get(item.get("severity", "Low"), 9))
    risks = sorted(as_list(data, "risks"), key=lambda item: (RISK_ORDER.get(item.get("likelihood", "Medium"), 9), str(item.get("risk", ""))))
    actions = sorted(as_list(data, "recommended_actions"), key=lambda item: item.get("priority", 999))

    lines = [
        f"# MSP Monthly Security Report — {data['client_name']}",
        "",
        "Northsignal Labs — local operational reporting output.",
        "",
        "> This report is an operational reporting aid. It is not legal, audit, insurance, compliance, certification, or professional-services advice. Replace sample values with verified client-specific evidence before external use.",
        "",
        "## Executive summary",
        "",
        f"- Client: {data['client_name']}",
        f"- Reporting period: {data['reporting_period']}",
        f"- Prepared by: {data['prepared_by']}",
        f"- Generated date: {today}",
        f"- Overall security posture: {data['overall_posture']}",
        f"- Highest-priority action: {data['top_recommendation']}",
        "",
        summarize(data),
        "",
        "## Security areas",
        "",
        md_table(["Area", "Status", "Notes", "Evidence source"], [[a.get("area", ""), a.get("status", ""), a.get("notes", ""), a.get("evidence_source", "")] for a in areas]),
        "## Key changes this month",
        "",
        md_table(["Change", "Impact", "Evidence"], [[c.get("change", ""), c.get("impact", ""), c.get("evidence", "")] for c in as_list(data, "changes")]),
        "## Metrics snapshot",
        "",
        md_table(["Metric", "Current", "Target", "Trend", "Source"], [[m.get("metric", ""), m.get("current", ""), m.get("target", ""), m.get("trend", "not_tracked"), m.get("source", "")] for m in metrics]),
        "## Incidents and notable alerts",
        "",
        md_table(["Date", "Summary", "Severity", "Action taken", "Current status"], [[i.get("date", ""), i.get("summary", ""), i.get("severity", ""), i.get("action_taken", ""), i.get("current_status", "")] for i in incidents]),
        "## Risk register update",
        "",
        md_table(["Risk", "Business impact", "Likelihood", "Owner", "Due date", "Status"], [[r.get("risk", ""), r.get("business_impact", ""), r.get("likelihood", ""), r.get("owner", ""), r.get("due_date", ""), r.get("status", "")] for r in risks]),
        "## Evidence checklist",
        "",
        md_table(["Evidence item", "Status", "Location/notes"], [[e.get("item", ""), e.get("status", ""), e.get("location", "")] for e in as_list(data, "evidence")]),
        "## Recommended next actions",
        "",
        md_table(["Priority", "Action", "Reason", "Owner", "Due date"], [[a.get("priority", ""), a.get("action", ""), a.get("reason", ""), a.get("owner", ""), a.get("due_date", "")] for a in actions]),
        "## Client decision log",
        "",
        md_table(["Decision needed", "Options", "Recommendation", "Decision/date"], [[d.get("decision_needed", ""), d.get("options", ""), d.get("recommendation", ""), d.get("decision_date", "pending")] for d in as_list(data, "decision_log")]),
        "## Suggested MSP follow-up",
        "",
        "1. Attach source evidence before sending externally.",
        "2. Keep the executive summary to one highest-priority action and a short posture explanation.",
        "3. Carry unresolved risks and decisions into the next monthly report or QBR agenda.",
        "",
    ]
    return "\n".join(lines)


def html_report(markdown: str, title: str) -> str:
    escaped = html.escape(markdown)
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <style>
    body{{font-family:Inter,system-ui,sans-serif;line-height:1.55;margin:0;background:#f6f8fb;color:#152033}}
    main{{max-width:1100px;margin:auto;padding:32px 20px}}
    pre{{white-space:pre-wrap;background:#fff;border:1px solid #dbe3ef;border-radius:16px;padding:22px;box-shadow:0 8px 24px rgba(18,32,51,.06)}}
  </style>
</head>
<body><main><pre>{escaped}</pre></main></body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an MSP monthly security report from local JSON input.")
    parser.add_argument("input", type=Path, help="Path to input JSON matching schemas/msp-monthly-security-report.schema.json")
    parser.add_argument("--markdown-out", type=Path, required=True, help="Markdown output path")
    parser.add_argument("--html-out", type=Path, help="Optional standalone HTML output path")
    args = parser.parse_args(argv)

    data = load_json(args.input)
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    markdown = generate_markdown(data)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.write_text(markdown, encoding="utf-8")
    print(f"wrote {args.markdown_out}")

    if args.html_out:
        args.html_out.parent.mkdir(parents=True, exist_ok=True)
        args.html_out.write_text(html_report(markdown, f"MSP Monthly Security Report — {data['client_name']}"), encoding="utf-8")
        print(f"wrote {args.html_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
