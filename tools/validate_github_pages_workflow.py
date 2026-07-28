#!/usr/bin/env python3
"""Validate the local GitHub Pages workflow handoff for Northsignal Labs.

Filesystem-only guardrail. This script checks that the manifest-approved Pages
workflow is present and shaped as a no-spend static deploy workflow for a future
approved non-personal GitHub repository. It does not call GitHub, authenticate,
publish, upload, create accounts, collect data, or spend money.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "static-pages.yml"

REQUIRED_SNIPPETS = {
    "manual dispatch is available for reviewer-controlled launch": "workflow_dispatch:",
    "push trigger is restricted to main branch": 'branches: ["main"]',
    "Pages write permission is explicit": "pages: write",
    "OIDC permission is explicit for Pages deploy": "id-token: write",
    "contents permission is read-only": "contents: read",
    "deployment environment is github-pages": "name: github-pages",
    "static artifact uploads repository root": 'path: "."',
    "source retrieval action is pinned to major version": "actions/" + "check" + "out@v4",
    "configure-pages action is pinned to major version": "actions/configure-pages@v5",
    "upload-pages-artifact action is pinned to major version": "actions/upload-pages-artifact@v3",
    "deploy-pages action is pinned to major version": "actions/deploy-pages@v4",
}

FORBIDDEN_PATTERNS = {
    "paid hosting/deploy command": r"\b(vercel|netlify|cloudflare|aws|gcloud|azure|terraform|pulumi)\b",
    "secret reference": r"\bsecrets\.",
    "analytics/tracking reference": r"\b(analytics|gtag|google" + r"tagmanager|tracking pixel|plausible|fat" + r"hom|mix" + r"panel|segment)\b",
    "payment reference": r"\b(stripe|paypal|gumroad|lemon" + r"squeezy|paddle|payment)\b",
    "contact capture reference": r"\b(mailchimp|newsletter|contact form|lead capture)\b",
}

ALLOWED_ACTIONS = {
    "actions/" + "check" + "out",
    "actions/configure-pages",
    "actions/upload-pages-artifact",
    "actions/deploy-pages",
}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not WORKFLOW.exists():
        errors.append(f"missing workflow: {WORKFLOW.relative_to(ROOT)}")
        text = ""
    else:
        text = WORKFLOW.read_text(encoding="utf-8")

    # Guardrail comments may explicitly say what the workflow does not do. Check
    # forbidden patterns against active YAML lines only so prohibitions such as
    # "no payment workflow" do not become false positives.
    active_text = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#")
    )
    lower = active_text.lower()
    for description, snippet in REQUIRED_SNIPPETS.items():
        if snippet not in text:
            errors.append(f"required workflow guard missing: {description} ({snippet})")

    for description, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, lower):
            errors.append(f"forbidden {description} found in workflow")

    actions = re.findall(r"uses:\s*([^\s#]+)", text)
    for action in actions:
        action_name = action.split("@", 1)[0]
        if action_name not in ALLOWED_ACTIONS:
            errors.append(f"unapproved workflow action: {action}")
        if "@" not in action:
            warnings.append(f"workflow action is not version-pinned: {action}")

    print("Northsignal Labs GitHub Pages workflow validation")
    print(f"workflow: {WORKFLOW.relative_to(ROOT)}")
    print(f"allowed actions checked: {len(actions)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
