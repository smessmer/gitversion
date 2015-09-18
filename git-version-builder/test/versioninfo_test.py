import unittest

from gitversionbuilder.versioninfo import VersionInfo, TagInterpretation


class VersionInfoTest(unittest.TestCase):
    def test_equals(self):
        self.assertEqual(VersionInfo("v1.6.0", 20, "23fa", True),
                         VersionInfo("v1.6.0", 20, "23fa", True))

    def test_not_equals_tag(self):
        self.assertNotEqual(VersionInfo("v1.6.0", 20, "23fa", True),
                            VersionInfo("v1.6.1", 20, "23fa", True))

    def test_not_equals_commits_since_tag(self):
        self.assertNotEqual(VersionInfo("v1.6.1", 20, "23fa", True),
                            VersionInfo("v1.6.1", 21, "23fa", True))

    def test_not_equals_commit_id(self):
        self.assertNotEqual(VersionInfo("v1.6.1", 20, "23fa", True),
                            VersionInfo("v1.6.1", 20, "23fb", True))

    def test_not_equals_is_tag(self):
        self.assertNotEqual(VersionInfo("v1.6.1", 20, "23fa", True),
                            VersionInfo("v1.6.1", 20, "23fa", False))

    def test_version_string(self):
        self.assertEqual("v1.5-dev2-23fa", VersionInfo("v1.5", 2, "23fa", True).version_string)

    def test_version_string_for_tag(self):
        self.assertEqual("v1.5", VersionInfo("v1.5", 0, "23fa", True).version_string)

    def test_version_string_with_no_tag(self):
        self.assertEqual("dev2-23fa", VersionInfo("develop", 2, "23fa", False).version_string)

    def test_interpret_valid_tag_name(self):
        self.assertEqual(TagInterpretation(["1"], ""),
                         VersionInfo("1", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_plain(self):
        self.assertEqual(TagInterpretation(["1", "0"], ""),
                         VersionInfo("1.0", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_alpha(self):
        self.assertEqual(TagInterpretation(["1", "0"], "alpha"),
                         VersionInfo("1.0alpha", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_with_dash(self):
        self.assertEqual(TagInterpretation(["1", "02", "3"], "beta"),
                         VersionInfo("1.02.3-beta", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_stable(self):
        self.assertEqual(TagInterpretation(["1", "02"], "stable"),
                         VersionInfo("1.02-stable", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_final(self):
        self.assertEqual(TagInterpretation(["0", "8"], "final"),
                         VersionInfo("0.8final", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_M3(self):
        self.assertEqual(TagInterpretation(["0", "8"], "M3"),
                         VersionInfo("0.8-M3", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_m3(self):
        self.assertEqual(TagInterpretation(["0", "8"], "m3"),
                         VersionInfo("0.8m3", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_rc2(self):
        self.assertEqual(TagInterpretation(["0", "8"], "rc2"),
                         VersionInfo("0.8rc2", 0, "23fa", True).interpret_tag_name())

    def test_interpret_valid_tag_name_RC2(self):
        self.assertEqual(TagInterpretation(["0", "8"], "RC2"),
                         VersionInfo("0.8-RC2", 0, "23fa", True).interpret_tag_name())

    def test_interpret_invalid_tag_name(self):
        self.assertEqual(None, VersionInfo("develop", 0, "23fa", True).interpret_tag_name())

    def test_interpret_invalid_tag_name_invalid_tag(self):
        self.assertEqual(None, VersionInfo("1.0invalid", 0, "23fa", True).interpret_tag_name())

    def test_interpret_invalid_tag_name_invalid_tag_with_dash(self):
        self.assertEqual(None, VersionInfo("1.0-invalid", 0, "23fa", True).interpret_tag_name())

    def test_interpret_invalid_tag_name_invalid_number(self):
        self.assertEqual(None, VersionInfo("develop-alpha", 0, "23fa", True).interpret_tag_name())

    def test_interpret_invalid_tag_name_invalid_component_separator(self):
        self.assertEqual(None, VersionInfo("1,0-alpha", 0, "23fa", True).interpret_tag_name())

    def test_interpret_invalid_tag_name_invalid_missing_component(self):
        self.assertEqual(None, VersionInfo("1,-alpha", 0, "23fa", True).interpret_tag_name())


class TagInterpretationTest(unittest.TestCase):
    def test_equals(self):
        self.assertEqual(TagInterpretation(["1", "2"], "alpha"),
                         TagInterpretation(["1", "2"], "alpha"))

    def test_not_equals_version_tag(self):
        self.assertNotEqual(TagInterpretation(["1", "2"], "beta"),
                            TagInterpretation(["1", "2"], "alpha"))

    def test_not_equals_components_1(self):
        self.assertNotEqual(TagInterpretation(["1"], "alpha"),
                            TagInterpretation(["1", "2"], "alpha"))

    def test_not_equals_components_2(self):
        self.assertNotEqual(TagInterpretation(["1", "3"], "alpha"),
                            TagInterpretation(["1", "2"], "alpha"))


if __name__ == '__main__':
    unittest.main()
