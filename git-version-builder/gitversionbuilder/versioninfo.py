from utils import EqualityMixin


class VersionInfo(EqualityMixin):
    def __init__(self, git_tag_name, git_commits_since_tag, git_commit_id, git_tag_exists):
        assert(isinstance(git_tag_name, str))
        assert(isinstance(git_commits_since_tag, int))
        assert(isinstance(git_commit_id, str))
        assert(isinstance(git_tag_exists, bool))
        self.git_tag_name = git_tag_name
        self.git_commits_since_tag = git_commits_since_tag
        self.git_commit_id = git_commit_id
        self.git_tag_exists = git_tag_exists

    #def tag

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

