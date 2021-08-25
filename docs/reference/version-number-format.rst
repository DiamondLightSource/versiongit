Version Number Format
=====================

Git tags in the format given by `../how-to/make-a-release` will generate version numbers

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

