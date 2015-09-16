import unittest
import VersionInfo
import VersionInfoOutputter


class VersionInfoOutputterTest(unittest.TestCase):
    def test_output_cpp(self):
        expected = """
                    #pragma once
                    #ifndef __GITVERSIONBUILDER__VERSION_H__
                    #define __GITVERSIONBUILDER__VERSION_H__

                    namespace version {
                        constexpr const char *versionString = "v1.6-2-g230a";
                        constexpr const char *tagName = "v1.6";
                        constexpr const unsigned int commitsSinceTag = 2;
                        constexpr const char *gitCommitId = "230a";
                    }

                    #endif
                """
        actual = VersionInfoOutputter.to_cpp(VersionInfo.VersionInfo("v1.6", 2, "230a"))
        self.assertEqual(self._normalize(expected), self._normalize(actual))

    def _normalize(self, string):
        lines = string.splitlines()
        normalized_lines = map(self._normalize_line, lines)
        without_empty_lines = filter(None, normalized_lines)
        return "\n".join(without_empty_lines)

    def _normalize_line(self, line):
        tokens = line.split()
        return " ".join(tokens)


if __name__ == '__main__':
    unittest.main()
