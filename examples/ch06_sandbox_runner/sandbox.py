from __future__ import annotations
import subprocess
from dataclasses import dataclass
from typing import List

DENYLIST = {"rm", "sudo", "mkfs", "shutdown"}

@dataclass(frozen=True)
class SandboxResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


def validate_command(command: List[str]) -> None:
    """Reject commands that are too risky for the teaching sandbox."""
    dangerous = DENYLIST.intersection(command)
    if dangerous:
        joined = ", ".join(sorted(dangerous))
        raise PermissionError(f"dangerous command rejected: {joined}")


def run_command(command: List[str], timeout: float = 2.0) -> SandboxResult:
    validate_command(command)
    try:
        proc = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)
        return SandboxResult(proc.returncode, proc.stdout, proc.stderr, False)
    except subprocess.TimeoutExpired as exc:
        return SandboxResult(124, exc.stdout or "", exc.stderr or "", True)


def summarize(result: SandboxResult) -> str:
    if result.timed_out:
        return "TIMEOUT"
    return "PASS" if result.returncode == 0 else "FAIL"
