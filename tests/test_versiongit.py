import versiongit


def test_current_version_exists_and_is_str():
    assert isinstance(versiongit.__version__, str)
