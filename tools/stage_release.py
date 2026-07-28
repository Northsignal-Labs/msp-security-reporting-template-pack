#!/usr/bin/env python3
"""Stage manifest-approved Northsignal Labs release files into dist/.

Filesystem-only helper. It does not publish, upload, create accounts, contact
services, spend money, or modify any public channel. The staged dist/ folder is
for local review before a future explicitly approved free static release.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "RELEASE-MANIFEST.json"
DEFAULT_DIST = ROOT / "dist"

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


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"missing manifest: {MANIFEST_PATH}")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def safe_relative_path(value: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"unsafe manifest path: {value}")
    return rel


def remove_existing_dist(dist: Path) -> None:
    if not dist.exists():
        return
    try:
        dist.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"refusing to remove dist outside lab root: {dist}") from exc
    if dist == ROOT:
        raise ValueError("refusing to use lab root as dist")
    shutil.rmtree(dist)


def copy_required_files(required_files: list[str], dist: Path) -> list[dict]:
    staged: list[dict] = []
    for item in required_files:
        rel = safe_relative_path(item)
        source = ROOT / rel
        if source.is_symlink():
            raise ValueError(f"refusing to stage symlinked manifest file: {rel}")
        if not source.is_file():
            raise FileNotFoundError(f"required file missing or not a regular file: {rel}")
        target = dist / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        staged.append(
            {
                "path": rel.as_posix(),
                "bytes": target.stat().st_size,
                "sha256": sha256_file(target),
            }
        )
    return staged


def find_forbidden_files(dist: Path) -> list[str]:
    forbidden: list[str] = []
    if not dist.exists():
        return forbidden
    for path in dist.rglob("*"):
        rel = path.relative_to(dist).as_posix()
        if path.is_symlink() or path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
            forbidden.append(rel)
    return forbidden


def write_stage_manifest(dist: Path, source_manifest: dict, staged_files: list[dict]) -> Path:
    summary = {
        "project": source_manifest.get("project", "Northsignal Labs"),
        "source_manifest": "RELEASE-MANIFEST.json",
        "source_manifest_version": source_manifest.get("version"),
        "publication_status": "staged_local_only_not_published",
        "staged_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "guardrails": [
            "Local filesystem copy only",
            "Manifest-approved files only",
            "No upload, account creation, public posting, paid service, payment, no unapproved affiliate links, analytics, or contact workflow",
        ],
        "file_count": len(staged_files),
        "files": staged_files,
    }
    output = dist / "STAGED-RELEASE-MANIFEST.json"
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage manifest-approved static release files into dist/ for local review.")
    parser.add_argument("--dist", default=str(DEFAULT_DIST), help="Destination folder under autonomous-lab/ (default: dist)")
    parser.add_argument("--no-clean", action="store_true", help="Do not remove an existing dist folder before staging")
    args = parser.parse_args(argv)

    dist = Path(args.dist)
    if not dist.is_absolute():
        dist = (ROOT / dist).resolve()
    try:
        dist.relative_to(ROOT)
    except ValueError:
        print(f"ERROR: dist must be inside {ROOT}: {dist}", file=sys.stderr)
        return 2

    manifest = load_manifest()
    required_files = manifest.get("required_files", [])
    if not isinstance(required_files, list) or not required_files:
        print("ERROR: manifest has no required_files list", file=sys.stderr)
        return 2

    try:
        if not args.no_clean:
            remove_existing_dist(dist)
        dist.mkdir(parents=True, exist_ok=True)
        staged_files = copy_required_files(required_files, dist)
        stage_manifest = write_stage_manifest(dist, manifest, staged_files)
        forbidden = find_forbidden_files(dist)
    except Exception as exc:  # noqa: BLE001 - CLI reports all staging failures clearly.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("Northsignal Labs release staging")
    print(f"source root: {ROOT}")
    print(f"dist: {dist}")
    print(f"manifest-approved files copied: {len(staged_files)}")
    print(f"stage manifest: {stage_manifest.relative_to(ROOT)}")
    print(f"forbidden staged files: {len(forbidden)}")
    for item in forbidden:
        print(f"FORBIDDEN: {item}")
    if forbidden:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
