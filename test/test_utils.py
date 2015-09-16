from tempfile import NamedTemporaryFile
import os

class CodeAsserts:
    def assertCodeEqual(self, expected, actual):
        self.assertEqual(self._normalize(expected), self._normalize(actual))

    def _normalize(self, string):
        lines = string.splitlines()
        normalized_lines = map(self._normalize_line, lines)
        without_empty_lines = filter(None, normalized_lines)
        return "\n".join(without_empty_lines)

    def _normalize_line(self, line):
        tokens = line.split()
        return " ".join(tokens)



class TempFile:
    def __enter__(self):
        f = NamedTemporaryFile()
        f.close() # This also deletes the file
        self.filename = f.name
        return f.name

    def __exit__(self, type, value, tb):
        os.remove(self.filename)
