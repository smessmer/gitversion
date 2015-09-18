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
            return "dev%d-%s" % (self.commits_since_tag, self.commit_id)
        elif self.commits_since_tag == 0:
            return self.tag_name
        else:
            return "%s-dev%d-%s" % (self.tag_name, self.commits_since_tag, self.commit_id)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

