from herdr import HerdrSupervisor, PaneState

def test_state_detection():
    sup = HerdrSupervisor()
    snap = sup.ingest("w1:p1", "coder", "tests passed")
    assert snap.state == PaneState.DONE

def test_blocked_and_alerts():
    sup = HerdrSupervisor()
    snap = sup.ingest("w1:p2", "reviewer", "blocked: error in build")
    assert snap.state == PaneState.BLOCKED
    assert snap.alerts == ["needs_attention"]

def test_dashboard_counts():
    sup = HerdrSupervisor()
    sup.ingest("a", "pi", "formatting")
    sup.ingest("b", "codex", "done")
    assert sup.dashboard()["RUNNING"] == 1
    assert sup.dashboard()["DONE"] == 1
