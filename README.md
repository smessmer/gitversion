# git-version
This can be incorporated into your build process. If done so, it creates a source file containing git version information, which can then be used by your application.


Use with biicode
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


Use manually
================

There is a python script in the git-version-builder directory.
To generate a version.h file containing C++ version information, call

    python git-version-builder --lang cpp version.h
