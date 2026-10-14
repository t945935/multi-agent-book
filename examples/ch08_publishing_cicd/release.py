from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from typing import Dict, List

@dataclass(frozen=True)
class ReleaseManifest:
    version: str
    artifacts: Dict[str, str]
    checks: List[str]

def checksum(data: bytes) -> str:
    return sha256(data).hexdigest()[:12]

def create_manifest(version: str, files: Dict[str, bytes]) -> ReleaseManifest:
    artifacts = {name: checksum(content) for name, content in sorted(files.items())}
    checks = ["typst_compile", "artifact_checksum", "human_release_note"]
    return ReleaseManifest(version, artifacts, checks)

def is_publishable(manifest: ReleaseManifest) -> bool:
    return bool(manifest.version and manifest.artifacts and len(manifest.checks) >= 3)
