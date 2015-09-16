import re
from utils import EqualityMixin


class VersionInfo(EqualityMixin):
    def __init__(self, tag_name, commits_since_tag, commit_id, is_tag):
        assert(isinstance(tag_name, str))
        assert(isinstance(commits_since_tag, int))
        assert(isinstance(commit_id, str))
        assert(isinstance(is_tag, bool))
        self.tag_name = tag_name
        self.commits_since_tag = commits_since_tag
        self.commit_id = commit_id
        self.is_tag = is_tag

    @property
    def version_string(self):
        if not self.is_tag:
            return "%s-g%s" % (self.tag_name, self.commit_id)
        elif self.is_tag and self.commits_since_tag == 0:
            return self.tag_name
        else:
            return "%s-%d-g%s" % (self.tag_name, self.commits_since_tag, self.commit_id)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class VersionParseError(Exception):
    def __init__(self, version_string):
        self.version_string = version_string

    def __str__(self):
        return "Version not parseable: %s" % self.version_string


def parse(git_version_string, is_tag):
    matched = re.match("^([a-zA-Z0-9\.\-/]+)-([0-9]+)-g([0-9a-f]+)$", git_version_string)
    if matched:
        tag = matched.group(1)
        commits_since_tag = int(matched.group(2))
        commit_id = matched.group(3)
        return VersionInfo(tag, commits_since_tag, commit_id, is_tag)
    else:
        raise VersionParseError(git_version_string)
