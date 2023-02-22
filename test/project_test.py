#!/usr/bin/env python

import unittest # The test framework
import project # The code to test


class Test_get_name(unittest.TestCase):
    def test_get(self):
        self.assertEqual(project.get_name(), 'versionContainer')
    
    def test_get_suffix1(self):
        self.assertEqual(project.get_name('rrrrrrrl'), 'versionContainerrrrrrrrl')

    def test_get_suffix2(self):
        self.assertEqual(project.get_name('_lolaso'), 'versionContainer_lolaso')

    def test_get_suffix3(self):
        self.assertEqual(project.get_name('+awesome_incredibile-okay'), 'versionContainer+awesome_incredibile-okay')


class Test_get_url(unittest.TestCase):
    def test_get(self):
        self.assertEqual(project.get_url(), 'git@ssh.dev.azure.com:v3/POSITIONERS/Tools/versionContainer')


if __name__ == '__main__':
    unittest.main()
