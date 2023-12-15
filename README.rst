VersionGit
==========

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

.. warning::

    This has been deprecated in favour of setuptools_scm and is no longer maintained

VersionGit is a tool for managing the version number of Python modules, removing
the need to update an embedded version string whenever a Git tag is made, and
providing sensible development version numbers too. It does this by storing a
single file in the source repo that reads the version from ``git describe`` or
``git archive`` keywords. At build time, this file is modified in the
distribution to contain a static version number to be used in preference to
this. This tool is inspired by versioneer_, but has a vastly reduced feature set
so that the code stored in each module is minimal.

.. _versioneer:
    https://github.com/warner/python-versioneer

============== ==============================================================
PyPI           ``pip install versiongit``
Source code    https://github.com/dls-controls/versiongit
Documentation  https://dls-controls.github.io/versiongit
Changelog      https://github.com/dls-controls/versiongit/blob/master/CHANGELOG.rst
============== ==============================================================

License
-------
To make VersionGit easier to embed, all its code is dedicated to the public
domain. The ``_version_git.py`` that it creates is also in the public domain.
Specifically, both are released under the Creative Commons
"Public Domain Dedication" license (CC0-1.0)

.. |code_ci| image:: https://github.com/dls-controls/versiongit/workflows/Code%20CI/badge.svg?branch=master
    :target: https://github.com/dls-controls/versiongit/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/dls-controls/versiongit/workflows/Docs%20CI/badge.svg?branch=master
    :target: https://github.com/dls-controls/versiongit/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/dls-controls/versiongit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dls-controls/versiongit
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/versiongit.svg
    :target: https://pypi.org/project/versiongit
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-CC0%201.0-blue.svg
    :target: https://creativecommons.org/publicdomain/zero/1.0/
    :alt: CC0-1.0 License

..
    These definitions are used when viewing README.rst and will be replaced
    when included in index.rst

See https://dls-controls.github.io/versiongit for more detailed documentation.
