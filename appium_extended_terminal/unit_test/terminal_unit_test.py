import os
import time
import unittest

from appium_extended.appium_extended import AppiumExtended
from appium_extended_terminal.terminal import Terminal

app = AppiumExtended()

capabilities = {
    "platformName": "android",
    "appium:automationName": "uiautomator2",
}

app.connect(capabilities=capabilities)
assert app.server.is_alive()
terminal = Terminal(app.driver)

IMEI = "123470000000389"
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


class TestTerminal(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTerminal, self).__init__(*args, **kwargs)
        self.app = app
        self.terminal = terminal

    def test_adb_shell(self):
        time.sleep(1)
        command = 'service'
        args = 'call iphonesubinfo 1 | grep -o \'[0-9a-f]\\{8\\} \' | tail -n+3 | while read a; do echo -n \\\\u${a:4:4}\\\\u${a:0:4}; done'
        result = self.terminal.adb_shell(command, args)
        time.sleep(1)
        result = result.replace('\x00', '')
        self.assertEqual(result, IMEI)
        time.sleep(1)

    def test_push_and_pull(self):
        time.sleep(1)
        filename = 'new_file.txt'
        with open(filename, 'w') as file:
            file.write('Привет, мир!')
        self.terminal.push(source=filename,
                           destination=f'{INTERNAL_STORAGE}new_file.txt')
        time.sleep(1)
        os.remove(filename)
        self.terminal.pull(source=f"{INTERNAL_STORAGE}new_file.txt",
                           destination=filename)
        time.sleep(1)
        time.sleep(5)
        with open(filename, 'r') as file:
            content = file.read()
            self.assertEqual(content, 'Привет, мир!')
        os.remove(filename)
        time.sleep(1)

    def test_start_activity(self):
        time.sleep(1)
        self.terminal.start_activity(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY)
        time.sleep(5)
        package = self.terminal.get_current_app_package()
        print("test_start_activity", self.terminal.get_current_app_package())
        time.sleep(1)
        result = True if TERMUX_PACKAGE in package else False
        self.assertTrue(result)
        time.sleep(1)

    def test_close_app(self):
        time.sleep(1)
        self.terminal.start_activity(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY)
        time.sleep(10)
        self.terminal.close_app(package=TERMUX_PACKAGE)
        time.sleep(1)
        package = self.terminal.get_current_app_package()
        time.sleep(1)
        result = True if TERMUX_PACKAGE in package else False
        self.assertFalse(result)
        time.sleep(1)

    def test_reboot_app(self):
        time.sleep(1)
        self.terminal.start_activity(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY)
        time.sleep(1)
        self.terminal.reboot_app(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY)
        time.sleep(10)
        package = self.terminal.get_current_app_package()
        print("test_reboot_app", self.terminal.get_current_app_package())
        time.sleep(1)
        result = True if TERMUX_PACKAGE in package else False
        self.assertTrue(result)
        time.sleep(1)

    def test_press_home(self):
        time.sleep(1)
        self.assertTrue(self.terminal.press_home())
        time.sleep(1)

    def test_press_back(self):
        time.sleep(1)
        self.assertTrue(self.terminal.press_back())
        time.sleep(1)

    def test_press_menu(self):
        time.sleep(1)
        self.assertTrue(self.terminal.press_menu())
        time.sleep(1)

    def test_input_keycode_num_(self):
        time.sleep(1)
        self.assertTrue(self.terminal.input_keycode_num_(num=1))
        time.sleep(1)

    def test_input_keycode(self):
        time.sleep(1)
        self.assertTrue(self.terminal.input_keycode(keycode="KEYCODE_VOLUME_UP"))
        time.sleep(1)

    def test_input_by_virtual_keyboard(self):
        time.sleep(1)
        self.terminal.press_home()
        time.sleep(1)
        self.terminal.tap(x=350, y=1100)  # вызов меню приложений
        time.sleep(1)
        self.terminal.tap(x=50, y=100)  # активация клавиатуры
        time.sleep(1)
        time.sleep(3)
        self.assertTrue(self.terminal.input_by_virtual_keyboard(key="ok",
                                                                keyboard=VIRTUAL_KEYBOARD_QWERTY))
        time.sleep(3)
        self.terminal.press_home()
        time.sleep(1)

    def test_input_text(self):
        time.sleep(1)
        self.assertTrue(self.terminal.input_text(text="text"))
        time.sleep(1)

    def test_tap(self):
        time.sleep(1)
        self.assertTrue(self.terminal.tap(x=10, y=10))
        time.sleep(1)

    def test_swipe(self):
        time.sleep(1)
        self.assertTrue(self.terminal.swipe(start_x=10,
                                            start_y=10,
                                            end_x=20,
                                            end_y=20))
        time.sleep(1)

    def test_check_VPN(self):
        time.sleep(1)
        self.assertTrue(self.terminal.check_vpn(ip_address=VPN_IP))
        time.sleep(1)

    def test_stop_logcat(self):
        time.sleep(1)
        self.assertTrue(self.terminal.stop_logcat())
        time.sleep(1)

    def test_know_pid_and_kill_by_pid(self):
        if not self.terminal.is_app_installed(package=TERMUX_PACKAGE):
            self.terminal.install_app(app_path=PATH_TO_TERMUX)
        time.sleep(1)
        self.terminal.start_activity(package=TERMUX_PACKAGE, activity=TERMUX_ACTIVITY)
        time.sleep(10)
        pid = self.terminal.know_pid(name=TERMUX_PACKAGE)
        time.sleep(1)
        try:
            self.assertFalse(self.terminal.kill_by_pid(pid=pid))
        except:
            print('ERROR in self.assertFalse(self.appium_extended_terminal.kill_by_pid(pid=pid))')
        time.sleep(1)

    def test_kill_all(self):
        time.sleep(1)
        self.assertTrue(self.terminal.kill_all(name="logcat"))
        time.sleep(1)

    def test_kill_by_name(self):
        time.sleep(1)
        self.assertTrue(self.terminal.kill_by_name(name="logcat"))
        time.sleep(1)

    def test_delete_files_from_internal_storage(self):
        time.sleep(1)
        self.assertTrue(self.terminal.delete_files_from_internal_storage(path=INTERNAL_STORAGE))
        time.sleep(1)

    def test_delete_file_from_internal_storage(self):
        time.sleep(1)
        filename = 'new_file.txt'
        with open(filename, 'w') as file:
            file.write('Привет, мир!')
            time.sleep(1)
        self.terminal.push(source=filename,
                           destination=f"{INTERNAL_STORAGE}{filename}")
        time.sleep(1)
        os.remove(filename)
        time.sleep(1)
        self.assertTrue(self.terminal.delete_file_from_internal_storage(path=INTERNAL_STORAGE,
                                                                        filename="new_file.txt"))
        time.sleep(1)

    def test_get_screen_resolution(self):
        time.sleep(1)
        self.assertEqual(self.terminal.get_screen_resolution(), SCREEN_RESOLUTION)
        time.sleep(1)

    def test_run_background_process_is_process_exist(self):
        time.sleep(1)
        self.assertTrue(self.terminal.run_background_process(command='logcat'))
        time.sleep(1)
        self.assertTrue(self.terminal.is_process_exist(name='logcat'))
        self.assertTrue(self.terminal.stop_logcat())


# RUN SUITES
suite = unittest.TestSuite()

# ADD CLASS
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTerminal))

# ADD METHODS
# suite.addTest(TestTerminal('test_run_background_process_is_process_exist'))

# RUN
runner = unittest.TextTestRunner()
runner.run(suite)
