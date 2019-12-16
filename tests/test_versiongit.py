import os
import shutil
import sys
import zipfile
from subprocess import CalledProcessError, check_output
from tempfile import mkdtemp

import pytest
from mock import Mock, patch

import versiongit
from versiongit._version_git import get_cmdclass
from versiongit.command import main

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

    def remove_git_dir(self):
        shutil.rmtree(os.path.join(self.dir, ".git"))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.dir)


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
            if split[0] == "GIT_ARCHIVE_REF_NAMES":
                split[1] = "'%s'\n" % ref_names
            elif split[0] == "GIT_ARCHIVE_HASH":
                split[1] = "'%s'\n" % sha1
            else:
                continue
            lines[i] = " = ".join(split)
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


def test_current_version_exists_and_is_str():
    assert isinstance(versiongit.__version__, str)


def assert_records_git_error(version, error, sha1):
    assert version == "0+unknown.error"
    assert isinstance(error, CalledProcessError)
    assert (
        error.output.decode().strip().lower()
        == "fatal: not a git repository (or any of the parent directories): .git"
    )
    assert sha1 == "error"


def test_pre_tagged_version():
    with TempRepo("master") as repo:
        repo.checkout("b4b6df8")
        assert ("0+untagged.b4b6df8", None, "b4b6df8") == repo.version()
        repo.make_dirty()
        assert ("0+untagged.b4b6df8.dirty", None, "b4b6df8") == repo.version()
        repo.remove_git_dir()
        assert_records_git_error(*repo.version())


def test_tagged_version():
    with TempRepo("0.1") as repo:
        assert ("0.1", None, "8923f27") == repo.version()
        repo.make_dirty()
        assert ("0.1+0.8923f27.dirty", None, "8923f27") == repo.version()
        repo.remove_git_dir()
        assert_records_git_error(*repo.version())


def test_post_tagged_version():
    with TempRepo("master") as repo:
        repo.checkout("b9222df")
        assert ("0.1+2.b9222df", None, "b9222df") == repo.version()
        repo.make_dirty()
        assert ("0.1+2.b9222df.dirty", None, "b9222df") == repo.version()
        repo.remove_git_dir()
        assert_records_git_error(*repo.version())


def bad_git(cmd, **kwargs):
    cmd = [x.replace("git", "bad_git") for x in cmd]
    return check_output(cmd, **kwargs)


@patch("versiongit._version_git.check_output", bad_git)
def test_no_git_errors():
    with TempRepo("master") as repo:
        repo.checkout("b4b6df8")
        ver, err, md5 = repo.version()
        assert ver == "0+unknown.error"
        assert "No such file or directory: 'bad_git'" in str(err)
        assert md5 == "error"


def test_archive_versions():
    with TempArchive() as archive:
        archive.change_version("8923f27", "HEAD -> master, tag: 0.1")
        assert "0.1" == archive.version()
        archive.change_version("b9222df")
        assert "0+unknown.b9222df" == archive.version()


@patch("versiongit._version_git.GIT_ARCHIVE_REF_NAMES", "tag: 0.1")
@patch("versiongit._version_git.GIT_ARCHIVE_HASH", "1234567")
def test_mocked_ref_archive_versions(tmpdir):
    assert versiongit._version_git.get_version_from_git(tmpdir) == (
        "0.1",
        None,
        "1234567",
    )


@patch("versiongit._version_git.GIT_ARCHIVE_HASH", "1234567")
def test_mocked_hash_archive_versions(tmpdir):
    assert versiongit._version_git.get_version_from_git(tmpdir) == (
        "0+unknown.1234567",
        None,
        "1234567",
    )


def test_cmdclass_buildpy(tmpdir):
    class BuildPy:
        def run(self):
            tmpdir.mkdir("tst")
            self.has_been_run = True

    cmdclass = get_cmdclass(build_py=BuildPy)

    b_inst = cmdclass["build_py"]()
    b_inst.packages = ["tst"]
    b_inst.build_lib = tmpdir

    b_inst.run()
    expected = "__version__ = '%s'\n" % versiongit.__version__
    assert expected == tmpdir.join("tst", "_version_static.py").read()
    assert b_inst.has_been_run


def test_cmdclass_sdist(tmpdir):
    class Sdist:
        def make_release_tree(self, base_dir, files):
            tmpdir.mkdir("tst")
            self.run_with_args = (base_dir, files)

    cmdclass = get_cmdclass(sdist=Sdist)

    b_inst = cmdclass["sdist"]()
    b_inst.distribution = Mock(packages=["tst"])

    b_inst.make_release_tree(tmpdir, [])
    expected = "__version__ = '%s'\n" % versiongit.__version__
    assert expected == tmpdir.join("tst", "_version_static.py").read()
    assert b_inst.run_with_args == (tmpdir, [])


def test_no_command_args():
    with patch("sys.argv", [sys.argv[0]]):
        with pytest.raises(AssertionError) as excinfo:
            main()
    assert "Expected a python package directory, got None" == str(excinfo.value)


def test_command_version(capsys):
    with patch("sys.argv", [sys.argv[0], "--version"]):
        main()
    out, err = capsys.readouterr()
    assert not err
    assert out.strip() == versiongit.__version__


def test_command_add_blank(capsys, tmpdir):
    with patch("sys.argv", [sys.argv[0], str(tmpdir.mkdir("pkg"))]):
        main()
    lines = tmpdir.join("pkg", "_version_git.py").read().splitlines()
    assert lines[3].startswith("# versiongit-%s" % versiongit.__version__)
    out, err = capsys.readouterr()
    assert not err
    assert (
        out
        == """Added %(d)s/pkg/_version_git.py

Please add the following snippet to %(d)s/pkg/__init__.py:
--------------------------------------------------------------------------------
try:
    # In a release there will be a static version file written by setup.py
    from ._version_static import __version__  # type: ignore
except ImportError:
    # Otherwise get the release number from git describe
    from ._version_git import __version__
--------------------------------------------------------------------------------

Please add the following snippet to %(d)s/.gitattributes:
--------------------------------------------------------------------------------
*/_version_git.py export-subst
--------------------------------------------------------------------------------

Please add the following snippet to %(d)s/setup.py:
--------------------------------------------------------------------------------
# Place the directory containing _version_git on the path
for path, _, filenames in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "_version_git.py" in filenames:
        sys.path.append(path)
        break

from _version_git import get_cmdclass, __version__

setup(
    cmdclass=get_cmdclass(),
    version=__version__
)
--------------------------------------------------------------------------------

"""
        % dict(d=tmpdir)
    )


def test_command_update(capsys, tmpdir):
    pkg_dir = tmpdir.mkdir("pkg")
    pkg_dir.join("_version_git.py").write(
        """
Something that will be overwritten
"""
    )
    pkg_dir.join("__init__.py").write(
        """
# This is a file we wrote
try:
    # In a release there will be a static version file written by setup.py
    from ._version_static import __version__  # type: ignore
except ImportError:
    # Otherwise get the release number from git describe
    from ._version_git import __version__
from blah import stuff
"""
    )
    tmpdir.join(".gitattributes").write(
        """
* module-contact=fedid
*/_version_git.py export-subst
* something-else
"""
    )
    tmpdir.join("setup.py").write(
        """
import sys
import os
from setuptools import setup

import pytest

# Place the directory containing _version_git on the path
for path, _, filenames in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "_version_git.py" in filenames:
        sys.path.append(path)
        break

from _version_git import get_cmdclass, __version__

# Setup information is stored in setup.cfg but this function call
# is still necessary.
setup(
    cmdclass=get_cmdclass(),
    install_requires=["mock"],
    version=__version__,
    extra=1,
)
"""
    )
    with patch("sys.argv", [sys.argv[0], str(pkg_dir)]):
        main()
    lines = tmpdir.join("pkg", "_version_git.py").read().splitlines()
    assert lines[3].startswith("# versiongit-%s" % versiongit.__version__)
    out, err = capsys.readouterr()
    assert not err
    assert out == "Added %s/_version_git.py\n\n" % pkg_dir
