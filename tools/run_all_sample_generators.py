#!/usr/bin/env python3
"""Regenerate every Northsignal Labs sample report from local JSON fixtures.

Filesystem-only utility: no network calls, no accounts, no publishing, no
analytics/forms/contact capture, no payment/KYC/quote/invoice workflow, and no
spend. This gives future visitors/reviewers one command to verify the full
five-workflow proof-of-value set before an approved public launch.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SampleGenerator:
    name: str
    tool: str
    sample: str
    markdown_out: str
    html_out: str


GENERATORS = [
    SampleGenerator(
        name="MSP monthly security report",
        tool="tools/msp_monthly_security_report_generator.py",
        sample="samples/msp-monthly-security-report.sample.json",
        markdown_out="generated/msp-monthly-security-report.sample.md",
        html_out="generated/msp-monthly-security-report.sample.html",
    ),
    SampleGenerator(
        name="NIS2 readiness evidence summary",
        tool="tools/nis2_readiness_summary_generator.py",
        sample="samples/nis2-readiness-summary.sample.json",
        markdown_out="generated/nis2-readiness-summary.sample.md",
        html_out="generated/nis2-readiness-summary.sample.html",
    ),
    SampleGenerator(
        name="M365 Secure Score executive report",
        tool="tools/m365_secure_score_report_generator.py",
        sample="samples/m365-secure-score-report.sample.json",
        markdown_out="generated/m365-secure-score-report.sample.md",
        html_out="generated/m365-secure-score-report.sample.html",
    ),
    SampleGenerator(
        name="Cyber-insurance evidence gap register",
        tool="tools/cyber_insurance_gap_register_generator.py",
        sample="samples/cyber-insurance-gap-register.sample.json",
        markdown_out="generated/cyber-insurance-gap-register.sample.md",
        html_out="generated/cyber-insurance-gap-register.sample.html",
    ),
    SampleGenerator(
        name="vCISO QBR summary",
        tool="tools/vciso_qbr_summary_generator.py",
        sample="samples/vciso-qbr-summary.sample.json",
        markdown_out="generated/vciso-qbr-summary.sample.md",
        html_out="generated/vciso-qbr-summary.sample.html",
    ),
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Regenerate all manifest-approved sample Markdown/HTML outputs from local JSON fixtures."
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Verify every generator/sample/output path exists, but do not rewrite generated sample outputs.",
    )
    return parser.parse_args(argv)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_paths() -> list[str]:
    errors: list[str] = []
    for generator in GENERATORS:
        for label, rel_path in [("generator", generator.tool), ("sample", generator.sample)]:
            path = ROOT / rel_path
            if not path.exists():
                errors.append(f"missing {label} for {generator.name}: {rel_path}")
            elif not path.is_file():
                errors.append(f"not a regular file: {rel_path}")
        for label, rel_path in [("Markdown output", generator.markdown_out), ("HTML output", generator.html_out)]:
            path = ROOT / rel_path
            if not path.parent.exists():
                errors.append(f"missing output directory for {label} {generator.name}: {path.parent.relative_to(ROOT)}")
    return errors


def run_generator(generator: SampleGenerator) -> int:
    command = [
        sys.executable,
        generator.tool,
        generator.sample,
        "--markdown-out",
        generator.markdown_out,
        "--html-out",
        generator.html_out,
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        print(f"ERROR: {generator.name} generator exited {result.returncode}", file=sys.stderr)
    return result.returncode


def verify_outputs() -> list[str]:
    errors: list[str] = []
    for generator in GENERATORS:
        for label, rel_path in [("Markdown output", generator.markdown_out), ("HTML output", generator.html_out)]:
            path = ROOT / rel_path
            if not path.exists():
                errors.append(f"missing {label} for {generator.name}: {rel_path}")
                continue
            if not path.is_file():
                errors.append(f"not a regular file: {rel_path}")
                continue
            if path.stat().st_size <= 0:
                errors.append(f"empty {label} for {generator.name}: {rel_path}")
    return errors


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    print("Northsignal Labs all-sample generator runner")
    print(f"workflows: {len(GENERATORS)}")

    errors = validate_paths()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if not args.check_only:
        failures = [generator.name for generator in GENERATORS if run_generator(generator) != 0]
        if failures:
            for name in failures:
                print(f"ERROR: failed generator: {name}", file=sys.stderr)
            return 1

    output_errors = verify_outputs()
    if output_errors:
        for error in output_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    mode = "check-only" if args.check_only else "regenerated"
    print(f"state: {mode}")
    for generator in GENERATORS:
        print(f"verified {relative(ROOT / generator.markdown_out)}")
        print(f"verified {relative(ROOT / generator.html_out)}")
    print("errors: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
