import re
from EqualityMixin import EqualityMixin


class VersionInfo(EqualityMixin):
    def __init__(self, tag_name, commits_since_tag, commit_id):
        assert(isinstance(tag_name, str))
        assert(isinstance(commits_since_tag, int))
        assert(isinstance(commit_id, str))
        self.tag_name = tag_name
        self.commits_since_tag = commits_since_tag
        self.commit_id = commit_id

    @property
    def version_string(self):
        return "%s-%d-g%s" % (self.tag_name, self.commits_since_tag, self.commit_id)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class VersionParseError(Exception):
    def __init__(self, version_string):
        self.version_string = version_string

    def __str__(self):
        return "Version not parseable: %s" % self.version_string


def parse(git_version_string):
    matched = re.match("^([a-zA-Z0-9\.\-/]+)-([0-9]+)-g([0-9a-f]+)$", git_version_string)
    if matched:
        tag = matched.group(1)
        commits_since_tag = int(matched.group(2))
        commit_id = matched.group(3)
        return VersionInfo(tag, commits_since_tag, commit_id)
    else:
        raise VersionParseError(git_version_string)
