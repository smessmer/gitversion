import subprocess
import os
import re
import utils
import versioninfo


def from_git(git_directory):
    with utils.ChDir(git_directory):
        try:
            with open(os.devnull, 'w') as devnull:
                version_string = subprocess.check_output(["git", "describe", "--tags", "--long", "--abbrev=7"],
                                                         stderr=devnull)
            return _parse_git_version(version_string)
        except subprocess.CalledProcessError:
            # If there is no git tag, then the commits_since_tag returned by git is wrong
            # (because they consider the branch HEAD the tag and there are 0 commits since the branch head).
            # We want to return the total number of commits in the branch if there is no tag.
            total_num_commits = _total_number_of_commits_in_cwd()
            if total_num_commits > 0:
                branch_name = _branch_name_in_cwd()
                commit_id = _commit_id_in_cwd()
                return versioninfo.VersionInfo(git_tag_name=branch_name,
                                               git_commits_since_tag=total_num_commits,
                                               git_commit_id=commit_id,
                                               git_tag_exists=False)
            else:
                branch_name = "HEAD"
                commit_id = "0"
                return versioninfo.VersionInfo(git_tag_name=branch_name,
                                               git_commits_since_tag=total_num_commits,
                                               git_commit_id=commit_id,
                                               git_tag_exists=False)


def _total_number_of_commits_in_cwd():
    try:
        with open('/dev/null', 'w') as devnull:
            return int(subprocess.check_output(["git", "rev-list", "HEAD", "--count"], stderr=devnull))
    except subprocess.CalledProcessError:
        return 0


def _branch_name_in_cwd():
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()


def _commit_id_in_cwd():
    return subprocess.check_output(["git", "log", "--format=%h", "-n", "1"]).strip()


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


def _parse_git_version(git_version_string):
    matched = re.match("^([a-zA-Z0-9\.\-/]+)-([0-9]+)-g([0-9a-f]+)$", git_version_string)
    if matched:
        tag = matched.group(1)
        commits_since_tag = int(matched.group(2))
        commit_id = matched.group(3)
        return versioninfo.VersionInfo(git_tag_name=tag, git_commits_since_tag=commits_since_tag,
                                       git_commit_id=commit_id, git_tag_exists=True)
    else:
        raise VersionParseError(git_version_string)
