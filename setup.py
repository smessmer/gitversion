#!/usr/bin/env python

from setuptools import setup
from gitversionbuilder import main

main.create_version_file(git_directory=".", output_file="Version.py", lang="python")
version = main.get_version(git_directory=".")

setup(name='git-version-builder',
      version=version.version_string,
      description='Create a source file containing git version information.',
      author='Sebastian Messmer',
      author_email='heinzisoft@web.de',
      license='GPLv3',
      url='https://github.com/smessmer/git-version-builder',
      py_modules=['Version'],
      packages=['gitversionbuilder'],
      tests_require=['tempdir'],
      test_suite='test'
      )
