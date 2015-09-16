import subprocess
import os
import utils
import versioninfo


def from_git(git_directory):
    with utils.ChDir(git_directory):
        try:
            with open(os.devnull, 'w') as devnull:
                version_string = subprocess.check_output(["git", "describe", "--tags", "--long", "--abbrev=4"], stderr=devnull)
            return versioninfo.parse(version_string, is_tag=True)
        except subprocess.CalledProcessError:
            version_string = subprocess.check_output(["git", "describe", "--all", "--long", "--abbrev=7"])
            return versioninfo.parse(_remove_prefix("heads/", version_string), is_tag=False)


def _remove_prefix(prefix, string):
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string
