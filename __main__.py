#!/usr/bin/env python

import argparse

import Version
from gitversionbuilder import Main


def main():
    parser = argparse.ArgumentParser(description="Create a source file containing git version information.")
    parser.add_argument('--version', action='version', version=Version.VERSION_STRING)
    parser.add_argument('--lang', choices=['cpp', 'python'], required=True)
    parser.add_argument('file')
    args = parser.parse_args()

    Main.create_version_file(output_file=args.file, lang=args.lang)


if __name__ == '__main__':
    main()
