import sys
import pytest
from sandbox import run_command, summarize, validate_command


def test_success_command():
    res = run_command([sys.executable, "-c", "print('ok')"])
    assert summarize(res) == "PASS"
    assert "ok" in res.stdout


def test_failure_command():
    res = run_command([sys.executable, "-c", "raise SystemExit(3)"])
    assert summarize(res) == "FAIL"


def test_dangerous_command_rejected():
    with pytest.raises(PermissionError):
        validate_command(["sudo", "apt", "install", "demo"])


def test_timeout_command():
    res = run_command([sys.executable, "-c", "import time; time.sleep(0.2)"], timeout=0.01)
    assert summarize(res) == "TIMEOUT"
    assert res.timed_out
