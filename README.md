# git-version [![Build Status](https://travis-ci.org/smessmer/gitversion.svg?branch=master)](https://travis-ci.org/smessmer/gitversion)
Make git version information (e.g. last tag name, git commit id, ...) available to your source files.

This repository contains
  - a python script to generate C++ headers or python modules with this information. You can include the python script into your build process
  - a biicode block which can be directly included into biicode C++ projects


Use with biicode (only C++)
================

Add the following to your CMakeLists.txt

    INCLUDE(messmer/gitversion/cmake)
    GIT_VERSION_INIT()

Then, you can write in your source file:

    #include <messmer/gitversion/gitversion.h>
    cout << gitversion::VERSION.major() << endl;
    cout << gitversion::VERSION.toString() << endl;
    cout << gitversion::VERSION.isStable() << endl;
    cout << gitversion::VERSION.gitCommitId() << endl;
    // ... (see src/Version.h for more functions)

It will look for the closest git tag and fill the information from there.
It expects your git tag to be of the form

    [major].[minor]{alpha,beta,rc1,}

Valid versions are for example

  - 1.0
  - 1.0alpha
  - 0.8rc1
  - 12.34

Development Versions
-------------------

If the build is not made from the tag, but there are some commits on top of it, then gitversion::VERSION.isDev() will return true and gitversion::VERSION.toString() will contain the number of commits since the tag and a git commit id.
For example

    0.8alpha-dev3-3f4a

means that the last tag was 0.8alpha, there have been 3 commits since, and the current git commit id is 3f4a.

gitversion::VERSION.isStable() will only return true, if it is not a development version (no commits since the last tag), and the last tag is a final tag, not alpha, beta or rc.


Use manually (C++ and Python)
================

There is a python script in the git-version-builder directory.
To generate a version.h file containing C++ version information, call

    python git-version-builder --lang cpp version.h

To generate a python module with the information, call

    python git-version-builder --lang python version.py
