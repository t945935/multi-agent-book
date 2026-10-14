from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class Stage:
    name: str
    requires: List[str]

def default_stages() -> List[Stage]:
    return [
        Stage("spec", []),
        Stage("example", ["spec"]),
        Stage("draft", ["example"]),
        Stage("review", ["draft"]),
        Stage("build", ["review"]),
        Stage("release", ["build"]),
    ]

def ready_stages(done: List[str], stages: List[Stage]) -> List[str]:
    completed = set(done)
    return [s.name for s in stages if s.name not in completed and set(s.requires) <= completed]

def quality_gate(results: Dict[str, bool]) -> bool:
    return all(results.get(key, False) for key in ["tests", "review", "build"])
