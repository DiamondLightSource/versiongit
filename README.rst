VersionGit
==========

|build_status| |coverage| |pypi_version| |readthedocs|

VersionGit is a tool for managing the version number of Python modules, removing
the need to update an embedded version string whenever a Git tag is made, and
providing sensible development version numbers too. It does this by storing a
single file in the source repo that reads the version from ``git describe`` or
``git archive`` keywords. At build time, a second file will be created that
contains a static version number to be used in preference to this. This tool is
inspired by versioneer_, but has a vastly reduced feature set so that the code
stored in each module is minimal.

Documentation
-------------

Full documentation is available at http://versiongit.readthedocs.org

Source Code
-----------

Available from https://github.com/dls-controls/versiongit

Installation
------------
To install the latest release, type::

    pip install versiongit

Changelog
---------

See CHANGELOG_

Contributing
------------

See CONTRIBUTING_

License
-------
To make VersionGit easier to embed, all its code is dedicated to the public
domain. The `_version_git.py` that it creates is also in the public domain.
Specifically, both are released under the Creative Commons
"Public Domain Dedication" license (CC0-1.0), as described in LICENSE_

.. |build_status| image:: https://travis-ci.org/dls-controls/versiongit.svg?branch=master
    :target: https://travis-ci.org/dls-controls/versiongit
    :alt: Build Status

.. |coverage| image:: https://codecov.io/gh/dls-controls/versiongit/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dls-controls/versiongit
    :alt: Test coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/versiongit.svg
    :target: https://pypi.python.org/pypi/versiongit
    :alt: Latest PyPI version

.. |readthedocs| image:: https://readthedocs.org/projects/versiongit/badge/?version=latest
    :target: http://versiongit.readthedocs.org
    :alt: Documentation

.. _versioneer:
    https://github.com/warner/python-versioneer

.. _CHANGELOG:
    https://github.com/dls-controls/versiongit/blob/master/CHANGELOG.rst

.. _CONTRIBUTING:
    https://github.com/dls-controls/versiongit/blob/master/CONTRIBUTING.rst

.. _LICENSE:
    https://github.com/dls-controls/versiongit/blob/master/LICENSE
