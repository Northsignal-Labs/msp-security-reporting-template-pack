#!/usr/bin/env python3
"""Generate a vCISO-style QBR summary from local JSON.

Northsignal Labs filesystem-only utility: no network calls, no paid services,
no account dependency, no publishing, and no client data upload. The output is
an operational meeting summary and decision/action register only. It is not
legal, compliance, audit, insurance, regulatory, certification, risk-acceptance,
or professional vCISO advice.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VALID_STATUS = {"green", "amber", "red", "unknown"}
VALID_EFFORT = {"S", "M", "L", "Unknown"}
VALID_DECISION = {"approve", "park", "escalate", "needs_review"}
STATUS_ORDER = {"red": 0, "amber": 1, "unknown": 2, "green": 3}
EFFORT_ORDER = {"S": 0, "M": 1, "L": 2, "Unknown": 3}


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
    for field in ["client_name", "quarter", "meeting_date", "prepared_by", "scope", "executive_summary"]:
        if data.get(field) in (None, ""):
            errors.append(f"missing required field: {field}")

    for field in ["attendees", "scorecard", "top_risks", "decisions_requested", "action_register"]:
        try:
            items = as_list(data, field)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for idx, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"{field}[{idx}] must be an object")
                continue
            if field == "attendees":
                if not item.get("role"):
                    errors.append(f"attendees[{idx}] missing role")
            elif field == "scorecard":
                if not item.get("area"):
                    errors.append(f"scorecard[{idx}] missing area")
                if item.get("status") not in VALID_STATUS:
                    errors.append(f"scorecard[{idx}].status must be one of: {', '.join(sorted(VALID_STATUS))}")
                if not item.get("business_impact"):
                    errors.append(f"scorecard[{idx}] missing business_impact")
            elif field == "top_risks":
                if not item.get("risk"):
                    errors.append(f"top_risks[{idx}] missing risk")
                if item.get("status") not in VALID_STATUS:
                    errors.append(f"top_risks[{idx}].status must be one of: {', '.join(sorted(VALID_STATUS))}")
                if not item.get("owner"):
                    errors.append(f"top_risks[{idx}] missing owner")
            elif field == "decisions_requested":
                if not item.get("decision"):
                    errors.append(f"decisions_requested[{idx}] missing decision")
                if item.get("decision_type") not in VALID_DECISION:
                    errors.append(f"decisions_requested[{idx}].decision_type must be one of: {', '.join(sorted(VALID_DECISION))}")
                if not item.get("reason"):
                    errors.append(f"decisions_requested[{idx}] missing reason")
            elif field == "action_register":
                if not isinstance(item.get("priority"), int) or item.get("priority", 0) < 1:
                    errors.append(f"action_register[{idx}].priority must be an integer >= 1")
                if not item.get("action"):
                    errors.append(f"action_register[{idx}] missing action")
                if item.get("effort") not in VALID_EFFORT:
                    errors.append(f"action_register[{idx}].effort must be one of: {', '.join(sorted(VALID_EFFORT))}")
                if not item.get("owner"):
                    errors.append(f"action_register[{idx}] missing owner")
    return errors


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "_None recorded._\n"
    safe_rows = [[str(cell).replace("|", "\\|").replace("\n", " ") for cell in row] for row in rows]
    header = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in safe_rows]
    return "\n".join([header, sep, *body]) + "\n"


def summarize_status_counts(items: list[dict[str, Any]]) -> str:
    counts = {status: sum(1 for item in items if item.get("status") == status) for status in sorted(VALID_STATUS)}
    return f"Scorecard status: green={counts['green']}, amber={counts['amber']}, red={counts['red']}, unknown={counts['unknown']}."


def generate_markdown(data: dict[str, Any]) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    attendees = as_list(data, "attendees")
    scorecard = sorted(as_list(data, "scorecard"), key=lambda item: (STATUS_ORDER.get(item.get("status"), 9), str(item.get("area", ""))))
    risks = sorted(as_list(data, "top_risks"), key=lambda item: (STATUS_ORDER.get(item.get("status"), 9), str(item.get("risk", ""))))
    decisions = as_list(data, "decisions_requested")
    actions = sorted(as_list(data, "action_register"), key=lambda item: (item.get("priority", 999), EFFORT_ORDER.get(item.get("effort"), 9)))

    lines = [
        f"# vCISO QBR Summary — {data['client_name']} — {data['quarter']}",
        "",
        "Northsignal Labs — local operational QBR summary.",
        f"Generated: {generated_at}",
        "",
        "> This is an operational meeting summary and planning aid, not legal, compliance, audit, insurance, regulatory, certification, risk-acceptance, or professional vCISO advice. Business risk acceptance and regulated obligations should be confirmed by qualified owners/advisors.",
        "",
        "## Meeting context",
        "",
        f"- Client/entity: {data['client_name']}",
        f"- Quarter: {data['quarter']}",
        f"- Meeting date: {data['meeting_date']}",
        f"- Prepared by: {data['prepared_by']}",
        f"- Scope: {data['scope']}",
        "",
        "## Attendees / decision roles",
        "",
        md_table(["Role", "Decision responsibility", "Notes"], [[a.get("role", ""), a.get("decision_responsibility", ""), a.get("notes", "")] for a in attendees]),
        "## Executive summary",
        "",
        data["executive_summary"],
        "",
        summarize_status_counts(scorecard),
        "",
        "## Executive security scorecard",
        "",
        md_table(["Area", "Status", "Evidence date", "Business impact", "Next action", "Owner"], [[s.get("area", ""), s.get("status", ""), s.get("evidence_date", ""), s.get("business_impact", ""), s.get("next_action", ""), s.get("owner", "")] for s in scorecard]),
        "## Top risk / exception discussion",
        "",
        md_table(["Risk", "Status", "Evidence", "Owner", "Decision needed", "Review trigger"], [[r.get("risk", ""), r.get("status", ""), r.get("evidence", ""), r.get("owner", ""), r.get("decision_needed", ""), r.get("review_trigger", "")] for r in risks]),
        "## Decisions requested",
        "",
        md_table(["Decision", "Type", "Reason", "Options", "Decision owner"], [[d.get("decision", ""), d.get("decision_type", ""), d.get("reason", ""), d.get("options", ""), d.get("decision_owner", "")] for d in decisions]),
        "## Quarterly action register",
        "",
        md_table(["Priority", "Action", "Risk reduced", "Effort", "Owner", "Due date", "Status"], [[a.get("priority", ""), a.get("action", ""), a.get("risk_reduced", ""), a.get("effort", ""), a.get("owner", ""), a.get("due_date", ""), a.get("status", "")] for a in actions]),
        "## Suggested QBR closeout wording",
        "",
        "Use bounded, evidence-backed language: confirm what evidence was reviewed, what remains open, who owns each decision, and when the next review trigger occurs. Avoid saying risk is eliminated, the client is secure, or that the MSP has accepted business/legal/insurance risk on the client's behalf.",
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
    parser = argparse.ArgumentParser(description="Generate a vCISO QBR summary from local JSON input.")
    parser.add_argument("input", type=Path, help="Path to input JSON matching schemas/vciso-qbr-summary.schema.json")
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
        args.html_out.write_text(html_report(markdown, f"vCISO QBR Summary — {data['client_name']}"), encoding="utf-8")
        print(f"wrote {args.html_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
