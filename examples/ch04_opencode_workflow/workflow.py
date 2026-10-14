from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Plan:
    goal: str
    steps: List[str]
    approved: bool = False

@dataclass(frozen=True)
class BuildArtifact:
    files: List[str]
    summary: str

def create_plan(goal: str) -> Plan:
    return Plan(goal, ["inspect", "design", "modify", "verify"], False)

def approve(plan: Plan) -> Plan:
    return Plan(plan.goal, plan.steps, True)

def build(plan: Plan) -> BuildArtifact:
    if not plan.approved:
        raise PermissionError("build requires approved plan")
    return BuildArtifact(["src/module.py", "tests/test_module.py"], f"implemented {plan.goal}")
