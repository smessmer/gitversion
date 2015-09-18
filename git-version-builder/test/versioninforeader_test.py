import unittest

from gitversionbuilder import versioninfo, versioninforeader
import test_utils


class VersionInfoReaderTest(unittest.TestCase, test_utils.CodeAsserts):
    def test_parse_git_version_simple(self):
        obj = versioninforeader._parse_git_version("v1.6-0-g3f2a", True)
        self.assertEqual(versioninfo.VersionInfo("v1.6", 0, "3f2a", True), obj)

    def test_parse_git_version_with_commits_since_tag(self):
        obj = versioninforeader._parse_git_version("v1.6.3-23-g49302", True)
        self.assertEqual(versioninfo.VersionInfo("v1.6.3", 23, "49302", True), obj)

    def test_parse_git_version_with_dashes_in_tag(self):
        obj = versioninforeader._parse_git_version("v1.6.3-23-20-gfade", True)
        self.assertEqual(versioninfo.VersionInfo("v1.6.3-23", 20, "fade", True), obj)

    def test_parse_git_version_with_slashes_in_tag(self):
        obj = versioninforeader._parse_git_version("/heads/develop-20-gfade", False)
        self.assertEqual(versioninfo.VersionInfo("/heads/develop", 20, "fade", False), obj)

    def test_parse_git_version_missing_tag(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "23-gfade", True)

    def test_parse_git_version_empty_tag(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "-23-gfade", True)

    def test_parse_git_version_missing_commits_since_tag(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3-gfade", True)

    def test_parse_git_version_empty_commits_since_tag(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3--gfade", True)

    def test_parse_git_version_commits_since_tag_not_int(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3-a2-gfade", True)

    def test_parse_git_version_missing_commit_id(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3-20", True)

    def test_parse_git_version_empty_commit_id(self):
        self.assertRaises(versioninforeader.VersionParseError, versioninforeader._parse_git_version, "v2.3-20-", True)


if __name__ == '__main__':
    unittest.main()
