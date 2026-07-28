#!/usr/bin/env python3
"""Generate a cyber-insurance evidence gap register from local JSON.

Filesystem-only utility for Northsignal Labs. It does not call networks,
publish files, create accounts, spend money, or upload client data.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

VALID_ANSWERS = {"yes", "partial", "no", "unknown", "not_applicable"}
VALID_EVIDENCE = {"attached", "partial", "missing", "needs_validation", "not_applicable"}
RISK_ORDER = {"high": 0, "medium": 1, "low": 2}


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("input JSON must be an object")
    return data


def slug(value: Any) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not data.get("entity"):
        errors.append("missing required field: entity")
    controls = data.get("controls")
    if not isinstance(controls, list) or not controls:
        errors.append("controls must be a non-empty list")
        return errors
    for idx, control in enumerate(controls, start=1):
        if not isinstance(control, dict):
            errors.append(f"controls[{idx}] must be an object")
            continue
        if not control.get("control"):
            errors.append(f"controls[{idx}] missing control")
        answer = slug(control.get("current_answer", "unknown"))
        evidence = slug(control.get("evidence_status", "missing"))
        if answer not in VALID_ANSWERS:
            errors.append(f"controls[{idx}] invalid current_answer: {control.get('current_answer')}")
        if evidence not in VALID_EVIDENCE:
            errors.append(f"controls[{idx}] invalid evidence_status: {control.get('evidence_status')}")
    return errors


def risk_of_overstatement(answer: str, evidence: str) -> str:
    if answer == "not_applicable" or evidence == "not_applicable":
        return "low"
    if answer == "yes" and evidence in {"missing", "needs_validation"}:
        return "high"
    if answer in {"yes", "partial"} and evidence == "partial":
        return "medium"
    if answer in {"unknown", "partial"} and evidence in {"missing", "needs_validation"}:
        return "medium"
    if answer == "no" and evidence in {"missing", "needs_validation"}:
        return "medium"
    return "low"


def next_action(control: dict[str, Any], answer: str, evidence: str, risk: str) -> str:
    if control.get("next_action"):
        return str(control["next_action"])
    owner = control.get("owner") or "assigned owner"
    if evidence == "attached" and risk == "low":
        return "Keep evidence with the renewal/application packet and confirm it remains current."
    if answer == "yes" and evidence != "attached":
        return f"Ask {owner} to attach dated evidence before representing this control as implemented."
    if answer == "partial":
        return f"Ask {owner} to document covered systems, exceptions, and remediation plan."
    if answer == "unknown":
        return f"Ask {owner} to validate the answer and mark unsupported claims as unknown until confirmed."
    if answer == "no":
        return f"Ask {owner} to record compensating controls or remediation decision for business review."
    return f"Ask {owner} to review status and evidence before final responses are approved."


def normalize_controls(data: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for control in data.get("controls", []):
        answer = slug(control.get("current_answer", "unknown"))
        evidence = slug(control.get("evidence_status", "missing"))
        risk = risk_of_overstatement(answer, evidence)
        rows.append({
            "control": str(control.get("control", "")),
            "question": str(control.get("question", "")),
            "current_answer": answer.replace("_", " "),
            "evidence_status": evidence.replace("_", " "),
            "risk_of_overstatement": risk,
            "owner": str(control.get("owner", "unassigned")),
            "next_action": next_action(control, answer, evidence, risk),
            "due_date": str(control.get("due_date", "")),
            "notes": str(control.get("notes", "")),
        })
    return sorted(rows, key=lambda row: (RISK_ORDER[row["risk_of_overstatement"]], row["control"].lower()))


def markdown_report(data: dict[str, Any], rows: list[dict[str, str]]) -> str:
    today = date.today().isoformat()
    entity = data.get("entity", "[entity]")
    trigger = data.get("review_trigger", "[renewal/application/client review]")
    scope = data.get("scope", "[systems/entities reviewed]")
    prepared_by = data.get("prepared_by", "Northsignal Labs local generator")
    high = sum(1 for row in rows if row["risk_of_overstatement"] == "high")
    medium = sum(1 for row in rows if row["risk_of_overstatement"] == "medium")
    low = sum(1 for row in rows if row["risk_of_overstatement"] == "low")

    lines = [
        f"# Cyber Insurance Evidence Gap Register — {entity}",
        "",
        "Northsignal Labs — local, evidence-only automation output.",
        "",
        "> Important: this is an operational evidence organizer, not insurance, legal, brokerage, underwriting, audit, or coverage advice. Final representations should be reviewed by the authorized business owner and qualified advisors.",
        "",
        "## Summary",
        "",
        f"- Entity/client: {entity}",
        f"- Review trigger: {trigger}",
        f"- Scope: {scope}",
        f"- Prepared by: {prepared_by}",
        f"- Generated date: {today}",
        f"- Gap count by overstatement risk: high={high}, medium={medium}, low={low}",
        "",
        "## Gap register",
        "",
        "| Control/question | Current answer | Evidence status | Risk of overstatement | Owner | Next action | Due date |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        label = row["control"]
        if row["question"]:
            label = f"{label}: {row['question']}"
        lines.append(
            "| "
            + " | ".join(
                str(value).replace("|", "\\|")
                for value in [
                    label,
                    row["current_answer"],
                    row["evidence_status"],
                    row["risk_of_overstatement"],
                    row["owner"],
                    row["next_action"],
                    row["due_date"] or "[set date]",
                ]
            )
            + " |"
        )
    lines.extend([
        "",
        "## Conservative wording prompts",
        "",
        "- Do not answer `yes` unless the scope and dated evidence support the statement.",
        "- Use `partial` or `unknown` where coverage is not verified across all in-scope systems.",
        "- Keep exceptions, compensating controls, and final approval owner visible before responses are submitted.",
        "",
    ])
    return "\n".join(lines)


def html_report(markdown: str, title: str) -> str:
    body_lines = []
    in_table = False
    for line in markdown.splitlines():
        if line.startswith("# "):
            body_lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_table:
                body_lines.append("</tbody></table>")
                in_table = False
            body_lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("> "):
            body_lines.append(f"<blockquote>{html.escape(line[2:])}</blockquote>")
        elif line.startswith("- "):
            body_lines.append(f"<p>• {html.escape(line[2:])}</p>")
        elif line.startswith("| ") and not set(line.replace("|", "").strip()) <= {"-"}:
            cells = [html.escape(cell.strip()) for cell in line.strip("|").split("|")]
            tag = "th" if not in_table else "td"
            if not in_table:
                body_lines.append("<table><thead>")
            row = "<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in cells) + "</tr>"
            body_lines.append(row)
            if tag == "th":
                body_lines.append("</thead><tbody>")
                in_table = True
        elif line.strip():
            body_lines.append(f"<p>{html.escape(line)}</p>")
    if in_table:
        body_lines.append("</tbody></table>")
    return """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
  <style>body{{font-family:Inter,system-ui,sans-serif;line-height:1.5;margin:32px;max-width:1120px}} table{{border-collapse:collapse;width:100%;font-size:14px}} th,td{{border:1px solid #d9e2ef;padding:8px;vertical-align:top}} th{{background:#f4f7fb;text-align:left}} blockquote{{border-left:4px solid #6aa6ff;margin-left:0;padding-left:14px;color:#445}}</style>
</head>
<body>
{body}
</body>
</html>
""".format(title=html.escape(title), body="\n".join(body_lines))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="local questionnaire JSON input")
    parser.add_argument("--markdown-out", type=Path, required=True, help="Markdown output path")
    parser.add_argument("--html-out", type=Path, help="optional HTML output path")
    args = parser.parse_args(argv)

    data = load_json(args.input)
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    rows = normalize_controls(data)
    markdown = markdown_report(data, rows)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.write_text(markdown, encoding="utf-8")
    print(f"wrote {args.markdown_out}")

    if args.html_out:
        args.html_out.parent.mkdir(parents=True, exist_ok=True)
        args.html_out.write_text(html_report(markdown, f"Cyber Insurance Evidence Gap Register — {data.get('entity', '')}"), encoding="utf-8")
        print(f"wrote {args.html_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
