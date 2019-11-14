import sys
import os
import setuptools
from distutils.core import setup

# Place the directory containing _version_git on the path
for path, _, filenames in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "_version_git.py" in filenames:
        sys.path.append(path)
        break

from _version_git import get_cmdclass, __version__

# Setup information is stored in setup.cfg but this function call
# is still necessary.
setup(
    cmdclass=get_cmdclass(),
    version=__version__
)
