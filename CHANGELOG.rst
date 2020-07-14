Change Log
==========
All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`_.


Unreleased_
-----------

Nothing yet


1.0_ - 2020-07-14
-----------------

- Only match tags of format [0-9]*[-.][0-9]* (E.g. 1.2.3b3)
- Untagged version now starts with 0.0+ rather than 0+


0.6_ - 2020-02-20
-----------------

- Remove -C argument from git command to support git 1.8 onwards
- Print the git error to stderr if the git command fails


0.5_ - 2020-02-19
-----------------

- Change commandline tool to be called ``versiongit`` rather than
  ``version-git``
- Tweak version numbers to match versioneer


0.4_ - 2020-02-19
-----------------

- Put the static version and sha1 in GIT_REFS and GIT_SHA1 rather than writing
  _version_static.py


0.3_ - 2020-02-18
-----------------

- Exclude tests package from release


0.2_ - 2020-02-18
-----------------

- Added support for git archive output
- Added git_error and git_sha1 variables for debugging
- Lots of internal build changes


0.1 - 2019-09-20
----------------

- Initial release

.. _Unreleased: https://github.com/dls-controls/versiongit/compare/1.0...HEAD
.. _1.0: https://github.com/dls-controls/versiongit/compare/0.6...1.0
.. _0.6: https://github.com/dls-controls/versiongit/compare/0.5...0.6
.. _0.5: https://github.com/dls-controls/versiongit/compare/0.4...0.5
.. _0.4: https://github.com/dls-controls/versiongit/compare/0.3...0.4
.. _0.3: https://github.com/dls-controls/versiongit/compare/0.2...0.3
.. _0.2: https://github.com/dls-controls/versiongit/compare/0.1...0.2
