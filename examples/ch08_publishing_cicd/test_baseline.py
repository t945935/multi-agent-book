from release import checksum, create_manifest, is_publishable

def test_checksum_is_stable():
    assert checksum(b"book") == checksum(b"book")

def test_manifest_publishable():
    manifest = create_manifest("1.0.0", {"book.pdf": b"pdf", "cover.pdf": b"cover"})
    assert is_publishable(manifest)
    assert sorted(manifest.artifacts) == ["book.pdf", "cover.pdf"]
