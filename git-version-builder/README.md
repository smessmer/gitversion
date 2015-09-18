# git-version-builder
This can be incorporated into your build process. If done so, it creates a source file containing git version information, which can then be used by your application.

To build a distribution, run

$ python setup.py bdist --format=zip

This zip file can then be run using

$ python file.zip
