import unittest

from gitversionbuilder import versioninforeader
from gitversionbuilder.versioninfo import VersionInfo
from test_utils import GitDir


class ParseGitVersionTest(unittest.TestCase):
    def test_parse_git_version_simple(self):
        obj = versioninforeader._parse_git_version("v1.6-0-g3f2a")
        self.assertEqual(VersionInfo("v1.6", 0, "3f2a", True), obj)

    def test_parse_git_version_with_commits_since_tag(self):
        obj = versioninforeader._parse_git_version("v1.6.3-23-g49302")
        self.assertEqual(VersionInfo("v1.6.3", 23, "49302", True), obj)

    def test_parse_git_version_with_dashes_in_tag(self):
        obj = versioninforeader._parse_git_version("v1.6.3-23-20-gfade")
        self.assertEqual(VersionInfo("v1.6.3-23", 20, "fade", True), obj)

    def test_parse_git_version_with_slashes_in_tag(self):
        obj = versioninforeader._parse_git_version("/heads/develop-20-gfade")
        self.assertEqual(VersionInfo("/heads/develop", 20, "fade", True), obj)

    def test_parse_git_version_missing_tag(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "23-gfade")

    def test_parse_git_version_empty_tag(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "-23-gfade")

    def test_parse_git_version_missing_commits_since_tag(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3-gfade")

    def test_parse_git_version_empty_commits_since_tag(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3--gfade")

    def test_parse_git_version_commits_since_tag_not_int(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3-a2-gfade")

    def test_parse_git_version_missing_commit_id(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3-20")

    def test_parse_git_version_empty_commit_id(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3-20-")


class VersionInfoReaderTest(unittest.TestCase):
    def test_empty(self):
        with GitDir() as dir:
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("HEAD", 0, "0", False), version_info)

    def test_commit(self):
        with GitDir() as dir:
            commit_id = dir.create_git_commit()
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("master", 1, commit_id, False), version_info)

    def test_commit_commit(self):
        with GitDir() as dir:
            dir.create_git_commit()
            commit_id = dir.create_git_commit()
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("master", 2, commit_id, False), version_info)

    def test_commit_tag(self):
        with GitDir() as dir:
            commit_id = dir.create_git_commit()
            dir.create_git_tag("tagname")
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("tagname", 0, commit_id, True), version_info)

    def test_commit_tag_commit(self):
        with GitDir() as dir:
            dir.create_git_commit()
            dir.create_git_tag("tagname")
            commit_id = dir.create_git_commit()
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("tagname", 1, commit_id, True), version_info)

    def test_commit_tag_commit_commit(self):
        with GitDir() as dir:
            dir.create_git_commit()
            dir.create_git_tag("tagname")
            dir.create_git_commit()
            commit_id = dir.create_git_commit()
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("tagname", 2, commit_id, True), version_info)

    def test_commit_tag_commit_tag_commit(self):
        with GitDir() as dir:
            dir.create_git_commit()
            dir.create_git_tag("tagname")
            dir.create_git_commit()
            dir.create_git_tag("mytag2")
            commit_id = dir.create_git_commit()
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("mytag2", 1, commit_id, True), version_info)

    def test_commit_commit_tag_rewind(self):
        with GitDir() as dir:
            dir.create_git_commit()
            commit_id = dir.create_git_commit()
            dir.create_git_commit()
            dir.create_git_tag("tagname")
            dir.checkout_git_commit(commit_id)
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("HEAD", 2, commit_id, False), version_info)

    def test_commit_tag_commit_commit_tag_rewind(self):
        with GitDir() as dir:
            dir.create_git_commit()
            dir.create_git_tag("tagname")
            commit_id = dir.create_git_commit()
            dir.create_git_commit()
            dir.create_git_tag("mytag2")
            dir.checkout_git_commit(commit_id)
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("tagname", 1, commit_id, True), version_info)

    def test_commit_branch(self):
        with GitDir() as dir:
            commit_id = dir.create_git_commit()
            dir.create_git_branch("newbranch")
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("newbranch", 1, commit_id, False), version_info)

    def test_commit_branch_commit(self):
        with GitDir() as dir:
            dir.create_git_commit()
            dir.create_git_branch("newbranch")
            commit_id = dir.create_git_commit()
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("newbranch", 2, commit_id, False), version_info)

    def test_commit_tag_commit_branch_commit(self):
        with GitDir() as dir:
            dir.create_git_commit()
            dir.create_git_tag("mytag")
            dir.create_git_commit()
            dir.create_git_branch("newbranch")
            commit_id = dir.create_git_commit()
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("mytag", 2, commit_id, True), version_info)

    def test_commit_branchedcommit(self):
        with GitDir() as dir:
            commit_id = dir.create_git_commit()
            dir.create_git_branch("newbranch")
            dir.create_git_commit()
            dir.switch_git_branch("master")
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("master", 1, commit_id, False), version_info)

    def test_commit_branchedtaggedcommit(self):
        with GitDir() as dir:
            commit_id = dir.create_git_commit()
            dir.create_git_branch("newbranch")
            dir.create_git_commit()
            dir.create_git_tag("mytag")
            dir.switch_git_branch("master")
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("master", 1, commit_id, False), version_info)

    def test_commit_tag_branchedtaggedcommit(self):
        with GitDir() as dir:
            commit_id = dir.create_git_commit()
            dir.create_git_tag("originaltag")
            dir.create_git_branch("newbranch")
            dir.create_git_commit()
            dir.create_git_tag("newtag")
            dir.switch_git_branch("master")
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("originaltag", 0, commit_id, True), version_info)

    def test_commit_tag_commit_branchedtaggedcommit(self):
        with GitDir() as dir:
            dir.create_git_commit()
            dir.create_git_tag("originaltag")
            commit_id = dir.create_git_commit()
            dir.create_git_branch("newbranch")
            dir.create_git_commit()
            dir.create_git_tag("newtag")
            dir.switch_git_branch("master")
            version_info = versioninforeader.from_git(dir.dir)
            self.assertEqual(VersionInfo("originaltag", 1, commit_id, True), version_info)


if __name__ == '__main__':
    unittest.main()
