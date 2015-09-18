import unittest

from gitversionbuilder import versioninfo


class VersionInfoTest(unittest.TestCase):
    def test_equals(self):
        self.assertEqual(versioninfo.VersionInfo("v1.6.0", 20, "23fa", True),
                         versioninfo.VersionInfo("v1.6.0", 20, "23fa", True))

    def test_not_equals_tag(self):
        self.assertNotEqual(versioninfo.VersionInfo("v1.6.0", 20, "23fa", True),
                            versioninfo.VersionInfo("v1.6.1", 20, "23fa", True))

    def test_not_equals_commits_since_tag(self):
        self.assertNotEqual(versioninfo.VersionInfo("v1.6.1", 20, "23fa", True),
                            versioninfo.VersionInfo("v1.6.1", 21, "23fa", True))

    def test_not_equals_commit_id(self):
        self.assertNotEqual(versioninfo.VersionInfo("v1.6.1", 20, "23fa", True),
                            versioninfo.VersionInfo("v1.6.1", 20, "23fb", True))

    def test_not_equals_is_tag(self):
        self.assertNotEqual(versioninfo.VersionInfo("v1.6.1", 20, "23fa", True),
                            versioninfo.VersionInfo("v1.6.1", 20, "23fa", False))

    def test_version_string(self):
        self.assertEqual("v1.5-2-g23fa", versioninfo.VersionInfo("v1.5", 2, "23fa", True).version_string)

    def test_version_string_for_tag(self):
        self.assertEqual("v1.5", versioninfo.VersionInfo("v1.5", 0, "23fa", True).version_string)

    def test_parse_simple(self):
        obj = versioninfo.parse("v1.6-0-g3f2a", True)
        self.assertEqual(versioninfo.VersionInfo("v1.6", 0, "3f2a", True), obj)

    def test_parse_with_commits_since_tag(self):
        obj = versioninfo.parse("v1.6.3-23-g49302", True)
        self.assertEqual(versioninfo.VersionInfo("v1.6.3", 23, "49302", True), obj)

    def test_parse_with_dashes_in_tag(self):
        obj = versioninfo.parse("v1.6.3-23-20-gfade", True)
        self.assertEqual(versioninfo.VersionInfo("v1.6.3-23", 20, "fade", True), obj)

    def test_parse_with_slashes_in_tag(self):
        obj = versioninfo.parse("/heads/develop-20-gfade", False)
        self.assertEqual(versioninfo.VersionInfo("/heads/develop", 20, "fade", False), obj)

    def test_parse_missing_tag(self):
        self.assertRaises(versioninfo.VersionParseError, versioninfo.parse, "23-gfade", True)

    def test_parse_empty_tag(self):
        self.assertRaises(versioninfo.VersionParseError, versioninfo.parse, "-23-gfade", True)

    def test_parse_missing_commits_since_tag(self):
        self.assertRaises(versioninfo.VersionParseError, versioninfo.parse, "v2.3-gfade", True)

    def test_parse_empty_commits_since_tag(self):
        self.assertRaises(versioninfo.VersionParseError, versioninfo.parse, "v2.3--gfade", True)

    def test_parse_commits_since_tag_not_int(self):
        self.assertRaises(versioninfo.VersionParseError, versioninfo.parse, "v2.3-a2-gfade", True)

    def test_parse_missing_commit_id(self):
        self.assertRaises(versioninfo.VersionParseError, versioninfo.parse, "v2.3-20", True)

    def test_parse_empty_commit_id(self):
        self.assertRaises(versioninfo.VersionParseError, versioninfo.parse, "v2.3-20-", True)


if __name__ == '__main__':
    unittest.main()
