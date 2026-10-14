from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List

class PaneState(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    DONE = "DONE"

@dataclass
class PaneSnapshot:
    pane_id: str
    agent: str
    last_line: str
    state: PaneState
    alerts: List[str] = field(default_factory=list)

class HerdrSupervisor:
    def __init__(self) -> None:
        self.panes: Dict[str, PaneSnapshot] = {}

    def ingest(self, pane_id: str, agent: str, output: str) -> PaneSnapshot:
        text = output.strip()
        lowered = text.lower()
        if "waiting for input" in lowered or "blocked" in lowered:
            state = PaneState.BLOCKED
        elif "done" in lowered or "passed" in lowered:
            state = PaneState.DONE
        elif text:
            state = PaneState.RUNNING
        else:
            state = PaneState.IDLE
        alerts = []
        if "error" in lowered or "failed" in lowered:
            alerts.append("needs_attention")
        snap = PaneSnapshot(pane_id, agent, text.splitlines()[-1] if text else "", state, alerts)
        self.panes[pane_id] = snap
        return snap

    def dashboard(self) -> Dict[str, int]:
        counts = {state.value: 0 for state in PaneState}
        for snap in self.panes.values():
            counts[snap.state.value] += 1
        return counts
