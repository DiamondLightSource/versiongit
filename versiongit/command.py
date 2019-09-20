import os
import sys
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(
        description="Command line tool adding versiongit to python module")
    parser.add_argument("--version", action="store_true",
                        help="Print the current version of versiongit")
    args = parser.parse_args()
    if args.version:
        sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
        from versiongit import __version__
        print(__version__)


if __name__ == "__main__":
    main()
