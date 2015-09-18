from utils import EqualityMixin
import re


class TagInterpretation(EqualityMixin):
    def __init__(self, version_components, version_tag, is_dev_version):
        assert (isinstance(version_components, list))
        assert (all(isinstance(item, str) for item in version_components))
        assert (isinstance(version_tag, str))
        self.version_components = version_components
        self.version_tag = version_tag
        self.is_stable = (not is_dev_version) and self.version_tag in ["", "stable", "final"]

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class VersionInfo(EqualityMixin):
    def __init__(self, git_tag_name, git_commits_since_tag, git_commit_id, git_tag_exists):
        assert (isinstance(git_tag_name, str))
        assert (isinstance(git_commits_since_tag, int))
        assert (isinstance(git_commit_id, str))
        assert (isinstance(git_tag_exists, bool))
        self.git_tag_name = git_tag_name
        self.git_commits_since_tag = git_commits_since_tag
        self.git_commit_id = git_commit_id
        self.git_tag_exists = git_tag_exists
        self.is_dev = (not git_tag_exists) or (git_commits_since_tag != 0)

    def interpret_tag_name(self):
        matched = re.match("^v?([0-9]+(?:\.[0-9]+)*)-?(alpha|beta|(rc|RC)[0-9]|(m|M)[0-9]|stable|final)?$",
                           self.git_tag_name)
        if matched:
            version_components = matched.group(1).split('.')
            version_tag = matched.group(2)
            if version_tag is None:
                version_tag = ""
            return TagInterpretation(version_components, version_tag, self.is_dev)
        else:
            return None

    @property
    def version_string(self):
        if not self.git_tag_exists:
            return "dev%d-%s" % (self.git_commits_since_tag, self.git_commit_id)
        elif self.git_commits_since_tag == 0:
            return self.git_tag_name
        else:
            return "%s-dev%d-%s" % (self.git_tag_name, self.git_commits_since_tag, self.git_commit_id)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
