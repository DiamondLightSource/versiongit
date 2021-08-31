Installation Tutorial
=====================

.. note::

    For installation inside DLS, please see the internal documentation on
    ``dls-python3`` and ``pipenv``. Although these instructions will work
    inside DLS, they are intended for external use.

    If you want to contribute to the library itself, please follow
    the `contributing` instructions.

Check your version of python
----------------------------

You will need python 3.6 or greater. You can check your version of python by
typing into a terminal::

    python3 --version

Create a virtual environment
----------------------------

It is recommended that you install into a “virtual environment” so this
installation will not interfere with any existing Python software::

    python3 -m venv /path/to/venv
    source /path/to/venv/bin/activate


Installing the library
----------------------

You can now use ``pip`` to install the library::

    python3 -m pip install versiongit

If you require a feature that is not currently released you can also install
from github::

    python3 -m pip install git+git://github.com/dls-controls/versiongit.git

The library should now be installed and the commandline interface on your path.
You can check the version that has been installed by typing::

    versiongit --version


Add VersionGit to your package
------------------------------

You can then use the commandline ``versiongit`` tool to install a
``_version_git.py`` into the python package you wish to version::

    versiongit repo/packagename

This will create ``repo/packagename/_version_git.py`` and tell you what to put in
``repo/setup.py``, ``repo/packagename/__init__.py`` and ``repo/.gitattributes``
to make it work
