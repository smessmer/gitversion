import subprocess
import os
import Utils
import VersionInfo


def from_git(git_directory):
    version_string = _read_git_version_string(git_directory)
    return VersionInfo.parse(version_string)


def _read_git_version_string(git_directory):
    with Utils.ChDir(git_directory):
        try:
            with open(os.devnull, 'w') as devnull:
                return subprocess.check_output(["git", "describe", "--tags", "--long", "--abbrev=4"], stderr=devnull)
        except subprocess.CalledProcessError:
            return subprocess.check_output(["git", "describe", "--all", "--long", "--abbrev=7"])
