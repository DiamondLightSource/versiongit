VersionGit
==========

VersionGit is a tool for managing the version number of Python modules, removing
the need to update an embedded version string whenever a Git tag is made, and
providing sensible development version numbers too. It does this by storing a
single file in the source repo that reads the version from ``git describe`` or
``git archive`` keywords. At build time, this file is modified in the
distribution to contain a static version number to be used in preference to
this. This tool is inspired by versioneer_, but has a vastly reduced feature set
so that the code stored in each module is minimal.

How it works
------------

The commandline ``versiongit`` tool can be used to place a ``_version_git.py``
in your repository. This produces a sensible PEP440 compliant version number
accessible as ``yourmodule.__version__``. The two ways it gets this information
are documented below.

From Git
~~~~~~~~

At development time when running from a Git repository, the ``git describe``
command is used to work out the version number of the module. If the module
is on a tag, the version name will just be the tag name, otherwise it will
be suffixed with the number of commits since a tag and the sha1. This
``__version__`` variable can then be imported into your module namespace with
a ``from _version_git import __version__`` statement in the top level
``__init__.py``:

.. digraph:: from_git

    bgcolor=transparent
    node [fontname=Arial fontsize=10 shape=box style=filled fillcolor="#f54d27"]
    edge [fontname=Arial fontsize=10 arrowhead=vee]

    vgv [label="yourmodule._version_git.__version__"]
    vg [label="yourmodule._version_git.get_version_from_git"]
    Git
    v [label="yourmodule.__version__"]

    vgv -> vg [label="get_version_from_git()"]
    vg -> Git [label="describe --tags ..."]
    Git -> vg [label="0.1-3-gabc1234"]
    vg -> vgv [label="0.1+3.abc1234"]
    vgv -> v [label="0.1+3.abc1234"]

Static Version
~~~~~~~~~~~~~~

There are two times when we can't get the version number from git:

1) When running from a source archive produced by a ``git archive`` command
2) When running from an installed sdist, egg or wheel

To handle the first case, ``_version_git.py`` contains a ``GIT_REFS`` variable
that will be substituted by the ``git archive`` command. This will contain the
tag name among other things.

For the second case, ``_version_git.py`` contains some command classes that can
be used in ``setup.py`` when creating an ``sdist``, ``bidst_egg`` or
``bdist_wheel``. These command classes substitute the ``GIT_REFS`` variable in
the distribution, replacing it with the static version from Git.

Both cases produce a ``_version_git.py`` that computes the version number from
``GIT_REFS`` rather than from a ``git`` command:

.. digraph:: static_version

    bgcolor=transparent
    node [fontname=Arial fontsize=10 shape=box style=filled fillcolor="#f54d27"]
    edge [fontname=Arial fontsize=10 arrowhead=vee]

    vgv [label="yourmodule._version_git.__version__"]
    vga [label="yourmodule._version_git.GIT_REFS"]
    vg [label="yourmodule._version_git.get_version_from_git"]
    v [label="yourmodule.__version__"]

    vgv -> vg [label="get_version_from_git()"]
    vga -> vg [label="tag: 0.1"]
    vg -> vgv [label="0.1"]
    vgv -> v [label="0.1"]


Usage
-----

To install the latest release, type::

    pip install versiongit

You can then use the commandline ``versiongit`` tool to install a
``_version_git.py`` into the python module you wish to version::

    versiongit repo/modulename

This will create ``repo/modulename/_version_git.py`` and tell you what to put in
``repo/setup.py``, ``repo/modulename/__init__.py`` and ``repo/.gitattributes``
to make it work


Version Numbers
---------------

Version numbers are taken from the git tag. These tags must be of the format
[0-9]*[-.][0-9]* and dashes will be converted to dots. E.g.:

- 0.1
- 4.3b3
- 3-4 (converted to 3.4)

Tags not of this format will be ignored.

Version numbers are of the formats:

=========================== =============================
Version Number              Meaning
=========================== =============================
TAG                         On a git tag, so is a released version TAG
TAG+DISTANCE.gHASH[.dirty]  DISTANCE commits since released version TAG, with
                            the last commit being HASH. If dirty, then
                            uncommitted changes have been made to the source tree
0.0+untagged.gHASH[.dirty]  Cannot find a previous tag. The last commit is HASH.
                            If dirty, then there are uncommitted changes
0.0+unknown                 Cannot determine version from git
=========================== =============================

.. _versioneer:
    https://github.com/warner/python-versioneer
