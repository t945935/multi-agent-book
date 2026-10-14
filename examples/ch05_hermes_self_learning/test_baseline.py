from memory import ReflectionMemory, review_risk

def test_memory_extracts_rules():
    mem = ReflectionMemory()
    mem.observe("network timeout during fetch")
    mem.observe("agent overwrite conflict")
    assert mem.prompt_hints() == ["add_timeout_guard", "check_file_ownership"]

def test_review_risk_uses_memory():
    mem = ReflectionMemory()
    mem.observe("timeout")
    assert review_risk(mem, "network sync") == "HIGH"
    assert review_risk(mem, "format text") == "LOW"
