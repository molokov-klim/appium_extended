# ТЕСТ WEB ELEMENT EXTENDED
import glob
import inspect
import os
import time
import unittest

from appium_extended.appium_extended import AppiumExtended
from appium_extended_web_element.web_element_extended import WebElementExtended
from appium_extended_helpers.helpers_decorators import time_it

# logging.basicConfig(level=logging.DEBUG)

app = AppiumExtended()
caps = {
    "platformName": "android",
    "appium:automationName": "uiautomator2",
    # "appium:deviceName": adb.get_device_model(),
    # "appium:udid": adb.get_device_uuid(),
    "appium:noReset": True,
    "appium: autoGrantPermissions": True,
    "appium: newCommandTimeout": 600000,
}
app.connect(caps)
# logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])

# ELEMENT

locator_back = ("id", "ru.sigma.app.debug:id/backButton")

by = "xpath"
value = "//android.widget.TextView[contains(@text, 'Агенты')]"

locator_recycler = {"class": "androidx.recyclerview.widget.RecyclerView"}
locator_recycler_tuple = ('xpath',)

locator_tuple = ("xpath", "//android.widget.TextView[contains(@text, 'Агенты')]")
locator_dict = {"text": "Агенты", "enabled": "true"}

locator_tuple_elems = ("xpath", "//android.widget.TextView[contains(@scrollable, 'true')]")
locator_dict_elems = {'text': 'Агенты.', 'displayed': 'true'}

screenshot = os.path.join('core', 'appium', 'unit_test', 'test_data', 'screenshot.png')

part_image = os.path.join('core', 'appium', 'unit_test', 'test_data', 'part_image.png')
part_image_elements = os.path.join('core', 'appium', 'unit_test', 'test_data', 'part_image_elements.png')
bottom_blue_button = os.path.join('core', 'appium', 'unit_test', 'test_data', 'bottom_blue_button.png')

# ELEMENTS

locators_tuple = ("xpath", "//android.widget.TextView[contains(@text, 'Агенты')]")
locators_dict = {"text": "Агенты.",
                 "displayed": "true"}

# Создание папки test_results, если она не существует
test_results_dir = os.path.join('unit_test', 'test_results')
if not os.path.exists(test_results_dir):
    os.makedirs(test_results_dir)

# Очистка содержимого папки test_results
file_list = glob.glob(os.path.join(test_results_dir, "*"))
for file_path in file_list:
    os.remove(file_path)

print("===START UNIT TEST===")


class WebElementExtendedUTGet(unittest.TestCase):
    def test_get_element_by_locator_recycler(self):
        print("test_get_element_by_locator_recycler()")
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        element1 = element.get_element(locator=locator_recycler)
        inner_element = element1.get_element(locator=locator_tuple)
        self.assertIsInstance(inner_element, WebElementExtended)
        inner_element.click()
        app.get_element(locator_back).click(wait=True)

    def test_get_element_by_inner_element(self):
        print("test_get_element_by_inner_element()")
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        element2 = element.get_element(locator=locator_recycler)
        inner_element = element2.get_element(locator=locator_tuple)
        inner_element = element2.get_element(locator=inner_element)
        self.assertIsInstance(inner_element, WebElementExtended)
        inner_element.click()
        app.get_element(locator_back).click(wait=True)

    def test_get_element_by_text_locator(self):
        print("test_get_element_by_text_locator()")
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        element3 = element.get_element(locator=locator_recycler)
        inner_element = element3.get_element(locator={"text": "Агенты. Комиссионер"})
        self.assertIsInstance(inner_element, WebElementExtended)
        inner_element.click()
        app.get_element(locator_back).click(wait=True)

    def test_get_element_by_custom_locator(self):
        print("test_get_element_by_custom_locator()")
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        element4 = element.get_element(locator=locator_recycler)
        inner_element = element4.get_element(by=by, value=value)
        self.assertIsInstance(inner_element, WebElementExtended)
        inner_element.click()
        app.get_element(locator_back).click(wait=True)

    def test_get_element_by_part_image(self):
        print("test_get_element_by_part_image()")
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        element5 = element.get_element(locator=locator_recycler)
        inner_element = element5.get_element(locator=part_image)
        self.assertIsInstance(inner_element, WebElementExtended)
        inner_element.click()
        app.get_element(locator_back).click(wait=True)

    def test_get_attributes_text_only(self):
        print("test_get_attributes_text_only()")
        result = {'text': 'Агенты. Банковский платежный агент'}
        attributes = app.get_element(locator={'text': 'Агенты. Банковский платежный агент'}).get_attributes(['text'])
        self.assertEqual(attributes, result)

    def test_get_attributes_text_and_displayed(self):
        print("test_get_attributes_text_and_displayed()")
        result = {'text': 'Агенты. Банковский платежный агент', 'displayed': 'true'}
        attributes = app.get_element(locator={'text': 'Агенты. Банковский платежный агент'}).get_attributes(
            ['text', 'displayed'])
        self.assertEqual(attributes, result)

    def test_get_all_attributes(self):
        print("test_get_all_attributes()")
        result = {
            'index': '0',
            'package': 'ru.sigma.app.debug',
            'class': 'android.widget.TextView',
            'text': 'Агенты. Банковский платежный агент',
            'resource-id': 'ru.sigma.app.debug:id/categoryTitle',
            'checkable': 'false',
            'checked': 'false',
            'clickable': 'false',
            'enabled': 'true',
            'focusable': 'false',
            'focused': 'false',
            'long-clickable': 'false',
            'password': 'false',
            'scrollable': 'false',
            'selected': 'false',
            'bounds': '[62,220][533,313]',
            'displayed': 'true'
        }
        attributes = app.get_element(locator={'text': 'Агенты. Банковский платежный агент'}).get_attributes()
        self.assertEqual(attributes, result)


class WebElementExtendedUTDOM(unittest.TestCase):
    app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView')).scroll_to_top()

    @time_it
    def test_get_parent(self):
        self.assertIsInstance(app.get_element(
            locator={'text': 'Агенты. Платежный агент'}).get_parent(), WebElementExtended)

    @time_it
    def test_get_parents(self):
        elements = app.get_element(
            locator={'text': 'Агенты. Платежный агент'}).get_parents()
        self.assertIsInstance(elements[0], WebElementExtended)
        self.assertEqual(len(elements), 15)

    @time_it
    def test_get_sibling(self):
        element = app.get_element(
            locator={'index': "4", 'package': "ru.sigma.app.debug", 'class': "android.widget.FrameLayout", 'text': "",
                     'resource-id': "ru.sigma.app.debug:id/frontCard", 'checkable': "false", 'checked': "false",
                     'clickable': "true", 'enabled': "true", 'focusable': "false", 'focused': "false",
                     'long-clickable': "false", 'password': "false", 'scrollable': "false",
                     'selected': "false"}).get_sibling(
            attributes={'displayed': "true", 'clickable': "true", 'enabled': "true"})
        self.assertIsInstance(element, WebElementExtended)

    @time_it
    def test_get_siblings(self):
        elements = app.get_element(
            locator={'index': "4", 'package': "ru.sigma.app.debug", 'class': "android.widget.FrameLayout", 'text': "",
                     'resource-id': "ru.sigma.app.debug:id/frontCard", 'checkable': "false", 'checked': "false",
                     'clickable': "true", 'enabled': "true", 'focusable': "false", 'focused': "false",
                     'long-clickable': "false", 'password': "false", 'scrollable': "false",
                     'selected': "false"}).get_siblings()
        self.assertIsInstance(elements[0], WebElementExtended)
        self.assertEqual(len(elements), 6)

    @time_it
    def test_get_cousin(self):
        cousin = app.get_element(locator={'text': 'Агенты. Платежный агент'}).get_cousin(
            ancestor={'class': "androidx.recyclerview.widget.RecyclerView"},
            cousin={'class': "android.widget.TextView"})
        self.assertIsInstance(cousin, WebElementExtended)
        self.assertEqual(cousin.text, 'Агенты. Банковский платежный агент')

    @time_it
    def test_get_cousins(self):
        cousins = app.get_element(locator={'text': 'Агенты. Платежный агент'}).get_cousins(
            ancestor={'class': "androidx.recyclerview.widget.RecyclerView"},
            cousin={'class': "android.widget.TextView", 'text': 'Агенты.'}, contains=True)
        self.assertIsInstance(cousins[0], WebElementExtended)
        self.assertEqual(cousins[0].text, 'Агенты. Банковский платежный агент')
        self.assertEqual(len(cousins), 7)

    @time_it
    def test_is_contains(self):
        parent = app.get_element(locator={'text': 'Агенты. Платежный агент'}).get_parent()
        self.assertEqual(parent.is_contains(locator={'text': 'Агенты. Платежный агент'}), True)


class WebElementExtendedUTElements(unittest.TestCase):
    app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView')).scroll_to_top()

    @time_it
    def test_get_elements1(self):
        print("test_get_elements()")
        recycler_element = app.get_element(locator=locator_recycler)

        tuple_elements = recycler_element.get_elements(locator=locators_tuple)
        self.assertIsInstance(tuple_elements[0], WebElementExtended)
        self.assertEqual(len(tuple_elements), 7)

    @time_it
    def test_get_elements2(self):
        print("test_get_elements()")
        recycler_element = app.get_element(locator=locator_recycler)
        tuple_elements = recycler_element.get_elements(locator=locators_tuple)
        list_elements = recycler_element.get_elements(locator=tuple_elements)
        self.assertIsInstance(list_elements[0], WebElementExtended)
        self.assertEqual(len(list_elements), 7)

    @time_it
    def test_get_elements3(self):
        print("test_get_elements()")
        recycler_element = app.get_element(locator=locator_recycler)

        dict_elements = recycler_element.get_elements(locator=locators_dict)
        self.assertIsInstance(dict_elements[0], WebElementExtended)
        self.assertEqual(len(dict_elements), 7)

    @time_it
    def test_get_elements4(self):
        print("test_get_elements()")
        recycler_element = app.get_element(locator=locator_recycler)

        str_elements = recycler_element.get_elements(locator=part_image_elements)
        self.assertIsInstance(str_elements[0], WebElementExtended)
        self.assertEqual(len(str_elements), 7)

    @time_it
    def test_get_elements5(self):
        print("test_get_elements()")
        recycler_element = app.get_element(locator=locator_recycler)

        by_value_elements = recycler_element.get_elements(by=by, value=value)
        self.assertIsInstance(by_value_elements[0], WebElementExtended)
        self.assertEqual(len(by_value_elements), 7)

    @time_it
    def test_get_elements6(self):
        print("test_get_elements()")
        recycler_element = app.get_element(locator=locator_recycler)

        tuple_range_elements = recycler_element.get_elements(locator=locators_tuple,
                                                             elements_range=locators_tuple)
        self.assertIsInstance(tuple_range_elements[0], WebElementExtended)
        self.assertEqual(len(tuple_range_elements), 7)

    @time_it
    def test_get_elements7(self):
        print("test_get_elements()")
        recycler_element = app.get_element(locator=locator_recycler)
        dict_elements = recycler_element.get_elements(locator=locators_dict)
        tuple_elements = recycler_element.get_elements(locator=locators_tuple)
        list_elements = recycler_element.get_elements(locator=tuple_elements)
        list_range_elements = recycler_element.get_elements(locator=dict_elements, elements_range=list_elements)
        self.assertIsInstance(list_range_elements[0], WebElementExtended)
        self.assertEqual(len(list_range_elements), 7)

    @time_it
    def test_get_elements8(self):
        print("test_get_elements()")
        recycler_element = app.get_element(locator=locator_recycler)
        dict_elements = recycler_element.get_elements(locator=locators_dict)
        dict_range_elements = recycler_element.get_elements(locator=locators_tuple,
                                                            elements_range=dict_elements)
        self.assertIsInstance(dict_range_elements[0], WebElementExtended)
        self.assertEqual(len(dict_range_elements), 7)

    @time_it
    def test_get_elements9(self):
        print(inspect.currentframe().f_back.f_code.co_name)
        recycler_element = app.get_element(locator=locator_recycler)
        dict_elements = recycler_element.get_elements(locator=locators_dict)
        contains_elements = recycler_element.get_elements(locator={'text': 'Агенты. Другой тип агента'},
                                                          elements_range=dict_elements,
                                                          contains=False)
        print("Ошибка \"не удалось дождаться изменения окна\" - все ок, так и задумано")
        self.assertIsInstance(contains_elements[0], WebElementExtended)
        self.assertEqual(len(contains_elements), 1)


class WebElementExtendedUTClick(unittest.TestCase):
    @time_it
    def test_click1(self):
        self.assertIsInstance(app.get_element(locator=locator_tuple).click(), WebElementExtended)
        app.get_element(locator_back).click(wait=True)

    @time_it
    def test_click2(self):
        self.assertIsInstance(app.get_element(locator=locator_tuple).click(duration=3), WebElementExtended)
        app.get_element(locator_back).click(wait=True)

    @time_it
    def test_click3(self):
        self.assertIsInstance(app.get_element(locator=locator_tuple).click(duration=3, wait=True), WebElementExtended)
        app.get_element(locator_back).click(wait=True)

    @time_it
    def test_double_click1(self):
        # app.get_element(locator=locator_tuple).click()
        self.assertIsInstance(app.get_element(locator={'text': 'Банковский платежный агент'}).double_click(),
                              WebElementExtended)
        app.get_element(locator_back).click(wait=True)

    @time_it
    def test_double_click2(self):
        self.assertIsInstance(app.get_element(locator=locator_tuple).double_click(wait=True), WebElementExtended)
        app.get_element(locator_back).click(wait=True)

    @time_it
    def test_double_click3(self):
        app.get_element(locator=locator_tuple).click()
        app.get_element(locator_back).click(wait=True)

    @time_it
    def test_double_click4(self):
        self.assertIsInstance(app.get_element(locator={'text': 'Банковский платежный агент'}).double_click(wait=True),
                              WebElementExtended)
        app.get_element(locator_back).click(wait=True)

    @time_it
    def test_click_and_move1(self):
        self.assertIsInstance(
            app.get_element(locator={'text': 'Поверенный'}).click_and_move(locator={'text': 'Товары'}),
            WebElementExtended)

    @time_it
    def test_click_and_move2(self):
        self.assertIsInstance(app.get_element(locator=({'text': 'Агенты'})).click_and_move(
            locator=bottom_blue_button), WebElementExtended)

    @time_it
    def test_click_and_move3(self):
        self.assertIsInstance(app.get_element(locator={'text': 'Поверенный'}).click_and_move(locator=app.get_element(
            {'text': 'Товары'})), WebElementExtended)

    @time_it
    def test_click_and_move4(self):
        self.assertIsInstance(app.get_element(locator=({'text': 'Поверенный'})).click_and_move(
            locator=bottom_blue_button), WebElementExtended)

    @time_it
    def test_click_and_move5(self):
        self.assertIsInstance(app.get_element(locator={'text': 'Поверенный'}).click_and_move(
            x=360, y=1184), WebElementExtended)

    @time_it
    def test_click_and_move6(self):
        self.assertIsInstance(app.get_element(locator=({'text': 'Поверенный'})).click_and_move(
            direction=0, distance=10000), WebElementExtended)

    @time_it
    def test_click_and_move7(self):
        self.assertIsInstance(app.get_element(locator=({'text': 'Расходники'})).click_and_move(
            direction=180, distance=10000), WebElementExtended)


class WebElementExtendedUTap(unittest.TestCase):
    app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView')).scroll_to_top()

    @time_it
    def test_tap(self):
        self.assertIsInstance(app.get_element(locator={'text': 'Банковский платежный'}).tap(wait=False),
                              WebElementExtended)
        app.get_element(locator=locator_back).tap(wait=True)

    @time_it
    def test_tap_and_wait(self):
        self.assertIsInstance(app.get_element(locator={'text': 'Банковский платежный'}).tap(wait=True),
                              WebElementExtended)
        app.get_element(locator=locator_back).tap(wait=True)

    @time_it
    def test_double_tap_1(self):
        self.assertIsInstance(
            app.get_element(locator={'text': 'Банковский платежный'}).double_tap(wait=False, pause=0.1),
            WebElementExtended)
        app.get_element(locator=locator_back).tap(wait=True)

    @time_it
    def test_double_tap_4(self):
        self.assertIsInstance(
            app.get_element(locator={'text': 'Банковский платежный'}).double_tap(wait=False, pause=0.4),
            WebElementExtended)
        app.get_element(locator=locator_back).tap(wait=True)

    @time_it
    def test_double_tap_and_wait(self):
        self.assertIsInstance(app.get_element(locator={'text': 'Банковский платежный'}).double_tap(wait=True),
                              WebElementExtended)
        app.get_element(locator=locator_back).tap(wait=True)

    @time_it
    def test_tap_and_move(self):
        self.assertIsInstance(app.get_element(locator={'text': 'Поверенный'}).tap_and_move(locator={'text': 'Товары'}),
                              WebElementExtended)
        self.assertIsInstance(app.get_element(locator=({'text': 'ПСН'})).tap_and_move(
            locator=bottom_blue_button), WebElementExtended)
        self.assertIsInstance(app.get_element(locator={'text': 'Поверенный'}).tap_and_move(locator=app.get_element(
            {'text': 'Товары'})), WebElementExtended)
        self.assertIsInstance(app.get_element(locator=({'text': 'ПСН'})).tap_and_move(
            locator=bottom_blue_button), WebElementExtended)
        self.assertIsInstance(app.get_element(locator={'text': 'Поверенный'}).tap_and_move(
            x=360, y=1184), WebElementExtended)
        self.assertIsInstance(app.get_element(locator=({'text': 'Поверенный'})).tap_and_move(
            direction=0, distance=10000), WebElementExtended)
        self.assertIsInstance(app.get_element(locator=({'text': 'Расходники'})).tap_and_move(
            direction=180, distance=10000), WebElementExtended)


class WebElementExtendedUTAdbActions(unittest.TestCase):
    app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView')).scroll_to_top()

    @time_it
    def test_adb_tap(self):
        element = app.get_element(locator={'text': 'Комиссионер'})
        self.assertIsInstance(element.adb_tap(), WebElementExtended)
        time.sleep(3)
        app.get_element(locator=locator_back).click(wait=True)
        time.sleep(3)

    @time_it
    def test_adb_multi_tap(self):
        element = app.get_element(locator={'text': 'Комиссионер'})
        self.assertIsInstance(element.adb_multi_tap(), WebElementExtended)
        time.sleep(3)
        app.get_element(locator=locator_back).click(wait=True)
        time.sleep(3)

    @time_it
    def test_adb_swipe(self):
        element = app.get_element(locator={'text': 'Комиссионер'})
        self.assertIsInstance(element.adb_swipe(locator={'text': 'Подытог'}), WebElementExtended)
        element = app.get_element(locator={'text': 'Комиссионер'})
        self.assertIsInstance(element.adb_swipe(x=300, y=250), WebElementExtended)
        self.assertIsInstance(element.adb_swipe(direction=180, distance=50), WebElementExtended)


class WebElementExtendedUTScroll(unittest.TestCase):
    app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView')).scroll_to_top()

    @time_it
    def test_scroll_down(self):
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        self.assertIsInstance(element.scroll_down(), WebElementExtended)
        self.assertIsInstance(element.scroll_down(locator={'class': 'android.view.ViewGroup'}), WebElementExtended)
        self.assertIsInstance(element.scroll_down(locator={'class': 'android.view.ViewGroup'}, duration=30),
                              WebElementExtended)

    @time_it
    def test_scroll_up(self):
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        self.assertIsInstance(element.scroll_up(), WebElementExtended)
        self.assertIsInstance(element.scroll_up(locator={'class': 'android.view.ViewGroup'}), WebElementExtended)
        self.assertIsInstance(element.scroll_up(locator={'class': 'android.view.ViewGroup'}, duration=30),
                              WebElementExtended)

    @time_it
    def test_scroll_to_bottom(self):
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        self.assertIsInstance(element.scroll_to_bottom(), WebElementExtended)
        self.assertIsInstance(element.scroll_to_bottom(locator={'class': 'android.view.ViewGroup'}),
                              WebElementExtended)

    @time_it
    def test_scroll_to_top(self):
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        self.assertIsInstance(element.scroll_to_top(), WebElementExtended)
        self.assertIsInstance(element.scroll_to_top(locator={'class': 'android.view.ViewGroup'}),
                              WebElementExtended)

    @time_it
    def test_scroll_until_find(self):
        element = app.get_element(locator=('id', 'ru.sigma.app.debug:id/menuRecyclerView'))
        self.assertIsInstance(element.scroll_until_find(locator={'text': 'Характеристики'}), WebElementExtended)
        self.assertIsInstance(element.scroll_to_top(), WebElementExtended)
        self.assertIsInstance(element.scroll_until_find(locator={'text': 'актер'}), WebElementExtended)
        self.assertIsInstance(element.scroll_to_top(), WebElementExtended)


# CREATE SUITE
suite = unittest.TestSuite()

# ADD CLASS TO SUITE
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WebElementExtendedUTGet))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WebElementExtendedUTClick))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WebElementExtendedUTDOM))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WebElementExtendedUTElements))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WebElementExtendedUTAdbActions))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WebElementExtendedUTap))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WebElementExtendedUTScroll))  # ok

# RUN
runner = unittest.TextTestRunner()
runner.run(suite)

app.disconnect()
