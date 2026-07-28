#!/usr/bin/env python3
"""Review a staged Northsignal Labs release against the source manifest.

Filesystem-only helper. It compares RELEASE-MANIFEST.json with
`dist/STAGED-RELEASE-MANIFEST.json` and the actual files in `dist/` so future
static-release review can catch stale, missing, extra, or modified staged files
before any explicitly approved no-spend publishing route is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "RELEASE-MANIFEST.json"
RELEASE_SUMMARY_PATH = ROOT / "RELEASE-SUMMARY.md"
DEFAULT_DIST = ROOT / "dist"
STAGED_MANIFEST_NAME = "STAGED-RELEASE-MANIFEST.json"

EXCLUDED_NAMES = {
    "status.json",
    "__pycache__",
}
EXCLUDED_SUFFIXES = {
    ".pyc",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def safe_relative_path(value: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"unsafe relative path: {value}")
    return rel


def collect_actual_dist_files(dist: Path) -> set[str]:
    files: set[str] = set()
    if not dist.exists():
        return files
    for path in dist.rglob("*"):
        if path.is_file():
            files.add(path.relative_to(dist).as_posix())
    return files


def find_forbidden_dist_files(dist: Path) -> list[str]:
    forbidden: list[str] = []
    if not dist.exists():
        return forbidden
    for path in dist.rglob("*"):
        rel = path.relative_to(dist).as_posix()
        if path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
            forbidden.append(rel)
    return sorted(forbidden)


def extract_release_summary_claims(path: Path) -> dict[str, int | str | bool]:
    """Extract release-summary claims that should stay in sync with manifests.

    This intentionally checks a few reviewer-facing facts instead of parsing the
    whole Markdown file: release version, expected staged file count, and whether
    the summary still tells reviewers to run the staged-release review helper.
    """
    text = path.read_text(encoding="utf-8")
    claims: dict[str, int | str | bool] = {
        "mentions_review_helper": "tools/review_staged_release.py" in text,
        "mentions_source_manifest": "RELEASE-MANIFEST.json" in text,
        "mentions_staged_manifest": STAGED_MANIFEST_NAME in text,
    }

    version_match = re.search(r"Release version:\s*`([^`]+)`", text)
    if version_match:
        claims["release_version"] = version_match.group(1)

    count_match = re.search(r"Expected staged file count[^:\n]*:\s*(\d+)\s+manifest-approved files", text)
    if count_match:
        claims["expected_file_count"] = int(count_match.group(1))

    # Reviewer-facing count claims can appear outside the package snapshot (for
    # example in the healthy-result checklist).  Keep every current-count claim
    # synchronized so an approved upload reviewer is not handed a stale package
    # size while the first regex above still happens to match.
    all_count_claims: list[int] = []
    for pattern in (
        r"(\d+)\s+required files checked",
        r"(\d+)\s+manifest-approved files copied",
        r"(\d+)\s+manifest-approved files packaged",
        rf"{re.escape(STAGED_MANIFEST_NAME)}`?\s+reports\s+(\d+)\s+files",
    ):
        all_count_claims.extend(int(match) for match in re.findall(pattern, text))
    claims["all_file_count_claims"] = all_count_claims

    return claims


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare RELEASE-MANIFEST.json with dist/STAGED-RELEASE-MANIFEST.json and staged files."
    )
    parser.add_argument("--dist", default=str(DEFAULT_DIST), help="Staged release folder under autonomous-lab/ (default: dist)")
    args = parser.parse_args(argv)

    dist = Path(args.dist)
    if not dist.is_absolute():
        dist = (ROOT / dist).resolve()
    try:
        dist.relative_to(ROOT)
    except ValueError:
        print(f"ERROR: dist must be inside {ROOT}: {dist}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = load_json(MANIFEST_PATH)
        required_files = [safe_relative_path(item).as_posix() for item in manifest.get("required_files", [])]
        staged_manifest_path = dist / STAGED_MANIFEST_NAME
        staged_manifest = load_json(staged_manifest_path)
    except Exception as exc:  # noqa: BLE001 - CLI reports all review failures clearly.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    staged_entries = staged_manifest.get("files", [])
    if not isinstance(staged_entries, list):
        print("ERROR: staged manifest has no files list", file=sys.stderr)
        return 1

    required_set = set(required_files)
    staged_by_path = {str(item.get("path")): item for item in staged_entries if isinstance(item, dict)}
    staged_set = set(staged_by_path)
    actual_files = collect_actual_dist_files(dist)
    actual_release_files = actual_files - {STAGED_MANIFEST_NAME}

    missing_from_staged_manifest = sorted(required_set - staged_set)
    extra_in_staged_manifest = sorted(staged_set - required_set)
    missing_from_dist = sorted(required_set - actual_release_files)
    extra_in_dist = sorted(actual_release_files - required_set)

    for item in missing_from_staged_manifest:
        errors.append(f"required file absent from staged manifest: {item}")
    for item in extra_in_staged_manifest:
        errors.append(f"staged manifest contains non-required file: {item}")
    for item in missing_from_dist:
        errors.append(f"required file absent from dist: {item}")
    for item in extra_in_dist:
        errors.append(f"dist contains non-manifest file: {item}")

    if staged_manifest.get("source_manifest") != "RELEASE-MANIFEST.json":
        warnings.append("staged manifest source_manifest is not RELEASE-MANIFEST.json")
    if staged_manifest.get("source_manifest_version") != manifest.get("version"):
        errors.append(
            "staged manifest version does not match source manifest version: "
            f"{staged_manifest.get('source_manifest_version')} != {manifest.get('version')}"
        )
    if staged_manifest.get("file_count") != len(staged_entries):
        errors.append("staged manifest file_count does not match files list length")
    if len(staged_entries) != len(required_files):
        errors.append(f"staged file list length {len(staged_entries)} does not match required file count {len(required_files)}")

    try:
        summary_claims = extract_release_summary_claims(RELEASE_SUMMARY_PATH)
    except Exception as exc:  # noqa: BLE001 - CLI reports all review failures clearly.
        errors.append(f"could not parse RELEASE-SUMMARY.md drift checks: {exc}")
        summary_claims = {}

    summary_version = summary_claims.get("release_version")
    if summary_version != manifest.get("version"):
        errors.append(
            "RELEASE-SUMMARY.md release version does not match source manifest version: "
            f"{summary_version!r} != {manifest.get('version')!r}"
        )
    summary_count = summary_claims.get("expected_file_count")
    if summary_count != len(required_files):
        errors.append(
            "RELEASE-SUMMARY.md expected staged file count does not match required file count: "
            f"{summary_count!r} != {len(required_files)}"
        )
    for stale_count in summary_claims.get("all_file_count_claims", []):
        if stale_count != len(required_files):
            errors.append(
                "RELEASE-SUMMARY.md reviewer checklist file-count claim does not match required file count: "
                f"{stale_count!r} != {len(required_files)}"
            )
    for claim_name, description in {
        "mentions_review_helper": "tools/review_staged_release.py",
        "mentions_source_manifest": "RELEASE-MANIFEST.json",
        "mentions_staged_manifest": STAGED_MANIFEST_NAME,
    }.items():
        if summary_claims.get(claim_name) is not True:
            errors.append(f"RELEASE-SUMMARY.md does not reference {description}")

    forbidden = find_forbidden_dist_files(dist)
    for item in forbidden:
        errors.append(f"forbidden file staged: {item}")

    for rel in sorted(required_set & actual_release_files & staged_set):
        source = ROOT / rel
        staged = dist / rel
        if not source.is_file():
            errors.append(f"source required file missing: {rel}")
            continue
        source_bytes = source.stat().st_size
        source_sha = sha256_file(source)
        staged_bytes = staged.stat().st_size
        staged_sha = sha256_file(staged)
        entry = staged_by_path[rel]
        if staged_bytes != source_bytes or staged_sha != source_sha:
            errors.append(f"dist file differs from source: {rel}")
        if entry.get("bytes") != staged_bytes:
            errors.append(f"staged manifest byte count mismatch for {rel}")
        if entry.get("sha256") != staged_sha:
            errors.append(f"staged manifest sha256 mismatch for {rel}")

    print("Northsignal Labs staged release review")
    print(f"root: {ROOT}")
    print(f"dist: {dist}")
    print(f"source required files: {len(required_files)}")
    print(f"staged manifest entries: {len(staged_entries)}")
    print(f"actual staged release files: {len(actual_release_files)}")
    print(f"forbidden staged files: {len(forbidden)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")

    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")

    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
