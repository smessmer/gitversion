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

    #include <gitversion/version.h>
    cout << version::VERSION_STRING << endl;
    cout << version::IS_STABLE_VERSION << endl;
    cout << version::GIT_COMMIT_ID << endl;
    cout << version::GIT_COMMITS_SINCE_TAG << endl;
    // ... (see below for more variables)


Use manually (C++ and Python)
================

There is a python script in the git-version-builder directory.
To generate a version.h file containing C++ version information, call

    python git-version-builder --lang cpp version.h

To generate a python module with the information, call

    python git-version-builder --lang python version.py


Available Information
=================

Basic Information
-----------------
The following table shows the basic variables that are always available.

<table>
  <tr>
    <th rowspan="4">VERSION_STRING</th>
    <td style="white-space: nowrap;">1.0</td>
    <td>Built from git tag "1.0".</td>
  </tr>
  <tr>
    <td style="white-space: nowrap;">v0.8alpha</td>
    <td>Built from git tag "v0.8alpha".</td>
  </tr>
  <tr>
    <td style="white-space: nowrap;">0.8-dev3-4fa254c
    <td>Built from 3 commits after git tag "0.8". The current git commit has commit id 4fa254c.
  </tr>
  <tr>
    <td style="white-space: nowrap;">dev2-4fa254c</td>
    <td>The repository doesn't have any git tags yet. There are 2 commits since the repository started and the current git commit has commit id 4fa254c.</td>
  </tr>

  <tr>
    <th>GIT_TAG_NAME</th>
    <td colspan="2">The name of the last git tag. If there is no git tag, then this is the name of the git branch.</td>
  </tr>

  <tr>
    <th>GIT_COMMITS_SINCE_TAG</th>
    <td colspan="2">The number of git commits since the last git tag. If the repository doesn't have any git tags, then this is the number of git commits since the repository started</td>
  </tr>

  <tr>
    <th>GIT_COMMIT_ID</th>
    <td colspan="2">The commit id of the git commit this was built from.</td>
  </tr>

  <tr>
    <th>IS_DEV_VERSION</th>
    <td colspan="2">True, if this is a development version; i.e. there are no tags yet or GIT_COMMITS_SINCE_TAG > 0.</td>
  </tr>
</table>

Additional Information
----------------------

We will parse the git tag name and provide additional information if you use the following versioning scheme for your git tag names:

    /^v?[0-9]+(\.[0-9]+)*-?(alpha|beta|(rc|RC)[0-9]|(m|M)[0-9]|stable|final)?$/

In words, we support a set of numeric version components separated by a dot, then optionally a version tag like "alpha", "beta", "rc2", "M3", "stable", "final". The version tag can optionally be separated with a dash and the version number can optionally be prefixed with "v".

Examples for supported version numbers:

   - 0.8.1
   - v3.0
   - 1.1-alpha
   - 1.4.3beta
   - 2.0-M2
   - 4-RC2
   - 3.0final
   - 2.1-stable
   - ...

If you use a version scheme supported by this, we will provide the following additional information

<table>
  <tr>
    <th>IS_STABLE_VERSION</th>
    <td>True, if built from a final tag; i.e. IS_DEV_VERSION==false, GIT_COMMITS_SINCE_TAG == 0 and VERSION_TAG in {"", "stable", "final"}</td>
  </tr>

  <tr>
    <th>VERSION_COMPONENTS</th>
    <td>An array containing the version number split at the dots. That is, git tag "1.02.3alpha" will have VERSION_COMPONENTS=["1","02","3"].</td>
  </tr>

  <tr>
    <th>VERSION_TAG</th>
    <td>The version tag ("alpha", "beta", "rc4", "M2", "stable", "final", "", ...) that follows after the version number. If the version tag is separated by a dash, the dash is not included.</td>
  </tr>
</table>

