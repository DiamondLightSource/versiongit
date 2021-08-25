Make a Release
==============

Git tag with a PEP440 compliant version number.

Version numbers are taken from the git tag. These tags must be of the format
[0-9]*[-.][0-9]* and dashes will be converted to dots. E.g.:

- 0.1.6
- 4.3b3
- 3-4 (converted to 3.4)

Tags not of this format will be ignored.

