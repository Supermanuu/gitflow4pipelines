#!/usr/bin/env python3

import unittest # The test framework
import version # The code to test

class Test_getVersion(unittest.TestCase):
    # TODO: create an empty local git to perform tests?
    def test_format00(self):
        version.getVersionFromBranchName('dfsf')


class Test_getVersionFromBranchName(unittest.TestCase):
    def test_format00(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'dfsf')

    def test_format01(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release')

    def test_format02(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/')

    def test_format03(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1')

    def test_format04(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.')

    def test_format05(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.1')

    def test_format06(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.1.')

    def test_format07(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.1.1.1.1')

    def test_format08(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.1.1-')

    def test_format09(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.1.1.1-')

    def test_format10(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.1.1.1+')

    def test_format11(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.1.1.1-e')

    def test_format12(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.2.3.4-lol5')

    def test_format13(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, '  release/1.0.0.2')

    def test_format14(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.0.0-1')
    
    def test_format15(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, '* release/1.0.0-2')

    def test_format16(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, '* release/1.0.0-2+RS')

    def test_format17(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.2.3.4-5')

    def test_format18(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.2.3.4-5+lolaso')

    def test_format19(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromBranchName, 'release/1.2.3.4-5+RS232')

    def test_normal(self):
        self.assertEqual(version.getVersionFromBranchName('release/1.0.0'), '1.0.0')

    def test_revision1(self):
        self.assertEqual(version.getVersionFromBranchName('release/1.0.0.1'), '1.0.0.1')

    def test_revision2(self):
        self.assertEqual(version.getVersionFromBranchName('release/1.0.0.2'), '1.0.0.2')

    def test_additional1(self):
        self.assertEqual(version.getVersionFromBranchName('release/1.0.0+RS'), '1.0.0+RS')
    
    def test_additional2(self):
        self.assertEqual(version.getVersionFromBranchName('release/1.0.0+123456'), '1.0.0+123456')

    def test_allphanumeric1(self):
        self.assertEqual(version.getVersionFromBranchName('release/1.2.3.4+lolaso'), '1.2.3.4+lolaso')

    def test_allphanumeric2(self):
        self.assertEqual(version.getVersionFromBranchName('release/1.2.3.4+RS232'), '1.2.3.4+RS232')


class Test_aptVersioning(unittest.TestCase):
    def test_void(self):
        self.assertRaises(RuntimeError, version.aptVersioning, '')

    def test_bad1(self):
        self.assertRaises(RuntimeError, version.aptVersioning, '1')

    def test_bad2(self):
        self.assertRaises(RuntimeError, version.aptVersioning, '1.')

    def test_bad3(self):
        self.assertRaises(RuntimeError, version.aptVersioning, '1.2')

    def test_bad4(self):
        self.assertRaises(RuntimeError, version.aptVersioning, '1.2.')

    def test_bad5(self):
        self.assertRaises(RuntimeError, version.aptVersioning, '1.2.3+')

    def test_bad6(self):
        self.assertRaises(RuntimeError, version.aptVersioning, '1.2.3-')

    def test_bad7(self):
        self.assertRaises(RuntimeError, version.aptVersioning, '1.2.3-bad')

    def test_normal1(self):
        self.assertEqual(version.aptVersioning('1.0.0'), '1.0.0')

    def test_normal2(self):
        self.assertEqual(version.aptVersioning('1.2.0'), '1.2.0')

    def test_normal3(self):
        self.assertEqual(version.aptVersioning('1.0.3'), '1.0.3')

    def test_revision1(self):
        self.assertEqual(version.aptVersioning('1.0.0.4'), '4:1.0.0')

    def test_revision2(self):
        self.assertEqual(version.aptVersioning('1.2.0.4'), '4:1.2.0')

    def test_revision3(self):
        self.assertEqual(version.aptVersioning('1.0.3.4'), '4:1.0.3')

    # With +
    def test_normal1lolaso(self):
        self.assertEqual(version.aptVersioning('1.0.0+lolaso'), '1.0.0+lolaso')

    def test_normal2lolaso(self):
        self.assertEqual(version.aptVersioning('1.2.0+lolaso1'), '1.2.0+lolaso1')

    def test_normal3lolaso(self):
        self.assertEqual(version.aptVersioning('1.0.3+lolaso'), '1.0.3+lolaso')

    def test_revision1lolaso(self):
        self.assertEqual(version.aptVersioning('1.0.0.4+lolaso1'), '4:1.0.0+lolaso1')

    def test_revision2lolaso(self):
        self.assertEqual(version.aptVersioning('1.2.0.4+lolaso'), '4:1.2.0+lolaso')

    def test_revision3lolaso(self):
        self.assertEqual(version.aptVersioning('1.0.3.4+lolaso1'), '4:1.0.3+lolaso1')


if __name__ == '__main__':
    unittest.main()
