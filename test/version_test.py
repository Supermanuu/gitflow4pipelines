#!/usr/bin/env python3

import unittest # The test framework
import version # The code to test

import os
import subprocess

class Test_get_version(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if subprocess.call('rm -rf testRepo'.split(' ')) != 0:
            raise RuntimeError('Cannot remove test repo')
        if subprocess.call('mkdir testRepo'.split(' ')) != 0 \
            or subprocess.call('git -C testRepo init'.split(' ')) != 0 \
            or subprocess.call('git -C testRepo checkout -b main'.split(' ')) != 0 \
            or subprocess.call('git -C testRepo remote add origin https://127.0.0.1/what/an/url/testRepo'.split(' ')) != 0 \
            or subprocess.call('git -C testRepo config user.email you@example.com'.split(' ')) != 0 \
            or subprocess.call('git -C testRepo config user.name Name'.split(' ')) != 0:
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
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'', 'identifier':''})

    def test_02secondRelease(self):
        self.assertEqual(subprocess.call('git checkout -b release/1.0.1'.split(' ')), 0)
        self.assertEqual(subprocess.call('touch second'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add second'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m second'.split(' ')), 0)
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'1', 'revision':'', 'identifier':''})

    def test_03secondReleaseAgain(self):
        self.assertEqual(subprocess.call('touch nope'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add nope'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m nope'.split(' ')), 0)
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'1', 'revision':'', 'identifier':''})

    def test_04secondReleaseAgainAgain(self):
        self.assertEqual(subprocess.call('touch nopenope'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add nopenope'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m nopenope'.split(' ')), 0)
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'1', 'revision':'', 'identifier':''})

    def test_05thirthRelease(self):
        self.assertEqual(subprocess.call('git checkout -b release/1.0.2'.split(' ')), 0)
        self.assertEqual(subprocess.call('touch thirth'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add thirth'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m thirth'.split(' ')), 0)
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'2', 'revision':'', 'identifier':''})

    def test_06thirthReleaseWithOtherAdditionalRelease(self):
        self.assertEqual(subprocess.call('git checkout -b release/1.0.2+1noAddition'.split(' ')), 0)
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'2', 'revision':'', 'identifier':'+1noAddition'})

    def test_07nonRelease(self):
        self.assertEqual(subprocess.call('git checkout -b feature/none'.split(' ')), 0)
        self.assertEqual(subprocess.call('touch none'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add none'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m none'.split(' ')), 0)
        # We have to choose the not noAddition branch name cause this branch has no different changes from 1.0.2
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'2', 'revision':'', 'identifier':''})

    def test_08forthRelease(self):
        self.assertEqual(subprocess.call('git checkout -b release/1.0.3'.split(' ')), 0)
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'3', 'revision':'', 'identifier':''})

    def test_09flashback(self):
        self.assertEqual(subprocess.call('git checkout release/1.0.1'.split(' ')), 0)
        self.assertEqual(subprocess.call('git checkout -b feature/flashback'.split(' ')), 0)
        self.assertEqual(subprocess.call('touch flashback'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add flashback'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m flashback'.split(' ')), 0)
        # We have always to choose the most ancient version cause is where the commit was really done. After, the newest versions used it to build its changes
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'1', 'revision':'', 'identifier':''})

    def test_10flashbackRelease(self):
        self.assertEqual(subprocess.call('git checkout -b release/1.0.1+flashback'.split(' ')), 0)
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'1', 'revision':'', 'identifier':'+flashback'})

    def test_11thirthReleaseRevision(self):
        self.assertEqual(subprocess.call('git checkout release/1.0.3'.split(' ')), 0)
        self.assertEqual(subprocess.call('git checkout -b release/1.0.3.1'.split(' ')), 0)
        self.assertEqual(subprocess.call('touch revision'.split(' ')), 0)
        self.assertEqual(subprocess.call('git add revision'.split(' ')), 0)
        self.assertEqual(subprocess.call('git commit -m revision'.split(' ')), 0)
        self.assertEqual(version.get_version(), {'major':'1', 'minor':'0', 'patch':'3', 'revision':'1', 'identifier':''})


class Test_get_version_from_current_branch(unittest.TestCase):
    def test_format00(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'dfsf')

    def test_format01(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release')

    def test_format02(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/')

    def test_format03(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1')

    def test_format04(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.')

    def test_format05(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.1')

    def test_format06(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.1.')

    def test_format07(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.1.1.1.1')

    def test_format08(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.1.1-')

    def test_format09(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.1.1.1-')

    def test_format10(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.1.1.1+')

    def test_format11(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.1.1.1-e')

    def test_format12(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.2.3.4-lol5')

    def test_format13(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, '  release/1.0.0.2')

    def test_format14(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.0.0-1')
    
    def test_format15(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, '* release/1.0.0-2')

    def test_format16(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, '* release/1.0.0-2+RS')

    def test_format17(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.2.3.4-5')

    def test_format18(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.2.3.4-5+lolaso')

    def test_format19(self):
        self.assertRaises(version.ReleaseIsNotNormalized, version.get_version_from_current_branch, 'release/1.2.3.4-5+RS232')

    def test_normal(self):
        self.assertEqual(version.get_version_from_current_branch('release/1.0.0'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'', 'identifier':''})

    def test_revision1(self):
        self.assertEqual(version.get_version_from_current_branch('release/1.0.0.1'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'1', 'identifier':''})

    def test_revision2(self):
        self.assertEqual(version.get_version_from_current_branch('release/1.0.0.2'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'2', 'identifier':''})

    def test_additional1(self):
        self.assertEqual(version.get_version_from_current_branch('release/1.0.0+RS'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'', 'identifier':'+RS'})
    
    def test_additional2(self):
        self.assertEqual(version.get_version_from_current_branch('release/1.0.0+123456'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'', 'identifier':'+123456'})

    def test_allphanumeric1(self):
        self.assertEqual(version.get_version_from_current_branch('release/1.2.3.4+lolaso'), {'major':'1', 'minor':'2', 'patch':'3', 'revision':'4', 'identifier':'+lolaso'})

    def test_allphanumeric2(self):
        self.assertEqual(version.get_version_from_current_branch('release/1.2.3.4+RS232'), {'major':'1', 'minor':'2', 'patch':'3', 'revision':'4', 'identifier':'+RS232'})

    def test_remote1(self):
        self.assertEqual(version.get_version_from_current_branch('remotes/origin/release/1.2.3.4+RS232'), {'major':'1', 'minor':'2', 'patch':'3', 'revision':'4', 'identifier':'+RS232'})
    
    def test_remote1(self):
        self.assertEqual(version.get_version_from_current_branch('remotes/origin/release/2.13.0'), {'major':'2', 'minor':'13', 'patch':'0', 'revision':'', 'identifier':''})

class Test_split_version(unittest.TestCase):
    def test_void(self):
        self.assertRaises(RuntimeError, version.split_version, '')

    def test_bad1(self):
        self.assertRaises(RuntimeError, version.split_version, '1')

    def test_bad2(self):
        self.assertRaises(RuntimeError, version.split_version, '1.')

    def test_bad3(self):
        self.assertRaises(RuntimeError, version.split_version, '1.2')

    def test_bad4(self):
        self.assertRaises(RuntimeError, version.split_version, '1.2.')

    def test_bad5(self):
        self.assertRaises(RuntimeError, version.split_version, '1.2.3+')

    def test_bad6(self):
        self.assertRaises(RuntimeError, version.split_version, '1.2.3-')

    def test_bad7(self):
        self.assertRaises(RuntimeError, version.split_version, '1.2.3-bad')

    def test_normal1(self):
        self.assertEqual(version.split_version('1.0.0'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'', 'identifier':''})

    def test_normal2(self):
        self.assertEqual(version.split_version('1.2.0'), {'major':'1', 'minor':'2', 'patch':'0', 'revision':'', 'identifier':''})

    def test_normal3(self):
        self.assertEqual(version.split_version('1.0.3'), {'major':'1', 'minor':'0', 'patch':'3', 'revision':'', 'identifier':''})

    def test_revision1(self):
        self.assertEqual(version.split_version('1.0.0.4'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'4', 'identifier':''})

    def test_revision2(self):
        self.assertEqual(version.split_version('1.2.0.4'), {'major':'1', 'minor':'2', 'patch':'0', 'revision':'4', 'identifier':''})

    def test_revision3(self):
        self.assertEqual(version.split_version('1.0.3.4'), {'major':'1', 'minor':'0', 'patch':'3', 'revision':'4', 'identifier':''})

    # With +
    def test_normal1lolaso(self):
        self.assertEqual(version.split_version('1.0.0+lolaso'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'', 'identifier':'+lolaso'})

    def test_normal2lolaso(self):
        self.assertEqual(version.split_version('1.2.0+lolaso1'), {'major':'1', 'minor':'2', 'patch':'0', 'revision':'', 'identifier':'+lolaso1'})

    def test_normal3lolaso(self):
        self.assertEqual(version.split_version('1.0.3+lolaso'), {'major':'1', 'minor':'0', 'patch':'3', 'revision':'', 'identifier':'+lolaso'})

    def test_revision1lolaso(self):
        self.assertEqual(version.split_version('1.0.0.4+lolaso1'), {'major':'1', 'minor':'0', 'patch':'0', 'revision':'4', 'identifier':'+lolaso1'})

    def test_revision2lolaso(self):
        self.assertEqual(version.split_version('1.2.0.4+lolaso'), {'major':'1', 'minor':'2', 'patch':'0', 'revision':'4', 'identifier':'+lolaso'})

    def test_revision3lolaso(self):
        self.assertEqual(version.split_version('1.0.3.4+lolaso1'), {'major':'1', 'minor':'0', 'patch':'3', 'revision':'4', 'identifier':'+lolaso1'})


class Test_format_version(unittest.TestCase):
    def test_normal1(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0')), '1.0.0')

    def test_normal2(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0')), '1.2.0')

    def test_normal3(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3')), '1.0.3')

    def test_revision1(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0.4')), '1.0.0.4')

    def test_revision2(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0.4')), '1.2.0.4')

    def test_revision3(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3.4')), '1.0.3.4')

    # With identifier
    def test_normal1lolaso(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0+lolaso')), '1.0.0+lolaso')

    def test_normal2lolaso(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0+lolaso1')), '1.2.0+lolaso1')

    def test_normal3lolaso(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3+lolaso')), '1.0.3+lolaso')

    def test_revision1lolaso(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0.4+lolaso1')), '1.0.0.4+lolaso1')

    def test_revision2lolaso(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0.4+lolaso')), '1.2.0.4+lolaso')

    def test_revision3lolaso(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3.4+lolaso1')), '1.0.3.4+lolaso1')

    # With deb formatting
    def test_revision1deb(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0.4'), deb_version=True), '4:1.0.0')

    def test_revision2deb(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0.4'), deb_version=True), '4:1.2.0')

    def test_revision3deb(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3.4'), deb_version=True), '4:1.0.3')

    # With deb formatting and identifier
    def test_revision1lolasoDeb(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0.4+lolaso1'), deb_version=True), '4:1.0.0+lolaso1')

    def test_revision2lolasoDeb(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0.4+lolaso'), deb_version=True), '4:1.2.0+lolaso')

    def test_revision3lolasoDeb(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3.4+lolaso1'), deb_version=True), '4:1.0.3+lolaso1')

    # With deb formatting, identifier and architecture
    def test_revision1lolasoDebAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0.4+lolaso1'), deb_version=True, architecture='amd64'), '4:1.0.0+lolaso1_amd64')

    def test_revision2lolasoDebAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0.4+lolaso'), deb_version=True, architecture='amd64'), '4:1.2.0+lolaso_amd64')

    def test_revision3lolasoDebAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3.4+lolaso1'), deb_version=True, architecture='amd64'), '4:1.0.3+lolaso1_amd64')

    # With deb formatting, identifier and project name
    def test_revision1lolasoDebAndProj(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0.4+lolaso1'), deb_version=True, project_name=True), 'versionContainer_4:1.0.0+lolaso1')

    def test_revision2lolasoDebAndProj(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0.4+lolaso'), deb_version=True, project_name=True), 'versionContainer_4:1.2.0+lolaso')

    def test_revision3lolasoDebAndProj(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3.4+lolaso1'), deb_version=True, project_name=True), 'versionContainer_4:1.0.3+lolaso1')

    # With deb formatting, identifier, architecture and project name
    def test_revision1lolasoDebAndProjAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0.4+lolaso1'), deb_version=True, project_name=True, architecture='amd64'), 'versionContainer_4:1.0.0+lolaso1_amd64')

    def test_revision2lolasoDebAndProjAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0.4+lolaso'), deb_version=True, project_name=True, architecture='amd64'), 'versionContainer_4:1.2.0+lolaso_amd64')

    def test_revision3lolasoDebAndProjAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3.4+lolaso1'), deb_version=True, project_name=True, architecture='amd64'), 'versionContainer_4:1.0.3+lolaso1_amd64')

    # Without deb formatting but with identifier, architecture and project name
    def test_revision1lolasoAndProjAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.0.0.4+lolaso1'), project_name=True, architecture='amd64'), '1.0.0.4+lolaso1')

    def test_revision2lolasoAndProjAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.2.0.4+lolaso'), project_name=True, architecture='amd64'), '1.2.0.4+lolaso')

    def test_revision3lolasoAndProjAndArch(self):
        self.assertEqual(version.format_version(version.split_version('1.0.3.4+lolaso1'), project_name=True, architecture='amd64'), '1.0.3.4+lolaso1')


if __name__ == '__main__':
    unittest.main()
