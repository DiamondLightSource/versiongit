import os
import shutil
import sys
import zipfile
from subprocess import check_output
from tempfile import mkdtemp

import versiongit


class TempRepo:
    def __init__(self, commit):
        # Check the current remotes, and checkout from the first
        self.dir = mkdtemp()
        self.commit = commit
        remotes = check_output("git remote -v".split()).decode()
        first_remote = remotes.splitlines()[0].split()[1]
        command = "git clone --branch %s %s %s" % (
            commit, first_remote, self.dir)
        check_output(command.split())

    def checkout(self, sha1):
        command = "git -C %s checkout %s" % (self.dir, sha1)
        check_output(command.split())
        self.commit = sha1

    def version_from_archive(self):
        archive_dir = mkdtemp()
        archive = os.path.join(archive_dir, "archive.zip")
        command = "git -C %s archive -o %s %s" % (
            self.dir, archive, self.commit)
        check_output(command.split())
        with zipfile.ZipFile(archive) as z:
            z.extractall(archive_dir)
        version = self.version(archive_dir)
        shutil.rmtree(archive_dir)
        return version

    def version(self, d=None):
        if d is None:
            d = self.dir
        version = versiongit._version_git.get_version_from_git(d)
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
        shutil.rmtree(self.dir)


def test_current_version_exists_and_is_str():
    assert isinstance(versiongit.__version__, str)


def test_pre_tagged_version():
    with TempRepo("master") as repo:
        repo.checkout("b4b6df8")
        assert repo.version() == "0+untagged.b4b6df8"
        repo.make_dirty()
        assert repo.version() == "0+untagged.b4b6df8.dirty"
        #assert repo.version_from_archive() == "0+unknown.b4b6df8"
        repo.remove_git_dir()
        assert repo.version() == "0+unknown.error"


def test_tagged_version():
    with TempRepo("0.1") as repo:
        assert repo.version() == "0.1"
        repo.make_dirty()
        assert repo.version() == "0.1+0.8923f27.dirty"
        #assert repo.version_from_archive() == "0.1"
        repo.remove_git_dir()
        assert repo.version() == "0+unknown.error"


def test_post_tagged_version():
    with TempRepo("master") as repo:
        repo.checkout("b9222df")
        assert repo.version() == "0.1+2.b9222df"
        repo.make_dirty()
        assert repo.version() == "0.1+2.b9222df.dirty"
        #assert repo.version_from_archive() == "0+unknown.b9222df"
        repo.remove_git_dir()
        assert repo.version() == "0+unknown.error"


def test_archive_versions():
    with TempRepo("master") as repo:
