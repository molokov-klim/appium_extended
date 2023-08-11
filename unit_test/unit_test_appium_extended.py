# -*- coding: utf-8 -*-
# ТЕСТ APPIUM EXTENDED
import glob
import os
import unittest
import logging

import numpy as np
from PIL import Image

from appium_extended.appium_extended import AppiumExtended
from appium_extended_web_element.web_element_extended import WebElementExtended
from appium_extended_helpers.helpers_decorators import time_it
from appium_extended_utils import utils

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
outer_image_path = os.path.join('core', 'appium', 'unit_test', 'test_data', 'outer_image.png')
inner_image_path = os.path.join('core', 'appium', 'unit_test', 'test_data', 'inner_image.png')
start_position_image_path = os.path.join('core', 'appium', 'unit_test', 'test_data', 'start_position_image.png')
end_position_image_path = os.path.join('core', 'appium', 'unit_test', 'test_data', 'end_position_image.png')

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


class AppiumExtendedUTGet(unittest.TestCase):

    @time_it
    def test_get_element(self):
        logging.info("test_get_element()")

        element = app.get_element(locator=locator_recycler)
        self.assertIsInstance(element, WebElementExtended)

        element2 = app.get_element(locator=locator_tuple)
        self.assertIsInstance(element2, WebElementExtended)

        element3 = app.get_element(locator=element)
        self.assertIsInstance(element3, WebElementExtended)

        element4 = app.get_element(locator={"text": "Агенты. Поверенный"})
        self.assertIsInstance(element4, WebElementExtended)

        element5 = app.get_element(by=by, value=value)
        self.assertIsInstance(element5, WebElementExtended)

        element6 = app.get_element(locator=part_image)
        self.assertIsInstance(element6, WebElementExtended)

    @time_it
    def test_get_elements(self):
        tuple_elements = app.get_elements(locator=locators_tuple)
        self.assertIsInstance(tuple_elements[0], WebElementExtended)

        list_elements = app.get_elements(locator=tuple_elements)
        self.assertIsInstance(list_elements[0], WebElementExtended)

        dict_elements = app.get_elements(locator=locators_dict)
        self.assertIsInstance(dict_elements[0], WebElementExtended)

        str_elements = app.get_elements(locator=part_image_elements)
        self.assertIsInstance(str_elements[0], WebElementExtended)

        by_value_elements = app.get_elements(by=by, value=value)
        self.assertIsInstance(by_value_elements[0], WebElementExtended)

        tuple_range_elements = app.get_elements(locator=locators_tuple,
                                                elements_range=locators_tuple)
        self.assertIsInstance(tuple_range_elements[0], WebElementExtended)

        list_range_elements = app.get_elements(locator=dict_elements, elements_range=list_elements)
        self.assertIsInstance(list_range_elements[0], WebElementExtended)

        dict_range_elements = app.get_elements(locator=locators_tuple,
                                               elements_range=dict_elements)
        self.assertIsInstance(dict_range_elements[0], WebElementExtended)

    @time_it
    def test_get_image_coordinates(self):
        expected_result = (62, 828, 465, 871)

        # Проверка с использованием данных типа bytes
        with open(part_image, 'rb') as f:
            part_image_bytes = f.read()
        coord_bytes = app.get_image_coordinates(image=part_image_bytes)
        self.assertEqual(coord_bytes, expected_result)

        # Проверка с использованием данных типа np.ndarray
        part_image_array = np.array(Image.open(part_image))
        coord_array = app.get_image_coordinates(image=part_image_array)
        self.assertEqual(coord_array, expected_result)

        # Проверка с использованием данных типа PIL Image
        part_image_pil = Image.open(part_image)
        coord_pil = app.get_image_coordinates(image=part_image_pil)
        self.assertEqual(coord_pil, expected_result)

        # Проверка с использованием данных типа str (путь к файлу)
        coord_path = app.get_image_coordinates(image=part_image)
        self.assertEqual(coord_path, expected_result)

    @time_it
    def test_get_inner_image_coordinates(self):
        expected_result = (543, 700, 675, 753)

        # Проверка с использованием данных типа bytes
        with open(outer_image_path, 'rb') as f:
            outer_image_path_bytes = f.read()
        with open(inner_image_path, 'rb') as f:
            inner_image_path_bytes = f.read()
        coord_bytes = app.get_inner_image_coordinates(outer_image_path=outer_image_path_bytes,
                                                      inner_image_path=inner_image_path_bytes)
        self.assertEqual(coord_bytes, expected_result)

        # Проверка с использованием данных типа np.ndarray
        outer_image_array = np.array(Image.open(outer_image_path))
        inner_image_array = np.array(Image.open(inner_image_path))
        coord_array = app.get_inner_image_coordinates(outer_image_path=outer_image_array,
                                                      inner_image_path=inner_image_array)
        self.assertEqual(coord_array, expected_result)

        # Проверка с использованием данных типа PIL Image
        outer_image_pil = Image.open(outer_image_path)
        inner_image_pil = Image.open(inner_image_path)
        coord_pil = app.get_inner_image_coordinates(outer_image_path=outer_image_pil,
                                                    inner_image_path=inner_image_pil)
        self.assertEqual(coord_pil, expected_result)

        # Проверка с использованием данных типа str (путь к файлу)
        coord_path = app.get_inner_image_coordinates(outer_image_path=outer_image_path,
                                                     inner_image_path=inner_image_path)
        self.assertEqual(coord_path, expected_result)

    @time_it
    def test_get_text_coordinates(self):
        coord = app.get_text_coordinates(text='Агенты. Платежный агент')
        self.assertEqual(coord, (62, 839, 459, 862))
        coord = app.get_text_coordinates(text='Платежный агент', ocr=False)
        self.assertEqual(coord, (62, 828, 533, 871))


class AppiumExtendedUTIs(unittest.TestCase):

    @time_it
    def test_is_image_on_screen(self):
        # Проверка с использованием данных типа bytes
        with open(part_image, 'rb') as f:
            part_image_bytes = f.read()
        result_bytes = app.is_image_on_the_screen(image=part_image_bytes)
        self.assertTrue(result_bytes)

        # Проверка с использованием данных типа np.ndarray
        part_image_array = np.array(Image.open(part_image))
        result_array = app.is_image_on_the_screen(image=part_image_array)
        self.assertTrue(result_array)

        # Проверка с использованием данных типа PIL Image
        part_image_pil = Image.open(part_image)
        result_pil = app.is_image_on_the_screen(image=part_image_pil)
        self.assertTrue(result_pil)

        # Проверка с использованием данных типа str (путь к файлу)
        result_path = app.is_image_on_the_screen(image=part_image)
        self.assertTrue(result_path)

    @time_it
    def test_is_text_on_screen(self):
        logging.info("test_get_element()")
        result = app.is_text_on_screen(text="Агенты. Платежный агент")
        self.assertTrue(result)
        result = app.is_text_on_screen(text="Агенты. Платежный агент", ocr=False)
        self.assertTrue(result)


class AppiumExtendedUTOther(unittest.TestCase):

    @time_it
    def test_find_coordinates_by_image(self):
        expected_result = (62, 828, 465, 871)

        # Проверка с использованием данных типа bytes
        with open(part_image, 'rb') as f:
            part_image_bytes = f.read()
        result_bytes = app.get_image_coordinates(image=part_image_bytes)
        self.assertEqual(result_bytes, expected_result)

        # Проверка с использованием данных типа np.ndarray
        part_image_array = np.array(Image.open(part_image))
        result_array = app.get_image_coordinates(image=part_image_array)
        self.assertEqual(result_array, expected_result)

        # Проверка с использованием данных типа PIL Image
        part_image_pil = Image.open(part_image)
        result_pil = app.get_image_coordinates(image=part_image_pil)
        self.assertEqual(result_pil, expected_result)

        # Проверка с использованием данных типа str (путь к файлу)
        result_path = app.get_image_coordinates(image=part_image)
        self.assertEqual(result_path, expected_result)

    @time_it
    def test_find_many_coordinates_by_image(self):
        expected_result = [(543, 243, 675, 296), (543, 420, 675, 473), (543, 572, 675, 625),
                           (543, 699, 675, 752), (543, 826, 675, 879), (543, 953, 675, 1006)]

        # Проверка с использованием данных типа bytes
        with open(inner_image_path, 'rb') as f:
            inner_image_bytes = f.read()
        result_bytes = app.get_many_coordinates_of_image(image=inner_image_bytes)
        self.assertEqual(result_bytes, expected_result)

        # Проверка с использованием данных типа np.ndarray
        inner_image_array = np.array(Image.open(inner_image_path))
        result_array = app.get_many_coordinates_of_image(image=inner_image_array)
        self.assertEqual(result_array, expected_result)

        # Проверка с использованием данных типа PIL Image
        inner_image_pil = Image.open(inner_image_path)
        result_pil = app.get_many_coordinates_of_image(image=inner_image_pil)
        self.assertEqual(result_pil, expected_result)

        # Проверка с использованием данных типа str (путь к файлу)
        result_path = app.get_many_coordinates_of_image(image=inner_image_path)
        self.assertEqual(result_path, expected_result)

    @time_it
    def test_draw_by_coordinates(self):
        agent_001 = app.get_element({'text': 'Агенты. Банковский платежный агент'}).get_coordinates()
        agent_002 = app.get_element({'text': 'Агенты. Банковский платежный субагент'}).get_coordinates()
        agent_003 = app.get_element({'text': 'Агенты. Другой тип агента'}).get_coordinates()
        agent_004 = app.get_element({'text': 'Агенты. Комиссионер'}).get_coordinates()

        # Проверка с использованием данных типа bytes
        with open(screenshot, 'rb') as f:
            screenshot_bytes = f.read()
        name = 'screenshot_bytes.png'
        path = os.path.join('unit_test', 'test_results', name)
        result_bytes = app.draw_by_coordinates(image=screenshot_bytes, coordinates=agent_001, path=path)
        self.assertTrue(result_bytes)
        self.assertTrue(os.path.isfile(path))

        # Проверка с использованием данных типа np.ndarray
        screenshot_array = np.array(Image.open(screenshot))
        name = 'screenshot_array.png'
        path = os.path.join('unit_test', 'test_results', name)
        result_array = app.draw_by_coordinates(image=screenshot_array, coordinates=agent_002, path=path)
        self.assertTrue(result_array)
        self.assertTrue(os.path.isfile(path))

        # Проверка с использованием данных типа PIL Image
        screenshot_pil = Image.open(screenshot)
        name = 'screenshot_pil.png'
        path = os.path.join('unit_test', 'test_results', name)
        result_pil = app.draw_by_coordinates(image=screenshot_pil, coordinates=agent_003, path=path)
        self.assertTrue(result_pil)
        self.assertTrue(os.path.isfile(path))

        # Проверка с использованием данных типа str (путь к файлу)
        name = 'screenshot_str.png'
        path = os.path.join('unit_test', 'test_results', name)
        result_path = app.draw_by_coordinates(image=screenshot, coordinates=agent_004, path=path)
        self.assertTrue(result_path)
        self.assertTrue(os.path.isfile(path))


class AppiumExtendedUTFind(unittest.TestCase):

    @time_it
    def test_find_and_get_element(self):
        element = app.find_and_get_element(locator={'text': 'Характеристики'})
        self.assertEqual(element.get_attribute('text'), 'Характеристики')
        app.get_element(locator=locator_recycler).scroll_to_top()


class AppiumExtendedUTTap(unittest.TestCase):

    @time_it
    def test_tap_with_locator(self):
        locator = {"text": "Агенты. Поверенный"}
        result = app.tap(locator=locator)
        self.assertEqual(result, app)
        app.get_element(locator_back).click()

    @time_it
    def test_tap_with_coordinates(self):
        bounds = app.get_element(locator={"text": "Агенты. Поверенный"}).get_coordinates()
        x, y = utils.calculate_center_of_coordinates(coordinates=bounds)
        result = app.tap(x=x, y=y)
        self.assertEqual(result, app)
        app.get_element(locator_back).click()

    @time_it
    def test_tap_with_image(self):
        result = app.tap(image=part_image)
        self.assertEqual(result, app)
        app.get_element(locator_back).click()


class AppiumExtendedUTSwipe(unittest.TestCase):

    @time_it
    def test_swipe_with_element_locator(self):
        start_position = {'text': 'Комиссионер'}
        end_position = {'text': 'Платежный агент'}
        result = app.swipe(start_position=start_position, end_position=end_position)
        self.assertEqual(result, app)
        app.get_element(locator=locator_recycler).scroll_to_top()

    @time_it
    def test_swipe_with_element_coordinates(self):
        start_position = (465, 871)
        end_position = (300, 400)
        result = app.swipe(start_position=start_position, end_position=end_position)
        self.assertEqual(result, app)
        app.get_element(locator=locator_recycler).scroll_to_top()

    @time_it
    def test_swipe_with_image(self):
        start_position = start_position_image_path
        end_position = end_position_image_path
        result = app.swipe(start_position=start_position, end_position=end_position)
        self.assertEqual(result, app)
        app.get_element(locator=locator_recycler).scroll_to_top()

    @time_it
    def test_swipe_with_direction_and_distance(self):
        start_position = (465, 871)
        direction = 1
        distance = 100
        result = app.swipe(start_position=start_position, direction=direction, distance=distance)
        self.assertEqual(result, app)
        app.get_element(locator=locator_recycler).scroll_to_top()


# RUN SUITES
suite = unittest.TestSuite()

# ADD CLASS
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(AppiumExtendedUTGet))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(AppiumExtendedUTIs))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(AppiumExtendedUTOther))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(AppiumExtendedUTTap))  # ok
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(AppiumExtendedUTSwipe))  # ok

# ADD METHODS
# suite.addTest(AppiumExtendedUTFind('test_find_and_get_element'))


# RUN
runner = unittest.TextTestRunner()
runner.run(suite)

# app.get_element(locator=locator_tuple).get_attributes('text')

app.disconnect()
