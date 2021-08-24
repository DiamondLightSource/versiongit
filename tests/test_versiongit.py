import os
import shutil
import stat
import sys
import zipfile
from subprocess import CalledProcessError, check_output
from tempfile import mkdtemp

from mock import Mock, patch

import versiongit
from versiongit._version_git import get_cmdclass

TOP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


class TempRepo:
    def __init__(self, commit):
        # Check the current remotes, and checkout from the first
        self.dir = mkdtemp()
        self.commit = commit
        remotes = check_output("git remote -v".split()).decode()
        first_remote = remotes.splitlines()[0].split()[1]
        command = "git clone --branch %s %s %s" % (commit, first_remote, self.dir)
        check_output(command.split())

    def checkout(self, sha1):
        command = "git -C %s checkout %s" % (self.dir, sha1)
        check_output(command.split())
        self.commit = sha1

    def version(self, d=None):
        if d is None:
            d = self.dir
        version = versiongit._version_git.get_version_from_git(d)
        return version

    def make_dirty(self):
        path = os.path.join(self.dir, "versiongit", "__init__.py")
        with open(path, "a") as f:
            f.write("\n")

    def remove_dir(self, d):
        # https://github.com/trufflesecurity/truffleHog/pull/15
        def del_rw(action, name, exc):
            os.chmod(name, stat.S_IWRITE)
            os.remove(name)

        shutil.rmtree(d, onerror=del_rw)

    def remove_git_dir(self):
        self.remove_dir(os.path.join(self.dir, ".git"))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_dir(self.dir)


class TempArchive:
    def __init__(self):
        self.dir = mkdtemp()
        archive = os.path.join(self.dir, "archive.zip")
        command = "git -C %s archive -o %s HEAD" % (TOP, archive)
        check_output(command.split())
        with zipfile.ZipFile(archive) as z:
            z.extractall(self.dir)

    def change_version(self, sha1, ref_names="HEAD -> master, github/master"):
        path = os.path.join(self.dir, "versiongit", "_version_git.py")
        with open(path) as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            split = line.split(" = ")
            if split[0] == "GIT_REFS":
                lines[i] = '%s = "%s"\n' % (split[0], ref_names)
            elif split[0] == "GIT_SHA1":
                lines[i] = '%s = "%s"\n' % (split[0], sha1)
        with open(path, "w") as f:
            f.writelines(lines)

    def version(self):
        script = os.path.join(self.dir, "versiongit", "command.py")
        version = check_output([sys.executable, script, "--version"]).decode().strip()
        return version

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.dir)
        pass


def test_tmp_doesnt_have_a_dot_git_dir():
    if os.path.exists("/tmp/.git"):
        raise RuntimeError(
            "/tmp/.git exists, quite a few of these tests will fail because of this"
        )


def test_current_version_exists_and_is_str():
    version = versiongit.__version__
    assert str(version) == version


def assert_records_git_error(version, sha1, error):
    assert version == "0.0+unknown"
    assert isinstance(error, CalledProcessError)
    assert (
        error.output.decode().strip().lower()
        == "fatal: not a git repository (or any of the parent directories): .git"
    )
    assert sha1 is None


def test_pre_tagged_version():
    with TempRepo("master") as repo:
        repo.checkout("b4b6df8")
        assert ("0.0+untagged.gb4b6df8", "b4b6df8", None) == repo.version()
        repo.make_dirty()
        assert ("0.0+untagged.gb4b6df8.dirty", "b4b6df8", None) == repo.version()
        repo.remove_git_dir()
        assert_records_git_error(*repo.version())


def test_tagged_version():
    with TempRepo("0.1") as repo:
        assert ("0.1", "8923f27", None) == repo.version()
        repo.make_dirty()
        assert ("0.1+0.g8923f27.dirty", "8923f27", None) == repo.version()
        repo.remove_git_dir()
        assert_records_git_error(*repo.version())


def test_post_tagged_version():
    with TempRepo("master") as repo:
        repo.checkout("b9222df")
        assert ("0.1+2.gb9222df", "b9222df", None) == repo.version()
        repo.make_dirty()
        assert ("0.1+2.gb9222df.dirty", "b9222df", None) == repo.version()
        repo.remove_git_dir()
        assert_records_git_error(*repo.version())


def test_non_matching_tag_version():
    with TempRepo("master") as repo:
        repo.checkout("3440bc2")
        assert ("0.5+3.g3440bc2", "3440bc2", None) == repo.version()
        repo.make_dirty()
        assert ("0.5+3.g3440bc2.dirty", "3440bc2", None) == repo.version()
        repo.remove_git_dir()
        assert_records_git_error(*repo.version())


def bad_git(cmd, **kwargs):
    cmd = [x.replace("git", "bad_git") for x in cmd]
    return check_output(cmd, **kwargs)


@patch("versiongit._version_git.check_output", bad_git)
def test_no_git_errors(capsys):
    with TempRepo("master") as repo:
        if sys.platform.startswith("win"):
            err_msg = "The system cannot find the file specified"
        else:
            err_msg = "No such file or directory"
        repo.checkout("b4b6df8")
        ver, sha1, err = repo.version()
        assert ver == "0.0+unknown"
        assert sha1 is None
        assert err_msg in str(err)
        captured = capsys.readouterr()
        assert not captured.out
        assert err_msg in captured.err


def test_archive_versions():
    with TempArchive() as archive:
        archive.change_version("8923f27", "HEAD -> master, tag: 0.1")
        assert "0.1" == archive.version()
        archive.change_version("b9222df")
        assert "0.0+untagged.gb9222df" == archive.version()


@patch("versiongit._version_git.GIT_REFS", "tag: 0.1")
@patch("versiongit._version_git.GIT_SHA1", "1234567")
def test_mocked_ref_archive_versions(tmpdir):
    assert versiongit._version_git.get_version_from_git(tmpdir) == (
        "0.1",
        "1234567",
        None,
    )


@patch("versiongit._version_git.GIT_SHA1", "1234567")
def test_mocked_hash_archive_versions(tmpdir):
    assert versiongit._version_git.get_version_from_git(tmpdir) == (
        "0.0+untagged.g1234567",
        "1234567",
        None,
    )


def test_cmdclass_buildpy(tmpdir):
    class BuildPy:
        def run(self):
            with open(str(tmpdir.mkdir("tst") / "_version_git.py"), "w") as f:
                f.write("GIT_SHA1 = anything\nGIT_REFS = anything\n")
            self.has_been_run = True

    cmdclass = get_cmdclass(build_py=BuildPy)

    b_inst = cmdclass["build_py"]()
    b_inst.packages = ["tst"]
    b_inst.build_lib = str(tmpdir)

    b_inst.run()
    expected = "GIT_SHA1 = '%s'\nGIT_REFS = 'tag: %s'\n" % (
        versiongit._version_git.git_sha1,
        versiongit.__version__,
    )
    assert expected == tmpdir.join("tst", "_version_git.py").read()
    assert b_inst.has_been_run


def test_cmdclass_sdist(tmpdir):
    class Sdist:
        def make_release_tree(self, base_dir, files):
            with open(str(tmpdir.mkdir("tst") / "_version_git.py"), "w") as f:
                f.write("blah\nGIT_SHA1 = anything\nGIT_REFS = anything\n")
            self.run_with_args = (base_dir, files)

    cmdclass = get_cmdclass(sdist=Sdist)

    b_inst = cmdclass["sdist"]()
    b_inst.distribution = Mock(packages=["tst"])

    b_inst.make_release_tree(str(tmpdir), [])
    expected = "blah\nGIT_SHA1 = '%s'\nGIT_REFS = 'tag: %s'\n" % (
        versiongit._version_git.git_sha1,
        versiongit.__version__,
    )
    assert expected == tmpdir.join("tst", "_version_git.py").read()
    assert b_inst.run_with_args == (tmpdir, [])
