#!/usr/bin/env python

from setuptools import setup
from gitversionbuilder import main

main.create_version_file(git_directory=".", output_file="Version.py", lang="python")
version = main.get_version(git_directory=".")

setup(name='gitversion',
      version=version.version_string,
      description='Make git version information (e.g. git tag name, git commit id, ...) available to your source files. A simple use case scenario is to output this version information when the application is called with "--version".',
      author='Sebastian Messmer',
      author_email='heinzisoft@web.de',
      license='GPLv3',
      url='https://github.com/smessmer/gitversion',
      py_modules=['Version'],
      packages=['gitversionbuilder'],
      tests_require=['tempdir'],
      test_suite='test'
      )
