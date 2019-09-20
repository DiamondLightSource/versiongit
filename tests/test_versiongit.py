import sys
from subprocess import check_output
from tempfile import mkdtemp


def checkout_repo_and_import(commit=None):
    # Check the current remotes, and checkout from the first
    d = mkdtemp()
    remotes = check_output("git remote -v".split()).decode()
    first_remote = remotes.splitlines()[0].split()[1]
    clone_command = "git clone"
    if commit:
        clone_command += " --branch %s" % commit
    check_output(("%s %s %s" % (clone_command, first_remote, d)).split())
    sys.path.insert(1, d)
    import versiongit
    return d, versiongit


def test_current_version_exists_and_is_str():
    import versiongit
    assert isinstance(versiongit.__version__, str)


def test_tagged_version():
    d, versiongit = checkout_repo_and_import("0.1")
    assert versiongit.__version__ == "0.1"

