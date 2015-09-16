#!/usr/bin/env python

from distutils.core import setup
from gitversionbuilder import Main
from distutils.command.bdist_dumb import bdist_dumb


# This class takes care that the files are added in top level to the zip file, not in a subdir
class custom_bdist_dumb(bdist_dumb):
    def reinitialize_command(self, name, **kw):
        cmd = bdist_dumb.reinitialize_command(self, name, **kw)
        if name == 'install':
            cmd.install_lib = '/'
        return cmd

Main.create_version_file("Version.py", "python")
version = Main.get_version()

setup(name='git-version-builder',
      cmdclass = {'bdist_dumb': custom_bdist_dumb},
      version=version.version_string,
      description='Create a source file containing git version information.',
      author='Sebastian Messmer',
      author_email='heinzisoft@web.de',
      url='https://github.com/smessmer/git-version-builder',
      py_modules=['Version', '__main__'],
      packages=['gitversionbuilder']
      )
