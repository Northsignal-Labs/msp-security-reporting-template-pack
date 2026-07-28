#!/usr/bin/env python3
"""Generate a NIS2 readiness summary from local JSON.

Northsignal Labs filesystem-only utility: no network calls, no paid services,
no account dependency, no publishing, and no client data upload. The output is
an operational evidence summary only. It is not legal, regulatory, audit,
compliance, certification, or professional-services advice and does not decide
NIS2 applicability.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VALID_READINESS = {"Ready", "Partial", "At risk", "Unknown"}
VALID_AREA_STATUS = {"ready", "partial", "missing", "not_reviewed"}
VALID_IMPACT = {"Low", "Medium", "High"}
AREA_STATUS_ORDER = {"missing": 0, "partial": 1, "not_reviewed": 2, "ready": 3}
IMPACT_ORDER = {"High": 0, "Medium": 1, "Low": 2}


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
    for field in ["client_name", "review_date", "prepared_by", "scope", "overall_readiness", "top_gap"]:
        if data.get(field) in (None, ""):
            errors.append(f"missing required field: {field}")
    if data.get("overall_readiness") not in VALID_READINESS:
        errors.append("overall_readiness must be one of: Ready, Partial, At risk, Unknown")

    for field in ["evidence_areas", "gaps", "questions_for_advisor", "recommended_actions"]:
        try:
            items = as_list(data, field)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for idx, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"{field}[{idx}] must be an object")
                continue
            if field == "evidence_areas":
                if not item.get("area"):
                    errors.append(f"evidence_areas[{idx}] missing area")
                if item.get("status") not in VALID_AREA_STATUS:
                    errors.append(f"evidence_areas[{idx}].status must be one of: {', '.join(sorted(VALID_AREA_STATUS))}")
                if item.get("evidence") in (None, ""):
                    errors.append(f"evidence_areas[{idx}] missing evidence")
            if field == "gaps":
                if not item.get("gap"):
                    errors.append(f"gaps[{idx}] missing gap")
                if item.get("impact") not in VALID_IMPACT:
                    errors.append(f"gaps[{idx}].impact must be Low, Medium, or High")
                if not item.get("next_action"):
                    errors.append(f"gaps[{idx}] missing next_action")
            if field == "questions_for_advisor" and not item.get("question"):
                errors.append(f"questions_for_advisor[{idx}] missing question")
            if field == "recommended_actions":
                if not isinstance(item.get("priority"), int) or item.get("priority", 0) < 1:
                    errors.append(f"recommended_actions[{idx}].priority must be an integer >= 1")
                if not item.get("action"):
                    errors.append(f"recommended_actions[{idx}] missing action")
    return errors


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "_None recorded._\n"
    safe_rows = [[str(cell).replace("|", "\\|").replace("\n", " ") for cell in row] for row in rows]
    header = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in safe_rows]
    return "\n".join([header, sep, *body]) + "\n"


def summarize_area_counts(areas: list[dict[str, Any]]) -> str:
    counts = {status: sum(1 for item in areas if item.get("status") == status) for status in sorted(VALID_AREA_STATUS)}
    return (
        f"Evidence areas: ready={counts['ready']}, partial={counts['partial']}, "
        f"missing={counts['missing']}, not_reviewed={counts['not_reviewed']}."
    )


def generate_markdown(data: dict[str, Any]) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    areas = sorted(as_list(data, "evidence_areas"), key=lambda item: (AREA_STATUS_ORDER.get(item.get("status"), 9), str(item.get("area", ""))))
    gaps = sorted(as_list(data, "gaps"), key=lambda item: (IMPACT_ORDER.get(item.get("impact"), 9), str(item.get("gap", ""))))
    actions = sorted(as_list(data, "recommended_actions"), key=lambda item: item.get("priority", 999))
    advisor_questions = as_list(data, "questions_for_advisor")

    lines = [
        f"# NIS2 Readiness Evidence Summary — {data['client_name']}",
        "",
        "Northsignal Labs — local operational evidence summary.",
        f"Generated: {generated_at}",
        "",
        "> This is an operational evidence summary, not legal, regulatory, audit, compliance, certification, or professional-services advice. NIS2 applicability, formal obligations, and reporting duties should be confirmed by qualified legal/compliance advisors.",
        "",
        "## Executive summary",
        "",
        f"- Client/entity: {data['client_name']}",
        f"- Review date: {data['review_date']}",
        f"- Prepared by: {data['prepared_by']}",
        f"- Scope: {data['scope']}",
        f"- Overall readiness: {data['overall_readiness']}",
        f"- Highest-priority gap: {data['top_gap']}",
        "",
        summarize_area_counts(areas),
        "",
        "## Applicability context for qualified review",
        "",
        f"- Sector/supply-chain notes: {data.get('sector_notes', 'not recorded')}",
        f"- Country/local transposition notes: {data.get('country_notes', 'not recorded')}",
        "",
        "## Evidence area status",
        "",
        md_table(["Area", "Status", "Evidence", "Owner", "Notes"], [[a.get("area", ""), a.get("status", ""), a.get("evidence", ""), a.get("owner", ""), a.get("notes", "")] for a in areas]),
        "## Gap register",
        "",
        md_table(["Gap", "Evidence missing", "Impact", "Owner", "Target date", "Next action"], [[g.get("gap", ""), g.get("evidence_missing", ""), g.get("impact", ""), g.get("owner", ""), g.get("target_date", ""), g.get("next_action", "")] for g in gaps]),
        "## Questions for legal/compliance advisor review",
        "",
        md_table(["Question", "Context", "Owner"], [[q.get("question", ""), q.get("context", ""), q.get("owner", "")] for q in advisor_questions]),
        "## Recommended next actions",
        "",
        md_table(["Priority", "Action", "Reason", "Owner", "Target date"], [[a.get("priority", ""), a.get("action", ""), a.get("reason", ""), a.get("owner", ""), a.get("target_date", "")] for a in actions]),
        "## Suggested MSP follow-up",
        "",
        "1. Attach source evidence before sharing privately with stakeholders.",
        "2. Keep applicability and notification questions separate from operational evidence collection.",
        "3. Use qualified legal/compliance review for country/entity/sector obligations before making formal claims.",
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
    parser = argparse.ArgumentParser(description="Generate a NIS2 readiness evidence summary from local JSON input.")
    parser.add_argument("input", type=Path, help="Path to input JSON matching schemas/nis2-readiness-summary.schema.json")
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
        args.html_out.write_text(html_report(markdown, f"NIS2 Readiness Evidence Summary — {data['client_name']}"), encoding="utf-8")
        print(f"wrote {args.html_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
