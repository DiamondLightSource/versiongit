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

    vgv [label="yourmodule._version_git.__version__"]
    vg [label="yourmodule._version_git.get_version_from_git"]
    Git
    v [label="yourmodule.__version__"]

    vgv -> vg [label="get_version_from_git()"]
    vg -> Git [label="describe --tags ..."]
    Git -> vg [label="0.1-3-gabc1234"]
    vg -> vgv [label="0.1+3.abc1234"]
    vgv -> v [label="0.1+3.abc1234"]

If we were to tag and run ``python setup.py sdist`` or ``bdist_egg`` or
``bdist_wheel`` then ``setup.py`` will use the same ``_version_git.py`` file
to take that version from git describe and place it in a static file in the
output. This can then be installed and used in production, when the version
number will be loaded from the generated ``_version_static.py``:

.. digraph:: production

    bgcolor=transparent
    node [fontname=Arial fontsize=10 shape=box style=filled fillcolor="#f54d27"]
    edge [fontname=Arial fontsize=10 arrowhead=vee]

    vs [label="yourmodule._version_static.__version__"]
    v [label="yourmodule.__version__"]

    vs -> v [label="0.1"]

The final use case is to export a source archive from git and run from that. In
this case, ``_version_git.py`` contains substitutions that will be expanded in
preference to running a git command:

.. digraph:: archive

    bgcolor=transparent
    node [fontname=Arial fontsize=10 shape=box style=filled fillcolor="#f54d27"]
    edge [fontname=Arial fontsize=10 arrowhead=vee]

    vgv [label="yourmodule._version_git.__version__"]
    vga [label="yourmodule._version_git.GIT_ARCHIVE_REF_NAMES"]
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
``_version_git.py``

.. _versioneer:
    https://github.com/warner/python-versioneer
