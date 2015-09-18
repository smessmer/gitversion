import subprocess
import os
import re
import utils
import versioninfo


def from_git(git_directory):
    with utils.ChDir(git_directory):
        try:
            with open(os.devnull, 'w') as devnull:
                version_string = subprocess.check_output(["git", "describe", "--tags", "--long", "--abbrev=7"], stderr=devnull)
            return _parse_git_version(version_string, is_tag=True)
        except subprocess.CalledProcessError:
            version_string = subprocess.check_output(["git", "describe", "--all", "--long", "--abbrev=7"])
            return _parse_git_version(_remove_prefix("heads/", version_string), is_tag=False)


def _remove_prefix(prefix, string):
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string


class VersionParseError(Exception):
    def __init__(self, version_string):
        self.version_string = version_string

    def __str__(self):
        return "Version not parseable: %s" % self.version_string


def _parse_git_version(git_version_string, is_tag):
    matched = re.match("^([a-zA-Z0-9\.\-/]+)-([0-9]+)-g([0-9a-f]+)$", git_version_string)
    if matched:
        tag = matched.group(1)
        commits_since_tag = int(matched.group(2))
        commit_id = matched.group(3)
        return versioninfo.VersionInfo(tag, commits_since_tag, commit_id, is_tag)
    else:
        raise VersionParseError(git_version_string)
