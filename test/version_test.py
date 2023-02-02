#!/usr/bin/env python3

import unittest # The test framework
import version # The code to test

import os
import subprocess

class Test_getVersion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if subprocess.call('rm -rf testRepo'.split(' ')) != 0:
            raise RuntimeError('Cannot remove test repo')
        if subprocess.call('mkdir testRepo'.split(' ')) != 0 \
            or subprocess.call('git -C testRepo init'.split(' ')) != 0:
            raise RuntimeError('Cannot create test repo')
        os.chdir('testRepo')

    @classmethod
    def tearDownClass(cls):
        os.chdir('..')

    def test_01firstRelease(self):
        self.assertEqual(subprocess.call('touch first'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add first'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m first'.split(' ')), 0)
        self.assertEqual(subprocess.call('git checkout -b release/1.0.0'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.0')

    def test_02secondRelease(self):
        self.assertEqual(subprocess.call('touch second'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add second'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m second'.split(' ')), 0)
        self.assertEqual(subprocess.call('git checkout -b release/1.0.1'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.1')

    def test_03secondReleaseAgain(self):
        self.assertEqual(subprocess.call('touch nope'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add nope'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m nope'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.1')

    def test_04secondReleaseAgainAgain(self):
        self.assertEqual(subprocess.call('touch nopenope'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add nopenope'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m nopenope'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.1')

    def test_05thirthRelease(self):
        self.assertEqual(subprocess.call('touch thirth'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add thirth'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m thirth'.split(' ')), 0)
        self.assertEqual(subprocess.call('git checkout -b release/1.0.2'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.2')

    def test_06thirthReleaseWithOtherAdditionalRelease(self):
        self.assertEqual(subprocess.call('git checkout -b release/1.0.2+ThirthAddition'.split(' ')), 0)
        self.assertNotEqual(version.getFirstNormalizedVersion(), '1.0.2')
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.2+ThirthAddition')

    def test_07nonRelease(self):
        self.assertEqual(subprocess.call('touch none'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add none'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m none'.split(' ')), 0)
        self.assertEqual(subprocess.call('git checkout -b feature/none'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.2+ThirthAddition')

    def test_08forthRelease(self):
        self.assertEqual(subprocess.call('git checkout -b release/1.0.3'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.3')

    def test_09flashback(self):
        self.assertEqual(subprocess.call('git checkout release/1.0.1'.split(' ')), 0)
        self.assertEqual(subprocess.call('touch flashback'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add flashback'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m flashback'.split(' ')), 0)
        self.assertEqual(subprocess.call('git checkout -b feature/flashback'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.1')

    def test_10flashbackRelease(self):
        self.assertEqual(subprocess.call('git checkout -b release/1.0.1+flashback'.split(' ')), 0)
        self.assertEqual(version.getFirstNormalizedVersion(), '1.0.1+flashback')


class Test_getVersionFromCurrentBranch(unittest.TestCase):
    def test_format00(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'dfsf')

    def test_format01(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release')

    def test_format02(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/')

    def test_format03(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1')

    def test_format04(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.')

    def test_format05(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.1')

    def test_format06(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.1.')

    def test_format07(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.1.1.1.1')

    def test_format08(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.1.1-')

    def test_format09(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.1.1.1-')

    def test_format10(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.1.1.1+')

    def test_format11(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.1.1.1-e')

    def test_format12(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.2.3.4-lol5')

    def test_format13(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, '  release/1.0.0.2')

    def test_format14(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.0.0-1')
    
    def test_format15(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, '* release/1.0.0-2')

    def test_format16(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, '* release/1.0.0-2+RS')

    def test_format17(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.2.3.4-5')

    def test_format18(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.2.3.4-5+lolaso')

    def test_format19(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.getVersionFromCurrentBranch, 'release/1.2.3.4-5+RS232')

    def test_normal(self):
        self.assertEqual(version.getVersionFromCurrentBranch('release/1.0.0'), '1.0.0')

    def test_revision1(self):
        self.assertEqual(version.getVersionFromCurrentBranch('release/1.0.0.1'), '1.0.0.1')

    def test_revision2(self):
        self.assertEqual(version.getVersionFromCurrentBranch('release/1.0.0.2'), '1.0.0.2')

    def test_additional1(self):
        self.assertEqual(version.getVersionFromCurrentBranch('release/1.0.0+RS'), '1.0.0+RS')
    
    def test_additional2(self):
        self.assertEqual(version.getVersionFromCurrentBranch('release/1.0.0+123456'), '1.0.0+123456')

    def test_allphanumeric1(self):
        self.assertEqual(version.getVersionFromCurrentBranch('release/1.2.3.4+lolaso'), '1.2.3.4+lolaso')

    def test_allphanumeric2(self):
        self.assertEqual(version.getVersionFromCurrentBranch('release/1.2.3.4+RS232'), '1.2.3.4+RS232')


class Test_debVersioning(unittest.TestCase):
    def test_void(self):
        self.assertRaises(RuntimeError, version.debVersioning, '')

    def test_bad1(self):
        self.assertRaises(RuntimeError, version.debVersioning, '1')

    def test_bad2(self):
        self.assertRaises(RuntimeError, version.debVersioning, '1.')

    def test_bad3(self):
        self.assertRaises(RuntimeError, version.debVersioning, '1.2')

    def test_bad4(self):
        self.assertRaises(RuntimeError, version.debVersioning, '1.2.')

    def test_bad5(self):
        self.assertRaises(RuntimeError, version.debVersioning, '1.2.3+')

    def test_bad6(self):
        self.assertRaises(RuntimeError, version.debVersioning, '1.2.3-')

    def test_bad7(self):
        self.assertRaises(RuntimeError, version.debVersioning, '1.2.3-bad')

    def test_normal1(self):
        self.assertEqual(version.debVersioning('1.0.0'), '1.0.0')

    def test_normal2(self):
        self.assertEqual(version.debVersioning('1.2.0'), '1.2.0')

    def test_normal3(self):
        self.assertEqual(version.debVersioning('1.0.3'), '1.0.3')

    def test_revision1(self):
        self.assertEqual(version.debVersioning('1.0.0.4'), '4:1.0.0')

    def test_revision2(self):
        self.assertEqual(version.debVersioning('1.2.0.4'), '4:1.2.0')

    def test_revision3(self):
        self.assertEqual(version.debVersioning('1.0.3.4'), '4:1.0.3')

    # With +
    def test_normal1lolaso(self):
        self.assertEqual(version.debVersioning('1.0.0+lolaso'), '1.0.0+lolaso')

    def test_normal2lolaso(self):
        self.assertEqual(version.debVersioning('1.2.0+lolaso1'), '1.2.0+lolaso1')

    def test_normal3lolaso(self):
        self.assertEqual(version.debVersioning('1.0.3+lolaso'), '1.0.3+lolaso')

    def test_revision1lolaso(self):
        self.assertEqual(version.debVersioning('1.0.0.4+lolaso1'), '4:1.0.0+lolaso1')

    def test_revision2lolaso(self):
        self.assertEqual(version.debVersioning('1.2.0.4+lolaso'), '4:1.2.0+lolaso')

    def test_revision3lolaso(self):
        self.assertEqual(version.debVersioning('1.0.3.4+lolaso1'), '4:1.0.3+lolaso1')


if __name__ == '__main__':
    unittest.main()
