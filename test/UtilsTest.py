import unittest
import os
from gitversionbuilder import Utils


class UtilsTest(unittest.TestCase):
    def test_chdir_to_root(self):
        curdir = os.getcwd()
        with Utils.ChDir('/'):
            self.assertEquals('/', os.getcwd())
        self.assertEquals(curdir, os.getcwd())

    def test_chdir_to_parent(self):
        curdir = os.getcwd()
        with Utils.ChDir('..'):
            self.assertEquals(os.path.abspath(os.path.join(curdir, '..')), os.getcwd())
        self.assertEquals(curdir, os.getcwd())


if __name__ == '__main__':
    unittest.main()
