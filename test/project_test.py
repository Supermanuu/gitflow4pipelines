#!/usr/bin/env python3

import unittest # The test framework
import project # The code to test


class Test_get_name(unittest.TestCase):
    def test_get(self):
        self.assertEqual(project.get_name(), 'versionContainer')


class Test_get_url(unittest.TestCase):
    def test_get(self):
        self.assertEqual(project.get_url(), 'git@ssh.dev.azure.com:v3/POSITIONERS/Tools/versionContainer')


if __name__ == '__main__':
    unittest.main()
