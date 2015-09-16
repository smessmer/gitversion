#!/usr/bin/env python

import VersionInfoReader
import VersionInfoOutputter


def main():
    version_info = VersionInfoReader.from_git()
    print VersionInfoOutputter.to_cpp(version_info)


if __name__ == '__main__':
    main()
