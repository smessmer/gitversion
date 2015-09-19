from tempfile import NamedTemporaryFile, mkdtemp
import os
import shutil
import subprocess
import random
import string
from gitversionbuilder.utils import ChDir

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
        if os.path.isfile(self.filename):
            os.remove(self.filename)


class GitDir:
    def __enter__(self):
        self.dir = mkdtemp()
        return self

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.dir)

    def setup_git_return_commit_id(self):
        with ChDir(self.dir):
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(["git", "init"], stdout=devnull)
                subprocess.check_call(["git", "config", "user.email", "you@example.com"]);
                subprocess.check_call(["git", "config", "user.name", "Your Name"]);
                return self.create_git_commit()

    def create_git_commit(self):
        filename = self._random_string(10)
        with ChDir(self.dir):
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(["touch", filename], stdout=devnull)
                subprocess.check_call(["git", "add", filename], stdout=devnull)
                subprocess.check_call(["git", "commit", "-m", "message"], stdout=devnull)
                commit_id = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
                return commit_id

    def _random_string(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def create_git_tag(self, tag_name):
        with ChDir(self.dir):
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(["git", "tag", tag_name], stdout=devnull)
