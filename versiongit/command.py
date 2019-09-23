import os
import sys
from argparse import ArgumentParser


def main():
    from versiongit import __version__

    parser = ArgumentParser(
        description="Command line tool adding versiongit to python module")
    parser.add_argument("--version", action="store_true",
                        help="Print the current version of versiongit")
    args = parser.parse_args()
    if args.version:
        print(__version__)


if __name__ == "__main__":
    sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
    main()
