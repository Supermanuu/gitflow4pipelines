#!/usr/bin/env python3

import unittest # The test framework
import projectName # The code to test


class Test_getProjectName(unittest.TestCase):
    def test_get(self):
        self.assertEqual(projectName.getProjectName(), 'versionContainer')


if __name__ == '__main__':
    unittest.main()
