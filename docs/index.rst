VersionGit
==========

VersionGit is a tool for managing the version number of Python modules, removing
the need to update an embedded version string whenever a Git tag is made, and
providing sensible development version numbers too. It does this by storing a
single file in the source repo that reads the version from ``git describe`` or
``git archive`` keywords. At build time, a second file will be created that
contains a static version number to be used in preference to this. This tool is
inspired by versioneer_, but has a vastly reduced feature set so that the code
stored in each module is minimal.

How it works
------------

The commandline ``versiongit`` tool can be used to place a ``_version_git.py``
in your repository. This can be used at development time to generate a sensible
PEP440 compliant version number accessible as ``yourmodule.__version__``:

.. digraph:: development

    bgcolor=transparent
    node [fontname=Arial fontsize=10 shape=box style=filled fillcolor="#f54d27"]
    edge [fontname=Arial fontsize=10 arrowhead=vee]

    vg [label="yourmodule._version_git"]
    v [label="yourmodule.__version__"]

    vg -> Git [label="describe --tags ..."]
    Git -> vg [label="0.1-3-gabc1234"]
    vg -> v [label="0.1+3.abc1234"]

Usage
-----

To install the latest release, type::

    pip install versiongit

You can then use the commandline ``versiongit`` tool to install a
``_version_git.py``

.. _versioneer:
    https://github.com/warner/python-versioneer
