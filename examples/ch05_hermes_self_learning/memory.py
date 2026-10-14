from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class ReflectionMemory:
    observations: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)

    def observe(self, text: str) -> None:
        self.observations.append(text)
        lowered = text.lower()
        if "timeout" in lowered:
            self.rules.append("add_timeout_guard")
        if "overwrite" in lowered:
            self.rules.append("check_file_ownership")

    def prompt_hints(self) -> List[str]:
        return sorted(set(self.rules))

def review_risk(memory: ReflectionMemory, task: str) -> str:
    hints = memory.prompt_hints()
    if "add_timeout_guard" in hints and "network" in task.lower():
        return "HIGH"
    return "LOW"
