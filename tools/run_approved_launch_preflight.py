#!/usr/bin/env python3
"""Run the guarded post-approval Northsignal Labs launch preflight.

Filesystem-only orchestrator. It converts an explicitly approved public channel
handoff into the shortest local sequence needed before a reviewer uploads the
manifest-approved static package: validate approval fields, dry-run/apply the
public URL reference cutover when requested, regenerate checksums, rerun release
telemetry gates, prepare the repo-root export, package the ZIP, and validate the
approval packet/bundle/dashboard honesty state.

It intentionally does not infer a URL, create accounts, authenticate, upload,
publish, post publicly, contact anyone, collect analytics/forms/contact data,
create payment/KYC/quote/invoice/sales workflows, or spend money.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "APPROVED-LAUNCH-PREFLIGHT.json"

PRECHECK_COMMANDS = [
    ["tools/validate_approval_handoff.py"],
    ["tools/perform_public_url_cutover.py"],
]

POST_CUTOVER_COMMANDS = [
    ["tools/validate_github_signal_labels.py"],
    ["tools/validate_github_pages_workflow.py"],
    ["tools/write_release_readiness_telemetry.py"],
    ["tools/compare_release_readiness_telemetry.py"],
    ["tools/prepare_public_repo_export.py"],
    ["tools/package_go_live_zip.py"],
    ["tools/validate_public_launch_packet_sync.py"],
    ["tools/validate_public_release_bundle.py"],
    ["tools/validate_dashboard_launch_blocker_honesty.py"],
]


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def command_to_argv(command: list[str]) -> list[str]:
    return [sys.executable, str(ROOT / command[0]), *command[1:]]


def run_command(command: list[str]) -> dict:
    argv = command_to_argv(command)
    completed = subprocess.run(
        argv,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    return {
        "command": "python3 " + " ".join(command),
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": stdout.splitlines()[-18:],
        "stderr_tail": stderr.splitlines()[-18:],
    }


def write_log(results: list[dict], *, mode: str, stopped_before_apply: bool) -> None:
    summary = {
        "project": "Northsignal Labs MSP Security Reporting Template Pack",
        "generated_at": iso_now(),
        "mode": mode,
        "publication_status": "local_only_not_published",
        "overall_pass": all(item["passed"] for item in results),
        "stopped_before_apply": stopped_before_apply,
        "commands": results,
        "guardrails": [
            "Local approval-to-upload preflight only",
            "No URL inference, account creation, authentication, upload, publishing, public posting, analytics, forms, contact capture, payment/KYC, quote/invoice/sales workflow, or spend",
            "A passing preflight prepares local dist/, public-repo-export/, GO-LIVE-PACKAGE.json, and ZIP artifacts for reviewer-controlled use only",
        ],
    }
    LOG_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the post-approval local launch preflight without uploading or creating accounts."
    )
    parser.add_argument(
        "--apply-cutover",
        action="store_true",
        help="After approval validation and dry-run pass, rewrite approved public URL references locally before final gates.",
    )
    parser.add_argument(
        "--precheck-only",
        action="store_true",
        help="Run approval validation and URL-cutover dry run only; do not apply or run final packaging gates.",
    )
    args = parser.parse_args(argv)

    results: list[dict] = []
    stopped_before_apply = False

    for command in PRECHECK_COMMANDS:
        result = run_command(command)
        results.append(result)
        if not result["passed"]:
            write_log(results, mode="precheck_only" if args.precheck_only else "full_preflight", stopped_before_apply=True)
            print("Northsignal Labs approved launch preflight")
            print("state: blocked_before_cutover")
            print(f"failed_command: {result['command']}")
            print(f"wrote {LOG_PATH.relative_to(ROOT)}")
            print("guardrail: no URL/account/upload/post/contact/analytics/payment/spend action occurred")
            return 1

    if args.precheck_only:
        write_log(results, mode="precheck_only", stopped_before_apply=True)
        print("Northsignal Labs approved launch preflight")
        print("state: precheck_passed_dry_run_only")
        print(f"commands_run: {len(results)}")
        print(f"wrote {LOG_PATH.relative_to(ROOT)}")
        print("next: after reviewer confirmation, rerun with --apply-cutover before final gates")
        return 0

    if not args.apply_cutover:
        stopped_before_apply = True
        write_log(results, mode="full_preflight_requires_apply_cutover", stopped_before_apply=True)
        print("Northsignal Labs approved launch preflight")
        print("state: dry_run_passed_apply_cutover_not_requested")
        print(f"commands_run: {len(results)}")
        print(f"wrote {LOG_PATH.relative_to(ROOT)}")
        print("next: rerun with --apply-cutover only after reviewer confirms the approved URL/account fields")
        print("guardrail: no public URL reference rewrite, upload, account creation, public posting, contact, analytics, payment/KYC, quote/invoice workflow, or spend occurred")
        return 2

    apply_result = run_command(["tools/perform_public_url_cutover.py", "--apply"])
    results.append(apply_result)
    if not apply_result["passed"]:
        write_log(results, mode="full_preflight_apply_cutover", stopped_before_apply=False)
        print("Northsignal Labs approved launch preflight")
        print("state: apply_cutover_failed")
        print(f"failed_command: {apply_result['command']}")
        print(f"wrote {LOG_PATH.relative_to(ROOT)}")
        return 1

    for command in POST_CUTOVER_COMMANDS:
        result = run_command(command)
        results.append(result)
        if not result["passed"]:
            write_log(results, mode="full_preflight_apply_cutover", stopped_before_apply=False)
            print("Northsignal Labs approved launch preflight")
            print("state: final_gate_failed")
            print(f"failed_command: {result['command']}")
            print(f"wrote {LOG_PATH.relative_to(ROOT)}")
            print("guardrail: local artifacts may have changed; no upload/account/post/contact/analytics/payment/spend action occurred")
            return 1

    write_log(results, mode="full_preflight_apply_cutover", stopped_before_apply=False)
    print("Northsignal Labs approved launch preflight")
    print("state: ready_for_reviewer_controlled_upload")
    print(f"commands_run: {len(results)}")
    print(f"wrote {LOG_PATH.relative_to(ROOT)}")
    print("artifacts: dist/, public-repo-export/, GO-LIVE-PACKAGE.json, verified ZIP")
    print("guardrail: upload/publication remains reviewer-controlled; no account/auth/post/contact/analytics/payment/spend action occurred")
    return 0


if __name__ == "__main__":
    sys.exit(main())
