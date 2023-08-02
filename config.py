import os.path
import getpass


# Appium
APPIUM_LOG_NAME = 'appium_ext'
APPIUM_LOG_LEVEL = 'debug'

APPIUM_IP = '10.77.124.25'
APPIUM_PORT = '4723'


# TODO УДАЛИТЬ ПОСЛЕ ИЗБАВЛЕНИЯ ОТ ФЛАСКА
# Вместо этого использовать ~driver.execute_script('mobile : shell', command)
# PROXY
PROXY = False        # если pytest запускается с другой машины, тогда используется Flask для проксирования cmd команд

# Flask
FLASK_IP = '10.77.124.25'
FLASK_PORT = '5555'




