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
        self.assertEqual("v1.5-dev2-23fa", versioninfo.VersionInfo("v1.5", 2, "23fa", True).version_string)

    def test_version_string_for_tag(self):
        self.assertEqual("v1.5", versioninfo.VersionInfo("v1.5", 0, "23fa", True).version_string)

    def test_version_string_with_no_tag(self):
        self.assertEqual("dev2-23fa", versioninfo.VersionInfo("develop", 2, "23fa", False).version_string)


if __name__ == '__main__':
    unittest.main()
