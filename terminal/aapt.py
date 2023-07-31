import logging
import os

import config
from utils.operations import subprocess_check_output


class Aapt:
    def __init__(self):
        self.logger = logging.getLogger(config.APPIUM_LOG_NAME)

    @staticmethod
    def get_package_name(path_to_apk: str) -> str:
        """
        Получает название пакета APK-файла с помощью команды aapt.
        Возвращает название пакета.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.info(f"get_package_name() < {path_to_apk}")

        command = ["aapt", "dump", "badging", os.path.join(path_to_apk)]

        # Выполнение команды и получение вывода
        output: str = subprocess_check_output(command)

        # Извлечение строки, содержащей информацию о пакете
        start_index = output.index("package: name='") + len("package: name='")
        end_index = output.index("'", start_index)

        # Извлекаем название пакета
        package_name = output[start_index:end_index]

        logger.info(f"get_package_name() > {package_name}")
        # Возвращение названия пакета в виде строки
        return package_name

    @staticmethod
    def get_launchable_activity_from_apk(path_to_apk: str) -> str:
        """
        Получает название запускаемой активности из APK-файла с помощью команды aapt.
        Возвращает название активности в виде строки.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.info(f"get_launchable_activity_from_apk() < {path_to_apk}")

        command = ["aapt", "dump", "badging", path_to_apk]

        # Выполнение команды и получение вывода
        output = subprocess_check_output(command)

        # Извлечение строки, содержащей информацию о запускаемой активности
        package_line = [line for line in output.splitlines() if line.startswith("launchable-activity")][0]

        # Извлечение названия активности из строки
        launchable_activity = package_line.split("'")[1]

        # Возвращение названия активности в виде строки

        logger.info(f"get_launchable_activity_from_apk() > {launchable_activity}")
        return launchable_activity
