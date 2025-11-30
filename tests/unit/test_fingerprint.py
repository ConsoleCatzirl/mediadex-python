from mediadex import fingerprint


def test_fingerprint(fake_file, fake_file_hash):
    found = fingerprint._generate(fake_file)
    assert found == fake_file_hash
