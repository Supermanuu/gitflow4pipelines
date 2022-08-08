#!/usr/bin/env python3

import unittest # The test framework
import lastVersion # The code to test

class Test_prettyTag(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(lastVersion.debTag('1.0.0'), '1.0.0')

    def test_revision(self):
        self.assertEqual(lastVersion.debTag('1.0.0.1'), '1:1.0.0')

    def test_revision2(self):
        self.assertEqual(lastVersion.debTag('1.0.0.2'), '2:1.0.0')

    def test_alpanumeric(self):
        self.assertEqual(lastVersion.debTag('1.0.0-lol1'), '1.0.0-lol1')

    def test_alpanumericAndRevision(self):
        self.assertEqual(lastVersion.debTag('1.0.0.1-lol1'), '1:1.0.0-lol1')

    def test_alpanumericAndRevision2(self):
        self.assertEqual(lastVersion.debTag('1.0.0.2-lol1'), '2:1.0.0-lol1')


class Test_organizer(unittest.TestCase):
    def test_format(self):
        self.assertRaises(RuntimeError, lastVersion.organizer, 'dfsf')

    def test_normal(self):
        self.assertEqual(lastVersion.organizer('1.0.0'), [ 1, 0, 0, 0, 0 ])

    def test_revision1(self):
        self.assertEqual(lastVersion.organizer('1.0.0.1'), [ 1, 0, 0, 1, 0 ])

    def test_revision2(self):
        self.assertEqual(lastVersion.organizer('1.0.0.2'), [ 1, 0, 0, 2, 0 ])

    def test_build1(self):
        self.assertEqual(lastVersion.organizer('1.0.0-1'), [ 1, 0, 0, 0, 1 ])
    
    def test_build2(self):
        self.assertEqual(lastVersion.organizer('1.0.0-2'), [ 1, 0, 0, 0, 2 ])

    def test_all(self):
        self.assertEqual(lastVersion.organizer('1.2.3.4-5'), [ 1, 2, 3, 4, 5 ])

    def test_allphanumeric(self):
        self.assertEqual(lastVersion.organizer('1.2.3.4-lol5'), [ 1, 2, 3, 4, 5 ])


class Test_sortTags(unittest.TestCase):
    def test_void(self):
        tags = []
        sort = []
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_normal(self):
        tags = ['1.0.0', '1.0.1', '1.0.10', '1.0.11', '1.0.12', '1.0.13', '1.0.14', '1.0.15', '1.0.16', '1.0.17', '1.0.18', '1.0.19', '1.0.2', '1.0.20', '1.0.21', '1.0.22', '1.0.23', '1.0.24', '1.0.25', '1.0.26', '1.0.3', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.8']
        sort = ['1.0.0', '1.0.1', '1.0.2', '1.0.3', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.8', '1.0.10', '1.0.11', '1.0.12', '1.0.13', '1.0.14', '1.0.15', '1.0.16', '1.0.17', '1.0.18', '1.0.19', '1.0.20', '1.0.21', '1.0.22', '1.0.23', '1.0.24', '1.0.25', '1.0.26']
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_sorted(self):
        tags = ['1.0.0', '1.0.1', '1.0.2', '1.0.3', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.8', '1.0.10', '1.0.11', '1.0.12', '1.0.13', '1.0.14', '1.0.15', '1.0.16', '1.0.17', '1.0.18', '1.0.19', '1.0.20', '1.0.21', '1.0.22', '1.0.23', '1.0.24', '1.0.25', '1.0.26']
        sort = ['1.0.0', '1.0.1', '1.0.2', '1.0.3', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.8', '1.0.10', '1.0.11', '1.0.12', '1.0.13', '1.0.14', '1.0.15', '1.0.16', '1.0.17', '1.0.18', '1.0.19', '1.0.20', '1.0.21', '1.0.22', '1.0.23', '1.0.24', '1.0.25', '1.0.26']
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_missing(self):
        tags = ['1.0.0', '1.0.1', '1.0.10', '1.0.12', '1.0.13', '1.0.14', '1.0.15', '1.0.16', '1.0.17', '1.0.19', '1.0.2', '1.0.20', '1.0.21', '1.0.22', '1.0.24', '1.0.25', '1.0.26', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.8']
        sort = ['1.0.0', '1.0.1', '1.0.2', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.8', '1.0.10', '1.0.12', '1.0.13', '1.0.14', '1.0.15', '1.0.16', '1.0.17', '1.0.19', '1.0.20', '1.0.21', '1.0.22', '1.0.24', '1.0.25', '1.0.26']
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_reverse(self):
        tags = ['1.0.0', '1.0.1', '1.0.2', '1.0.3', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.8', '1.0.10', '1.0.11', '1.0.12', '1.0.13', '1.0.14', '1.0.15', '1.0.16', '1.0.17', '1.0.18', '1.0.19', '1.0.20', '1.0.21', '1.0.22', '1.0.23', '1.0.24', '1.0.25', '1.0.26']
        tags.reverse()
        sort = ['1.0.0', '1.0.1', '1.0.2', '1.0.3', '1.0.4', '1.0.5', '1.0.6', '1.0.7', '1.0.8', '1.0.10', '1.0.11', '1.0.12', '1.0.13', '1.0.14', '1.0.15', '1.0.16', '1.0.17', '1.0.18', '1.0.19', '1.0.20', '1.0.21', '1.0.22', '1.0.23', '1.0.24', '1.0.25', '1.0.26']
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_revision(self):
        tags = ['1.0.2', '1.0.0', '1.0.1', '1.0.4', '1.0.0.1', '1.0.3', '1.0.3.1', '1.0.3.1']
        sort = ['1.0.0', '1.0.0.1', '1.0.1', '1.0.2', '1.0.3', '1.0.3.1', '1.0.3.1', '1.0.4']
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_build(self):
        tags = ['1.0.3-2', '1.0.0', '1.0.1', '1.0.3', '1.0.2', '1.0.3-1', '1.0.0-1', '1.0.4']
        sort = ['1.0.0', '1.0.0-1', '1.0.1', '1.0.2', '1.0.3', '1.0.3-1', '1.0.3-2', '1.0.4']
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_all(self):
        tags = ['1.0.3-2', '1.0.0', '1.0.0.1-1', '1.0.1', '1.0.4.1', '1.0.1.1-1', '1.0.3', '1.0.2', '1.0.0.1', '1.0.3-1', '1.0.0-1', '1.0.4']
        sort = ['1.0.0', '1.0.0-1', '1.0.0.1', '1.0.0.1-1', '1.0.1', '1.0.1.1-1', '1.0.2', '1.0.3', '1.0.3-1', '1.0.3-2', '1.0.4', '1.0.4.1']
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_allpphanumeric(self):
        tags = ['1.0.3-lol2', '1.0.0', '1.0.0.1-lol1', '1.0.1', '1.0.4.1', '1.0.1.1-lol1', '1.0.3', '1.0.2', '1.0.0.1', '1.0.3-lol1', '1.0.0-lol1', '1.0.4']
        sort = ['1.0.0', '1.0.0-lol1', '1.0.0.1', '1.0.0.1-lol1', '1.0.1', '1.0.1.1-lol1', '1.0.2', '1.0.3', '1.0.3-lol1', '1.0.3-lol2', '1.0.4', '1.0.4.1']
        self.assertEqual(lastVersion.sortTags(tags), sort)

    def test_allpphanumeric2(self):
        tags = ['1.0.0-lol100', '1.0.3-lol2', '1.0.0', '1.0.0.1-lol1', '1.0.0-lol12', '1.0.0-lol102', '1.0.1', '1.0.4.1', '1.0.1.1-lol1', '1.0.3', '1.0.2', '1.0.0-lol10', '1.0.0.1', '1.0.3-lol1', '1.0.0-lol1', '1.0.4']
        sort = ['1.0.0', '1.0.0-lol1', '1.0.0-lol10', '1.0.0-lol12', '1.0.0-lol100', '1.0.0-lol102', '1.0.0.1', '1.0.0.1-lol1', '1.0.1', '1.0.1.1-lol1', '1.0.2', '1.0.3', '1.0.3-lol1', '1.0.3-lol2', '1.0.4', '1.0.4.1']
        self.assertEqual(lastVersion.sortTags(tags), sort)

if __name__ == '__main__':
    unittest.main()
