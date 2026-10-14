import pytest
from workflow import create_plan, approve, build

def test_build_requires_approval():
    with pytest.raises(PermissionError):
        build(create_plan("feature"))

def test_plan_to_build_flow():
    plan = approve(create_plan("feature"))
    artifact = build(plan)
    assert "tests/test_module.py" in artifact.files
    assert "feature" in artifact.summary
