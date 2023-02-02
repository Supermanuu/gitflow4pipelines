#!/usr/bin/env python3

import unittest # The test framework
import project # The code to test


class Test_getName(unittest.TestCase):
    def test_get(self):
        self.assertEqual(project.getName(), 'versionContainer')


class Test_getURL(unittest.TestCase):
    def test_get(self):
        self.assertEqual(project.getURL(), 'git@ssh.dev.azure.com:v3/POSITIONERS/Tools/versionContainer')


if __name__ == '__main__':
    unittest.main()
