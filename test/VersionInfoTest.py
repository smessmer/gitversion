import unittest

from gitversionbuilder import VersionInfo


class VersionInfoTest(unittest.TestCase):
    def test_equals(self):
        self.assertEqual(VersionInfo.VersionInfo("v1.6.0", 20, "23fa"),
                         VersionInfo.VersionInfo("v1.6.0", 20, "23fa"))

    def test_not_equals_tag(self):
        self.assertNotEqual(VersionInfo.VersionInfo("v1.6.0", 20, "23fa"),
                            VersionInfo.VersionInfo("v1.6.1", 20, "23fa"))

    def test_not_equals_commits_since_tag(self):
        self.assertNotEqual(VersionInfo.VersionInfo("v1.6.1", 20, "23fa"),
                            VersionInfo.VersionInfo("v1.6.1", 21, "23fa"))

    def test_not_equals_commit_id(self):
        self.assertNotEqual(VersionInfo.VersionInfo("v1.6.1", 20, "23fa"),
                            VersionInfo.VersionInfo("v1.6.1", 20, "23fb"))

    def test_version_string(self):
        self.assertEqual("v1.5-2-g23fa", VersionInfo.VersionInfo("v1.5", 2, "23fa").version_string)

    def test_parse_simple(self):
        obj = VersionInfo.parse("v1.6-0-g3f2a")
        self.assertEqual(VersionInfo.VersionInfo("v1.6", 0, "3f2a"), obj)

    def test_parse_with_commits_since_tag(self):
        obj = VersionInfo.parse("v1.6.3-23-g49302")
        self.assertEqual(VersionInfo.VersionInfo("v1.6.3", 23, "49302"), obj)

    def test_parse_with_dashes_in_tag(self):
        obj = VersionInfo.parse("v1.6.3-23-20-gfade")
        self.assertEqual(VersionInfo.VersionInfo("v1.6.3-23", 20, "fade"), obj)

    def test_parse_with_slashes_in_tag(self):
        obj = VersionInfo.parse("/head/develop-20-gfade")
        self.assertEqual(VersionInfo.VersionInfo("/head/develop", 20, "fade"), obj)

    def test_parse_missing_tag(self):
        self.assertRaises(VersionInfo.VersionParseError, VersionInfo.parse, "23-gfade")

    def test_parse_empty_tag(self):
        self.assertRaises(VersionInfo.VersionParseError, VersionInfo.parse, "-23-gfade")

    def test_parse_missing_commits_since_tag(self):
        self.assertRaises(VersionInfo.VersionParseError, VersionInfo.parse, "v2.3-gfade")

    def test_parse_empty_commits_since_tag(self):
        self.assertRaises(VersionInfo.VersionParseError, VersionInfo.parse, "v2.3--gfade")

    def test_parse_commits_since_tag_not_int(self):
        self.assertRaises(VersionInfo.VersionParseError, VersionInfo.parse, "v2.3-a2-gfade")

    def test_parse_missing_commit_id(self):
        self.assertRaises(VersionInfo.VersionParseError, VersionInfo.parse, "v2.3-20")

    def test_parse_empty_commit_id(self):
        self.assertRaises(VersionInfo.VersionParseError, VersionInfo.parse, "v2.3-20-")


if __name__ == '__main__':
    unittest.main()
