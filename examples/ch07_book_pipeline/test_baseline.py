from pipeline import default_stages, ready_stages, quality_gate

def test_stage_readiness():
    stages = default_stages()
    assert ready_stages([], stages) == ["spec"]
    assert ready_stages(["spec", "example"], stages) == ["draft"]
    assert ready_stages(["spec", "example", "draft", "review", "build"], stages) == ["release"]

def test_quality_gate():
    assert quality_gate({"tests": True, "review": True, "build": True})
    assert not quality_gate({"tests": True, "review": False, "build": True})
