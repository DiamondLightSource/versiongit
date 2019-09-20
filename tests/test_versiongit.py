import os
import shutil
import sys
from subprocess import check_output
from tempfile import mkdtemp

import versiongit


class TempRepo:
    def __init__(self, commit):
        # Check the current remotes, and checkout from the first
        self.dir = mkdtemp()
        remotes = check_output("git remote -v".split()).decode()
        first_remote = remotes.splitlines()[0].split()[1]
        command = "git clone --branch %s %s %s" % (
            commit, first_remote, self.dir)
        check_output(command.split())

    def checkout(self, sha1):
        command = "git -C %s checkout %s" % (self.dir, sha1)
        check_output(command.split())

    def version(self):
        script = os.path.join(self.dir, "versiongit", "command.py")
        version = check_output(
            [sys.executable, script, "--version"]).decode().strip()
        return version

    def make_dirty(self):
        path = os.path.join(self.dir, "versiongit", "__init__.py")
        with open(path, "a") as f:
            f.write("\n")

    def remove_git_dir(self):
        shutil.rmtree(os.path.join(self.dir, ".git"))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #shutil.rmtree(self.dir)
        pass


def test_current_version_exists_and_is_str():
    assert isinstance(versiongit.__version__, str)


def test_pre_tagged_version():
    with TempRepo("master") as repo:
        repo.checkout("395f1b4")
        assert repo.version() == "0+untagged.395f1b4"
        repo.make_dirty()
        assert repo.version() == "0+untagged.395f1b4.dirty"


def test_tagged_version():
    with TempRepo("0.1") as repo:
        assert repo.version() == "0.1"


def test_tagged_version_with_modification():
    with TempRepo("0.1") as repo:
        with open(os.path.join(repo.dir, "versiongit", "__init__.py"), "a") as f:
            f.write("\n")
        assert repo.version() == "0.1+0.395f1b4.dirty"
