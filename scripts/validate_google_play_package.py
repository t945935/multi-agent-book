#!/usr/bin/env python3
"""Validate files and metadata needed for Google Play Books draft upload."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from typing import Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"
DOCS_DIR = ROOT_DIR / "docs"

REQUIRED_FILES = [
    DIST_DIR / "book_interior.pdf",
    DIST_DIR / "cover.pdf",
    DIST_DIR / "cover_1600x2400.jpg",
    DIST_DIR / "multi-agent-book-v1.0.0.epub",
    DIST_DIR / "release_manifest.json",
    DIST_DIR / "multi-agent-book-v1.0.0.zip",
    DOCS_DIR / "google_play_books_metadata.md",
    DOCS_DIR / "google_play_books_checklist.md",
    DOCS_DIR / "store_listing.md",
]

REQUIRED_MANIFEST_ARTIFACTS = [
    "dist/book_interior.pdf",
    "dist/cover.pdf",
    "dist/cover_1600x2400.jpg",
    "dist/multi-agent-book-v1.0.0.epub",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
]


def fail(message: str) -> None:
    print(f"❌ {message}")
    raise SystemExit(1)


def check_files() -> None:
    missing = [p.relative_to(ROOT_DIR).as_posix() for p in REQUIRED_FILES if not p.exists()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))

    for p in [
        DIST_DIR / "book_interior.pdf",
        DIST_DIR / "cover.pdf",
        DIST_DIR / "cover_1600x2400.jpg",
        DIST_DIR / "multi-agent-book-v1.0.0.epub",
    ]:
        if p.stat().st_size <= 0:
            fail(f"Empty artifact: {p.relative_to(ROOT_DIR)}")


def check_manifest() -> Dict:
    manifest_path = DIST_DIR / "release_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("title") != "多 Agent 系統架構與實戰":
        fail("Manifest title mismatch")
    if manifest.get("author") != "Happy eBook Authors":
        fail("Manifest author mismatch")
    if manifest.get("subtitle") != "用 AI Agent 團隊完成寫作、測試、排版與發布":
        fail("Manifest subtitle mismatch")
    artifacts = manifest.get("artifacts", {})
    for rel in REQUIRED_MANIFEST_ARTIFACTS:
        if rel not in artifacts:
            fail(f"Manifest missing artifact: {rel}")
        info = artifacts[rel]
        if not info.get("sha256") or len(info.get("sha256")) != 64:
            fail(f"Manifest artifact has invalid sha256: {rel}")
        if int(info.get("size_bytes", 0)) <= 0:
            fail(f"Manifest artifact has invalid size: {rel}")
    return manifest


def check_zip() -> None:
    zip_path = DIST_DIR / "multi-agent-book-v1.0.0.zip"
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
    expected_suffixes = [
        "dist/book_interior.pdf",
        "dist/cover.pdf",
        "dist/cover_1600x2400.jpg",
        "dist/multi-agent-book-v1.0.0.epub",
        "dist/release_manifest.json",
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
    ]
    for suffix in expected_suffixes:
        if not any(name.endswith(suffix) for name in names):
            fail(f"ZIP missing entry ending with: {suffix}")


def main() -> None:
    check_files()
    manifest = check_manifest()
    check_zip()
    print("==================================================")
    print("✅ Google Play Books package validation passed")
    print("==================================================")
    print(f"Title:    {manifest['title']}")
    print(f"Subtitle: {manifest['subtitle']}")
    print(f"Author:   {manifest['author']}")
    print("Note: create draft / upload / fill metadata may be automated, but Publish requires human approval.")


if __name__ == "__main__":
    main()
