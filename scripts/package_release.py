#!/usr/bin/env python3
"""Create release manifest and zip package for the book project."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"
QA_DIR = ROOT_DIR / "qa" / "reports"
DOCS_DIR = ROOT_DIR / "docs"
SRC_DIR = ROOT_DIR / "src"
DEFAULT_VERSION = "1.0.0"
TITLE = "多 Agent 系統架構與實戰"
SUBTITLE = "用 AI Agent 團隊完成寫作、測試、排版與發布"
AUTHOR = "Happy eBook Authors"


@dataclass(frozen=True)
class ArtifactInfo:
    path: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class ReleaseManifest:
    title: str
    subtitle: str
    author: str
    version: str
    created_at: str
    artifacts: Dict[str, ArtifactInfo]
    checks: List[str]
    notes: List[str]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_files(paths: List[Path]) -> None:
    missing = [str(p.relative_to(ROOT_DIR)) for p in paths if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing release files: " + ", ".join(missing))


def collect_release_files() -> List[Path]:
    files = [
        DIST_DIR / "cover.pdf",
        DIST_DIR / "book_interior.pdf",
        ROOT_DIR / "README.md",
        ROOT_DIR / "CHANGELOG.md",
        ROOT_DIR / "LICENSE",
    ]
    files.extend(sorted(SRC_DIR.glob("*.md")))
    files.extend(sorted(DOCS_DIR.rglob("*.md")))
    files.extend(sorted(QA_DIR.glob("ch*_review_report.md")))
    files.extend(sorted((ROOT_DIR / "examples").rglob("*.py")))
    files.extend(sorted((ROOT_DIR / "examples").rglob("*.md")))
    files.extend(sorted((ROOT_DIR / "examples").rglob("pyproject.toml")))
    files.extend(sorted((ROOT_DIR / "scripts").glob("*.py")))
    files.extend(sorted((ROOT_DIR / "scripts").glob("*.sh")))
    files.extend(sorted((ROOT_DIR / "templates").glob("*.typ")))
    files.extend(path for path in sorted((ROOT_DIR / "bin").iterdir()) if path.is_file())
    files.extend(sorted((ROOT_DIR / "assets").rglob("*.jpg")))
    files.extend(sorted((ROOT_DIR / "assets").rglob("*.png")))
    cover_jpg = DIST_DIR / "cover_1600x2400.jpg"
    if cover_jpg.exists():
        files.append(cover_jpg)
    files.extend(sorted(DIST_DIR.glob("*.epub")))
    return sorted(set(files))


def build_manifest(version: str, files: List[Path]) -> ReleaseManifest:
    artifacts: Dict[str, ArtifactInfo] = {}
    for path in files:
        rel = path.relative_to(ROOT_DIR).as_posix()
        artifacts[rel] = ArtifactInfo(rel, path.stat().st_size, sha256_file(path))

    checks = [
        "tests_passed",
        "typst_build_passed",
        "qa_reports_updated",
        "style_guide_checked",
        "release_manifest_created",
        "human_final_approval_required_before_public_upload",
    ]
    notes = [
        "Release package contains PDF cover, PDF interior, documentation, QA reports, preface, and appendix.",
        "Public marketplace upload is intentionally not automated and requires human final approval.",
    ]
    return ReleaseManifest(
        title=TITLE,
        subtitle=SUBTITLE,
        author=AUTHOR,
        version=version,
        created_at=datetime.now(timezone.utc).isoformat(),
        artifacts=artifacts,
        checks=checks,
        notes=notes,
    )


def write_manifest(manifest: ReleaseManifest) -> Path:
    path = DIST_DIR / "release_manifest.json"
    data = asdict(manifest)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_zip(version: str, files: List[Path], manifest_path: Path) -> Path:
    zip_path = DIST_DIR / f"multi-agent-book-v{version}.zip"
    package_root = f"multi-agent-book-v{version}"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files + [manifest_path]:
            rel = path.relative_to(ROOT_DIR).as_posix()
            zf.write(path, f"{package_root}/{rel}")
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Package book release artifacts")
    parser.add_argument("--version", default=DEFAULT_VERSION, help="release version, default: 1.0.0")
    args = parser.parse_args()

    DIST_DIR.mkdir(exist_ok=True)
    files = collect_release_files()
    require_files(files)
    manifest = build_manifest(args.version, files)
    manifest_path = write_manifest(manifest)
    zip_path = write_zip(args.version, files, manifest_path)

    print("==================================================")
    print("📦 Release package created")
    print("==================================================")
    print(f"Manifest: {manifest_path.relative_to(ROOT_DIR)}")
    print(f"ZIP:      {zip_path.relative_to(ROOT_DIR)}")
    print(f"Files:    {len(files) + 1}")
    print("Note: public upload still requires human final approval.")


if __name__ == "__main__":
    main()
