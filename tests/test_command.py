import sys

import pytest
from mock import patch

import versiongit
from versiongit.command import main


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
    assert lines[10] == 'GIT_SHA1 = "$Format:%h$"'
    out, err = capsys.readouterr()
    assert not err
    assert (
        out
        == """Added %(d)s/pkg/_version_git.py

Please add the following snippet to %(d)s/pkg/__init__.py:
--------------------------------------------------------------------------------
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

from _version_git import __version__, get_cmdclass  # noqa

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

from _version_git import __version__, get_cmdclass  # noqa

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
