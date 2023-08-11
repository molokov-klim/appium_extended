import unittest
import os

from appium_extended_terminal.aapt import Aapt
from appium_extended_terminal.adb import Adb

aapt = Aapt()
adb = Adb()

PATH_TO_APK = os.path.join("apk", "termux.apk")
adb.install_app(source=PATH_TO_APK)


class TestAapt(unittest.TestCase):

    def test_get_launchable_activity(self):
        activity = aapt.get_launchable_activity(PATH_TO_APK)
        self.assertEqual(activity, "com.termux.app.TermuxActivity")

    def test_get_package_name(self):
        package = aapt.get_package_name(PATH_TO_APK)
        self.assertEqual(package, "com.termux")


# RUN SUITES
suite = unittest.TestSuite()

# ADD CLASS
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAapt))

# RUN
runner = unittest.TextTestRunner()
runner.run(suite)
