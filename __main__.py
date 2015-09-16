#!/usr/bin/env python

import argparse

from gitversionbuilder import main

try:
    Version = __import__("Version")
except ImportError:
    Version = __import__("DummyVersion")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a source file containing git version information.")
    parser.add_argument('--version', action='version', version=Version.VERSION_STRING)
    parser.add_argument('--lang', choices=['cpp', 'python'], required=True)
    parser.add_argument('--dir', default='.')
    parser.add_argument('file')
    args = parser.parse_args()

    main.create_version_file(git_directory=args.dir, output_file=args.file, lang=args.lang)
