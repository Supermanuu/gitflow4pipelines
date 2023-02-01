#!/usr/bin/env python3

import unittest # The test framework
import brancheck # The code to test


class Test_getVersionFromBranchName(unittest.TestCase):
    def test_format00(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'dfsf', 'main')

    def test_format01(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'release', 'main')

    def test_badFeature2main(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'feature/1.0.0', 'main')

    def test_badFeature2master(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'feature/1.0.0', 'master')

    def test_badFeature2integration(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'feature/1.0.0', 'integration')

    def test_badRelease2main(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'release/1.0.0', 'main')

    def test_badRelease2master(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'release/1.0.0', 'master')

    def test_badbug2main(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'bug/1.0.0', 'main')

    def test_badbug2master(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'bug/1.0.0', 'master')

    def test_badbug2integration(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'bug/1.0.0', 'integration')

    def test_badbugfix2main(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'bugfix/1.0.0', 'main')

    def test_badbugfix2master(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'bugfix/1.0.0', 'master')

    def test_badbugfix2integration(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'bugfix/1.0.0', 'integration')

    def test_badfix2main(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'fix/1.0.0', 'main')

    def test_badfix2master(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'fix/1.0.0', 'master')

    def test_badfix2release(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'fix/1.0.0', 'release/1.0.0')

    def test_badhotfix2integration(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'hotfix/1.0.0', 'integration')

    def test_badhotfix2release(self):
        self.assertRaises(RuntimeError, brancheck.brancheck, 'hotfix/1.0.0', 'release/1.0.0')

    # Merged to release
    def test_feature2release1(self):
        brancheck.brancheck('feature/afgjhdflj', 'release/1.0.0')

    def test_feature2release2(self):
        brancheck.brancheck('feature/1.0.0.1+RS232', 'release/1.0.0.1+RS232')

    def test_bugfix2release1(self):
        brancheck.brancheck('bugfix/afgjhdflj', 'release/1.0.0')

    def test_bugfix2release2(self):
        brancheck.brancheck('bugfix/1.0.0.1+RS232', 'release/1.0.0.1+RS232')

    def test_bug2release1(self):
        brancheck.brancheck('bug/afgjhdflj', 'release/1.0.0')

    def test_bug2release2(self):
        brancheck.brancheck('bug/1.0.0.1+RS232', 'release/1.0.0.1+RS232')

    # Merged to integration
    def test_release2integration1(self):
        brancheck.brancheck('release/1.0.0', 'integration')

    def test_release2integration2(self):
        brancheck.brancheck('release/1.0.0.1+RS232', 'integration')

    def test_fix2integration1(self):
        brancheck.brancheck('fix/1.0.0', 'integration')

    def test_fix2integration2(self):
        brancheck.brancheck('fix/1.0.0.1+RS232', 'integration')

    # Merged to master
    def test_integration2master(self):
        brancheck.brancheck('integration', 'master')

    def test_hotfix2master(self):
        brancheck.brancheck('hotfix/1.0.0', 'master')

    def test_hotfix2master2(self):
        brancheck.brancheck('hotfix/1.0.0.1+RS232', 'master')

    # Merged to main
    def test_integration2main(self):
        brancheck.brancheck('integration', 'main')

    def test_hotfix2main(self):
        brancheck.brancheck('hotfix/1.0.0', 'main')

    def test_hotfix2main2(self):
        brancheck.brancheck('hotfix/1.0.0.1+RS232', 'main')

    # Merged to release with refs/heads/
    def test_feature2release1withRefsHeads(self):
        brancheck.brancheck('refs/heads/feature/afgjhdflj', 'refs/heads/release/1.0.0')

    def test_feature2release2withRefsHeads(self):
        brancheck.brancheck('refs/heads/feature/1.0.0.1+RS232', 'refs/heads/release/1.0.0.1+RS232')

    def test_bugfix2release1withRefsHeads(self):
        brancheck.brancheck('refs/heads/bugfix/afgjhdflj', 'refs/heads/release/1.0.0')

    def test_bugfix2release2withRefsHeads(self):
        brancheck.brancheck('refs/heads/bugfix/1.0.0.1+RS232', 'refs/heads/release/1.0.0.1+RS232')

    def test_bug2release1withRefsHeads(self):
        brancheck.brancheck('refs/heads/bug/afgjhdflj', 'refs/heads/release/1.0.0')

    def test_bug2release2withRefsHeads(self):
        brancheck.brancheck('refs/heads/bug/1.0.0.1+RS232', 'refs/heads/release/1.0.0.1+RS232')

    # Merged to integration with refs/heads/
    def test_release2integration1withRefsHeads(self):
        brancheck.brancheck('refs/heads/release/1.0.0', 'refs/heads/integration')

    def test_release2integration2withRefsHeads(self):
        brancheck.brancheck('refs/heads/release/1.0.0.1+RS232', 'refs/heads/integration')

    def test_fix2integration1withRefsHeads(self):
        brancheck.brancheck('refs/heads/fix/1.0.0', 'refs/heads/integration')

    def test_fix2integration2withRefsHeads(self):
        brancheck.brancheck('refs/heads/fix/1.0.0.1+RS232', 'refs/heads/integration')

    # Merged to master with refs/heads/
    def test_integration2masterwithRefsHeads(self):
        brancheck.brancheck('refs/heads/integration', 'refs/heads/master')

    def test_hotfix2masterwithRefsHeads(self):
        brancheck.brancheck('refs/heads/hotfix/1.0.0', 'refs/heads/master')

    def test_hotfix2master2withRefsHeads(self):
        brancheck.brancheck('refs/heads/hotfix/1.0.0.1+RS232', 'refs/heads/master')

    # Merged to main with refs/heads/
    def test_integration2mainwithRefsHeads(self):
        brancheck.brancheck('refs/heads/integration', 'refs/heads/main')

    def test_hotfix2mainwithRefsHeads(self):
        brancheck.brancheck('refs/heads/hotfix/1.0.0', 'refs/heads/main')

    def test_hotfix2main2withRefsHeads(self):
        brancheck.brancheck('refs/heads/hotfix/1.0.0.1+RS232', 'refs/heads/main')


if __name__ == '__main__':
    unittest.main()
