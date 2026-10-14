from micro_patch import replace_once, normalize_fullwidth_punctuation

def test_replace_once_success():
    res = replace_once("alpha beta", "beta", "gamma")
    assert res.changed
    assert res.content == "alpha gamma"

def test_replace_once_rejects_ambiguous_match():
    res = replace_once("x x", "x", "y")
    assert not res.changed
    assert res.occurrences == 2

def test_punctuation_normalization():
    assert normalize_fullwidth_punctuation("注意: a,b") == "注意： a，b"
