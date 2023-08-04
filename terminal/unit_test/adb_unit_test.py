import os
import subprocess
import time
import unittest

from terminal.adb import Adb

adb = Adb()

UDID = "00168910000010"
MODEL = "PT-5F"
INTERNAL_STORAGE = "/sdcard/Download/"
PATH_TO_TERMUX = os.path.join("apk", "termux.apk")
TERMUX_PACKAGE = "com.termux"
TERMUX_ACTIVITY = "com.termux.app.TermuxActivity"
VPN_IP = '213.232.199.14'
SCREEN_RESOLUTION = (720, 1280)

VIRTUAL_KEYBOARD_QWERTY = {
    "q": (41, 790),
    "w": (110, 790),
    "e": (183, 790),
    "r": (254, 790),
    "t": (327, 790),
    "y": (395, 790),
    "u": (470, 790),
    "i": (540, 790),
    "o": (610, 790),
    "p": (680, 790),
    "a": (75, 900),
    "s": (145, 900),
    "d": (215, 900),
    "f": (290, 900),
    "g": (360, 900),
    "h": (430, 900),
    "j": (500, 900),
    "k": (570, 900),
    "l": (645, 900),
    "z": (145, 1010),
    "x": (215, 1010),
    "c": (290, 1010),
    "v": (360, 1010),
    "b": (430, 1010),
    "n": (505, 1010),
    "m": (575, 1010),
    "Q": (41, 790),
    "W": (110, 790),
    "E": (183, 790),
    "R": (254, 790),
    "T": (327, 790),
    "Y": (395, 790),
    "U": (470, 790),
    "I": (540, 790),
    "O": (610, 790),
    "P": (680, 790),
    "A": (75, 900),
    "S": (145, 900),
    "D": (215, 900),
    "F": (290, 900),
    "G": (360, 900),
    "H": (430, 900),
    "J": (500, 900),
    "K": (570, 900),
    "L": (645, 900),
    "Z": (145, 1010),
    "X": (215, 1010),
    "C": (290, 1010),
    "V": (360, 1010),
    "B": (430, 1010),
    "N": (505, 1010),
    "M": (575, 1010),
    "UPPER_CASE": (50, 1010),
    "BACKSPACE": (670, 1010),
    "NUMBERS": (60, 1115),
    ",": (145, 1115),
    "LANG": (215, 1115),
    " ": (380, 1115),
    ".": (575, 1115),
    "OK": (665, 1115)
}


class TestAdb(unittest.TestCase):
    def test_get_device_uuid(self):
        uuid = adb.get_device_uuid()
        self.assertEqual(uuid, UDID)

    def test_get_device_model(self):
        model = adb.get_device_model()
        self.assertEqual(model, MODEL)

    def test_push_pull(self):
        filename = 'new_file.txt'
        with open(filename, 'w') as file:
            file.write('Привет, мир!')
        adb.push(source=filename, destination=f'{INTERNAL_STORAGE}new_file.txt')
        time.sleep(1)
        os.remove(filename)
        adb.pull(source=f'{INTERNAL_STORAGE}new_file.txt', destination=filename)
        time.sleep(5)
        with open(filename, 'r') as file:
            content = file.read()
            self.assertEqual(content, 'Привет, мир!')
        os.remove(filename)
        time.sleep(1)

    def test_is_installed_install_uninstall(self):
        if adb.is_app_installed(package=TERMUX_PACKAGE):
            adb.uninstall_app(package=TERMUX_PACKAGE)
        self.assertTrue(adb.install_app(source=PATH_TO_TERMUX))
        self.assertTrue(adb.is_app_installed(package=TERMUX_PACKAGE))
        self.assertTrue(adb.uninstall_app(package=TERMUX_PACKAGE))
        self.assertFalse(adb.is_app_installed(package=TERMUX_PACKAGE))

    def test_start_activity_get_current_package_get_current_activity(self):
        adb.press_home()
        if not adb.is_app_installed(package=TERMUX_PACKAGE):
            adb.install_app(source=PATH_TO_TERMUX)
        self.assertTrue(adb.start_activity(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY))
        time.sleep(10)
        self.assertEqual(adb.get_current_activity(), TERMUX_ACTIVITY)
        self.assertEqual(adb.get_current_package(), TERMUX_PACKAGE)
        adb.press_home()

    def test_close_app(self):
        if not adb.is_app_installed(package=TERMUX_PACKAGE):
            adb.install_app(source=PATH_TO_TERMUX)
        self.assertTrue(adb.start_activity(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY))
        self.assertTrue(adb.close_app(package=TERMUX_PACKAGE))

    def test_reboot_app(self):
        if not adb.is_app_installed(package=TERMUX_PACKAGE):
            adb.install_app(source=PATH_TO_TERMUX)
        self.assertTrue(adb.reboot_app(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY))
        time.sleep(5)
        self.assertTrue(adb.get_current_activity(), TERMUX_ACTIVITY)

    def test_press_home(self):
        self.assertTrue(adb.press_home())

    def test_press_back(self):
        self.assertTrue(adb.press_back())

    def test_press_menu(self):
        self.assertTrue(adb.press_menu())

    def test_input_keycode_num_(self):
        self.assertTrue(adb.input_keycode_num_(num=1))

    def test_input_keycode(self):
        self.assertTrue(adb.input_keycode(keycode="KEYCODE_VOLUME_UP"))
        time.sleep(3)

    def test_input_by_virtual_keyboard(self):
        time.sleep(1)
        adb.press_home()
        time.sleep(1)
        adb.tap(x=350, y=1100)  # вызов меню приложений
        time.sleep(1)
        adb.tap(x=50, y=100)  # активация клавиатуры
        time.sleep(3)
        self.assertTrue(adb.input_by_virtual_keyboard(text="ok", keyboard=VIRTUAL_KEYBOARD_QWERTY))
        time.sleep(3)
        adb.press_home()
        time.sleep(1)

    def test_input_text(self):
        time.sleep(1)
        adb.press_home()
        time.sleep(1)
        adb.tap(x=350, y=1100)  # вызов меню приложений
        time.sleep(1)
        adb.tap(x=50, y=100)  # активация клавиатуры
        time.sleep(3)
        self.assertTrue(adb.input_text(text="text"))
        time.sleep(1)
        adb.press_home()
        time.sleep(1)

    def test_tap(self):
        time.sleep(1)
        self.assertTrue(adb.tap(x=100, y=10))
        time.sleep(1)

    def test_swipe(self):
        time.sleep(1)
        self.assertTrue(adb.swipe(start_x=10,
                                  start_y=10,
                                  end_x=20,
                                  end_y=20))
        time.sleep(1)

    def test_check_vpn(self):
        time.sleep(1)
        self.assertTrue(adb.check_vpn(ip_address=VPN_IP))
        time.sleep(1)

    def test_stop_logcat(self):
        time.sleep(1)
        command = ['adb', 'logcat']
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.assertTrue(adb.stop_logcat())
        time.sleep(1)

    def test_reload_adb(self):
        time.sleep(1)
        self.assertTrue(adb.reload_adb())
        time.sleep(5)
        command = ['adb', 'shell', 'input', 'tap', str(100), str(100)]
        subprocess.run(command, check=True)

    def test_know_pid_and_kill_by_pid(self):
        time.sleep(1)
        adb.start_activity(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY)
        time.sleep(10)
        pid = adb.know_pid(name=TERMUX_PACKAGE)
        time.sleep(1)
        self.assertTrue(adb.kill_by_pid(pid=pid))
        time.sleep(1)

    def test_kill_by_name(self):
        if not adb.is_app_installed(package=TERMUX_PACKAGE):
            adb.install_app(source=TERMUX_PACKAGE)
        adb.start_activity(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY)
        time.sleep(10)
        adb.kill_by_name(name=TERMUX_PACKAGE)
        time.sleep(3)
        self.assertNotEqual(adb.get_current_activity(), TERMUX_PACKAGE)

    def test_kill_all(self):
        self.assertTrue(adb.run_background_process(command='adb logcat'))
        time.sleep(1)
        self.assertTrue(adb.is_process_exist(name='logcat'))
        self.assertTrue(adb.kill_all(name='logcat'))
        time.sleep(1)

    def test_delete_files_from_internal_storage(self):
        time.sleep(1)
        self.assertTrue(adb.delete_files_from_internal_storage(path=INTERNAL_STORAGE))
        time.sleep(1)

    def test_start_record_video_stop_video_pull_video(self):
        time.sleep(1)
        self.assertTrue(adb.start_record_video(path="sdcard/Movies", filename="record.mp4"))
        time.sleep(10)
        self.assertTrue(adb.stop_video())
        time.sleep(1)
        self.assertTrue(adb.pull_video(source=f'sdcard/Movies/record.mp4', destination="."))
        self.assertTrue(os.path.exists("record.mp4"))
        os.remove("record.mp4")
        self.assertFalse(adb.pull_video(source=f'sdcard/Movies/record.mp4', destination="."))

    def test_record_video(self):
        time.sleep(1)
        self.assertIsInstance(adb.record_video(path='/sdcard/Movies', filename="record.mp4"), subprocess.Popen)

    # def test_reboot(self):
    #     time.sleep(1)
    #     self.assertTrue(adb.reboot())
    #     time.sleep(50)
    #     command = ['adb', 'shell', 'input', 'tap', str(100), str(100)]
    #     subprocess.run(command, check=True)

    def test_get_screen_resolution(self):
        time.sleep(1)
        self.assertEqual(adb.get_screen_resolution(), SCREEN_RESOLUTION)
        time.sleep(1)

    def test_run_background_process_is_process_exist(self):
        time.sleep(1)
        self.assertTrue(adb.run_background_process(command='adb logcat'))
        time.sleep(1)
        self.assertTrue(adb.is_process_exist(name='logcat'))
        self.assertTrue(adb.stop_logcat())


# RUN SUITES
suite = unittest.TestSuite()

# ADD CLASS
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAdb))

# ADD METHODS
# suite.addTest(TestAdb('test_get_device_uuid'))    # ok
# suite.addTest(TestAdb('test_get_device_model'))   # ok
# suite.addTest(TestAdb('test_push_pull'))      # ok
# suite.addTest(TestAdb('test_is_installed_install_uninstall'))      # ok
# suite.addTest(TestAdb('test_start_activity_get_current_package_get_current_activity'))      # ok
# suite.addTest(TestAdb('test_close_app'))      # ok
# suite.addTest(TestAdb('test_reboot_app'))      # ok
# suite.addTest(TestAdb('test_press_home'))      # ok
# suite.addTest(TestAdb('test_press_back'))      # ok
# suite.addTest(TestAdb('test_press_menu'))      # ok
# suite.addTest(TestAdb('test_input_keycode_num_'))      # ok
# suite.addTest(TestAdb('test_input_keycode'))      # ok
# suite.addTest(TestAdb('test_input_by_virtual_keyboard'))      # ok
# suite.addTest(TestAdb('test_input_text'))      # ok
# suite.addTest(TestAdb('test_tap'))      # ok
# suite.addTest(TestAdb('test_swipe'))      # ok
# suite.addTest(TestAdb('test_check_vpn'))    # ok
# suite.addTest(TestAdb('test_stop_logcat'))  # ok
# suite.addTest(TestAdb('test_reload_adb'))      # ok
# suite.addTest(TestAdb('test_know_pid_and_kill_by_pid'))      # ok
# suite.addTest(TestAdb('test_kill_by_name'))      # ok
# suite.addTest(TestAdb('test_kill_all'))      # ok
# suite.addTest(TestAdb('test_delete_files_from_internal_storage'))  # ok
# suite.addTest(TestAdb('test_start_record_video_stop_video_pull_video'))  # ok
# suite.addTest(TestAdb('test_record_video'))  # ok
# suite.addTest(TestAdb('test_get_screen_resolution'))  # ok
# suite.addTest(TestAdb('test_run_background_process_is_process_exist'))  # ok


# RUN
runner = unittest.TextTestRunner()
runner.run(suite)
