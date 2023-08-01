import logging
import re
import subprocess
import sys
import time
import traceback
from typing import Dict, Union, Tuple
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(
#    __file__))))  # The sys.path.append line adds the parent directory of the tests directory to the Python module search path, allowing you to import modules from the root folder.

import config


class Adb:
    def __init__(self):
        self.logger = logging.getLogger(config.APPIUM_LOG_NAME)

    @staticmethod
    def get_device_uuid() -> Union[str, None]:
        """
        Получает UUID подключенного устройства Android с помощью команды adb.
        Returns:
            UUID в виде строки.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("get_device_uuid()")

        # Определение команды для выполнения с помощью adb для получения списка устройств
        command = ['adb', 'devices']

        try:
            # Выполнение команды и получение вывода
            response = subprocess.check_output(command)

            # Извлечение списка устройств из полученного вывода с использованием регулярных выражений
            device_list = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+|\d+)', response)

            # Возвращение первого устройства из списка (UUID подключенного устройства Android)
            logger.debug(f"get_device_uuid() > {device_list[0]}")

            return device_list[0]

        except subprocess.CalledProcessError as e:
            logger.error("get_device_uuid() > None")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)

    @staticmethod
    def get_device_model() -> Union[str, None]:
        """
        Получает модель подключенного устройства Android с помощью команды adb.
        Возвращает модель устройства.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("get_device_model()")

        command = ["adb", "shell", "getprop", "ro.product.model"]
        try:
            # Выполнение команды и получение вывода
            model = subprocess.check_output(command)
            # Возвращение модели устройства в виде строки
            logger.debug(f"get_device_model() > {model}")
            return model
        except subprocess.CalledProcessError as e:
            logger.error("get_device_model() > None")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)

    @staticmethod
    def push(source: str, destination: str) -> bool:
        """
        Копирует файл или директорию на подключенное устройство.

        Аргументы:
            source (str): Путь к копируемому файлу или директории.
            destination (str): Путь назначения на устройстве.

        Возвращает:
            bool: True, если файл или директория были успешно скопированы, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"push() < {source=}, {destination=}")

        command = ["adb", "push", source, destination]
        try:
            subprocess.run(command, check=True)
            logger.debug("push() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("push() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def pull(source: str, destination: str) -> bool:
        """
        Копирует файл или директорию с подключенного устройства.

        Аргументы:
            source (str): Путь к исходному файлу или директории на устройстве.
            destination (str): Целевой путь для сохранения скопированного файла или директории.

        Возвращает:
            bool: True, если файл или директория были успешно скопированы, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"pull() < {source=}, {destination=}")

        command = ["adb", "pull", source, destination]
        try:
            subprocess.run(command, check=True)
            logger.debug("pull() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("pull() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def install(source: str) -> bool:
        """
        Устанавливает файл APK на подключенном устройстве.

        Аргументы:
            source (str): Путь к файлу APK для установки.

        Возвращает:
            bool: True, если файл APK был успешно установлен, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"install() < {source=}")

        command = ["adb", "install", "-r", source]
        try:
            subprocess.run(command, check=True)
            logger.debug("install() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("install() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def start_activity(package: str, activity: str) -> bool:
        """
        Запускает активность на подключенном устройстве.

        Аргументы:
            package (str): Название пакета активности.
            activity (str): Название запускаемой активности.

        Возвращает:
            bool: True, если активность была успешно запущена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"start_activity() < {package=}, {activity=}")

        command = ['adb', 'shell', 'am', 'start', '-n', f'{package}/{activity}']
        try:
            subprocess.check_output(command)
            logger.debug("start_activity() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("start_activity() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def close_app(package: str) -> bool:
        """
        Принудительно останавливает указанный пакет с помощью ADB.
    
        Аргументы:
            package (str): Название пакета приложения для закрытия.
    
        Возвращает:
            bool: True, если приложение успешно закрыто, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"close_app() < {package=}")

        command = ['adb', 'shell', 'am', 'force-stop', package]
        try:
            subprocess.run(command, check=True)
            logger.debug("close_app() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("close_app() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    def reboot_app(self, package: str, activity: str) -> bool:
        """
        Перезапускает приложение, закрывая его и затем запуская указанную активность.

        Аргументы:
            package (str): Название пакета приложения.
            activity (str): Название активности для запуска.

        Возвращает:
            bool: True, если перезапуск приложения выполнен успешно, False в противном случае.
        """
        self.logger.debug(f"reboot_app() < {package=}, {activity=}")

        # Закрытие приложения
        if not self.close_app(package=package):
            self.logger.error("reboot_app() > False")
            return False

        # Запуск указанной активности
        if not self.start_activity(package=package, activity=activity):
            self.logger.error("reboot_app() > False")
            return False
        self.logger.debug("reboot_app() > True")
        return True

    @staticmethod
    def uninstall_app(package: str) -> bool:
        """
        Удаляет указанный пакет с помощью ADB.

        Аргументы:
            package (str): Название пакета приложения для удаления.

        Возвращает:
            bool: True, если приложение успешно удалено, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"uninstall_app() < {package=}")

        command = ['adb', 'uninstall', package]
        try:
            subprocess.run(command, check=True)
            logger.debug("uninstall_app() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("uninstall_app() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def press_home() -> bool:
        """
        Отправляет событие нажатия кнопки Home на устройство с помощью ADB.

        Возвращает:
            bool: True, если команда была успешно выполнена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("press_home()")

        command = ['adb', 'shell', 'input', 'keyevent', 'KEYCODE_HOME']
        try:
            subprocess.run(command, check=True)
            logger.debug("press_home() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("press_home() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def press_back() -> bool:
        """
        Отправляет событие нажатия кнопки Back на устройство с помощью ADB.

        Возвращает:
            bool: True, если команда была успешно выполнена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("press_back()")

        command = ['adb', 'shell', 'input', 'keyevent', 'KEYCODE_BACK']
        try:
            subprocess.run(command, check=True)
            logger.debug("press_back() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("press_back() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def press_menu() -> bool:
        """
        Отправляет событие нажатия кнопки Menu на устройство с помощью ADB.

        Возвращает:
            bool: True, если команда была успешно выполнена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("press_menu()")

        command = ['adb', 'shell', 'input', 'keyevent', 'KEYCODE_MENU']
        try:
            subprocess.run(command, check=True)
            logger.debug("press_menu() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("adb.press_menu() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def input_keycode_num_(num: int) -> bool:
        """
        Отправляет событие нажатия клавиши с числовым значением на устройство с помощью ADB.
        Допустимые значения: 0-9, ADD, COMMA, DIVIDE, DOT, ENTER, EQUALS

        Аргументы:
            num (int): Числовое значение клавиши для нажатия.

        Возвращает:
            bool: True, если команда была успешно выполнена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"input_keycode_num_() < {num=}")

        command = ['adb', 'shell', 'input', 'keyevent', f'KEYCODE_NUMPAD_{num}']
        try:
            subprocess.run(command, check=True)
            logger.debug("input_keycode_num_() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("input_keycode_num_() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def input_keycode(keycode: str) -> bool:
        """
        Вводит указанный код клавиши на устройстве с помощью ADB.

        Аргументы:
            keycode (str): Код клавиши для ввода.

        Возвращает:
            bool: True, если команда была успешно выполнена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"input_keycode() < {keycode=}")

        command = ['adb', 'shell', 'input', 'keyevent', f'{keycode}']
        try:
            subprocess.run(command, check=True)
            logger.debug("input_keycode() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("input_keycode() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    def input_by_virtual_keyboard(self, text: str, keyboard: Dict[str, tuple]) -> bool:
        """
        Вводит строку символов с помощью виртуальной клавиатуры.

        Аргументы:
            key (str): Строка символов для ввода.
            keyboard (dict): Словарь с маппингом символов на координаты нажатий.

        Возвращает:
            bool: True, если ввод выполнен успешно, False в противном случае.
        """
        self.logger.debug(f"input_by_virtual_keyboard() < {text=}, {keyboard=}")

        try:
            for char in text:
                # Вызываем функцию tap с координатами, соответствующими символу char
                self.tap(*keyboard[char])
            self.logger.debug("input_by_virtual_keyboard() > True")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error("input_by_virtual_keyboard() > False")
            self.logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            self.logger.error(traceback_info)
            return False

    @staticmethod
    def input_text(text: str) -> bool:
        """
        Вводит указанный текст на устройстве с помощью ADB.

        Аргументы:
            text (str): Текст для ввода.

        Возвращает:
            bool: True, если команда была успешно выполнена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"input_text() < {text=}")

        # Формируем команду для ввода текста с использованием ADB
        command = ['adb', 'shell', 'input', 'text', text]
        try:
            # Выполняем команду
            subprocess.run(command, check=True)
            logger.debug("input_text() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("input_text() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def tap(x: Union[str, int], y: Union[str, int]) -> bool:
        """
        Выполняет нажатие на указанные координаты на устройстве с помощью ADB.

        Аргументы:
            x: Координата X для нажатия.
            y: Координата Y для нажатия.

        Возвращает:
            bool: True, если команда была успешно выполнена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"tap() < {x=}, {y=}")

        # Формируем команду для выполнения нажатия по указанным координатам с использованием ADB
        command = ['adb', 'shell', 'input', 'tap', str(x), str(y)]
        try:
            subprocess.run(command, check=True)
            logger.debug("tap() > True")
            return True
        except subprocess.CalledProcessError as e:
            logger.error("tap() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def swipe(start_x: Union[str, int], start_y: Union[str, int],
              end_x: Union[str, int], end_y: Union[str, int],
              duration: int = 300) -> bool:
        """
        Выполняет свайп (перетаскивание) с одной точки на экране в другую на устройстве с помощью ADB.

        Аргументы:
            start_x: Координата X начальной точки свайпа.
            start_y: Координата Y начальной точки свайпа.
            end_x: Координата X конечной точки свайпа.
            end_y: Координата Y конечной точки свайпа.
            duration (int): Длительность свайпа в миллисекундах (по умолчанию 300).

        Возвращает:
            bool: True, если команда была успешно выполнена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"swipe() < {start_x=}, {start_y=}, {end_x=}, {end_y=}, {duration=}")

        # Формируем команду для выполнения свайпа с использованием ADB
        command = ['adb', 'shell', 'input', 'swipe', str(start_x), str(start_y), str(end_x), str(end_y), str(duration)]
        try:
            # Выполняем команду
            subprocess.run(command, check=True)
            logger.debug("swipe() > True")
            return True
        except subprocess.CalledProcessError as e:
            # Логируем ошибку, если возникло исключение
            logger.error("swipe() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def get_current_app_package() -> Union[str, None]:
        """
        Получает пакет текущего запущенного приложения на устройстве с помощью ADB.

        Возвращает:
            str: Название пакета текущего запущенного приложения, либо None, если произошла ошибка.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("get_current_app_package()")

        # Определяем команду в виде списка строк
        command = [
            "adb", "shell", "dumpsys", "window", "windows", "|", "grep", "-E", "'mCurrentFocus|mFocusedApp'",
            "|", "grep", "-e", "'mFo'"
        ]
        try:
            # Выполняем команду и получаем результат
            result = str(subprocess.check_output(command)).strip()
            # Находим позицию последнего вхождения подстроки "/." в строке
            end_index = result.rfind("/")
            # Извлекаем название приложения из предшествующих символов
            start_index = result.rfind(" ", 0, end_index) + 1
            app_name = result[start_index:end_index]
            logger.debug(f"get_current_app_package() > {app_name=}")
            return app_name
        except subprocess.CalledProcessError as e:
            # Логируем ошибку, если возникло исключение
            logger.error("adb.get_current_app_package() > None")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return None

    @staticmethod
    def check_vpn(ip_address: str = '') -> bool:
        """
        Проверяет, активно ли VPN-соединение на устройстве с помощью ADB.

        Аргументы:
            ip_address (str): IP-адрес для проверки VPN-соединения. Если не указан, используется значение из конфигурации.

        Возвращает:
            bool: True, если VPN-соединение активно, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"check_VPN() < {ip_address=}")

        # Определяем команду в виде строки
        command = f"adb shell netstat | grep -w -e {ip_address}"
        try:
            # Выполняем команду и получаем вывод
            output = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

            if "ESTABLISHED" in output.stdout:
                logger.debug("check_VPN() True")
                return True
            logger.debug("check_VPN() False")
            return False
        except subprocess.CalledProcessError as e:
            # Логируем ошибку, если возникло исключение
            logger.error("check_VPN() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

    @staticmethod
    def stop_logcat() -> bool:
        """
        Останавливает выполнение logcat на устройстве с помощью ADB.

        Возвращает:
            bool: True, если выполнение logcat остановлено успешно, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("stop_logcat()")

        command = ['adb', 'shell', 'ps', '|', 'grep', 'logcat']
        # Получаем список выполняющихся процессов logcat
        try:
            process_list = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            logger.error("adb.stop_logcat() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        # Проходим по списку процессов и отправляем каждому сигнал SIGINT
        for process in process_list.splitlines():
            pid = process.split()[1]
            try:
                subprocess.call(['adb', 'shell', 'kill', '-s', 'SIGINT', pid])
            except subprocess.CalledProcessError as e:
                logger.error("adb.stop_logcat() > False")
                logger.error(e)
                traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
                logger.error(traceback_info)
                return False
        logger.debug("stop_logcat() > True")
        return True

    @staticmethod
    def reload_adb() -> bool:
        """
        Перезапускает adb-сервер на устройстве.

        Возвращает:
            bool: True, если adb-сервер успешно перезапущен, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("reload_adb()")

        try:
            command = ['adb', 'kill-server']
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            logger.error("reload_adb() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        # Ожидаем некоторое время перед запуском adb-сервера
        time.sleep(3)
        try:
            command = ['adb', 'start-server']
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            logger.error("reload_adb() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        logger.debug("reload_adb() > True")
        return True

    @staticmethod
    def know_pid(name: str) -> Union[int, None]:
        """
        Находит Process ID (PID) процесса по его имени, используя adb shell ps.

        Параметры:
            name (str): Имя процесса, PID которого нужно найти.

        Возвращает:
            Union[int, None]: PID процесса, если он найден, или None, если процесс не найден.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"know_pid() < {name=}")
        command = ['adb', 'shell', 'ps']
        try:
            processes = str(subprocess.call(command)).strip()
        except subprocess.CalledProcessError as e:
            logger.error("know_pid() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        if name not in processes:
            logger.error("know_pid() > False")
            logger.error("know_pid() [Процесс не обнаружен]")
            return False
        # Разделение вывода на строки и удаление пустых строк
        lines = processes.strip().split('\n')
        # Проход по каждой строке вывода, начиная с 2-й строки, игнорируя заголовки
        for line in lines[1:]:
            # Разделение строки на столбцы по пробелам
            columns = line.split()
            # Проверка, что строка имеет не менее 9 столбцов
            if len(columns) >= 9:
                # Извлечение PID и имени процесса из соответствующих столбцов
                pid, process_name = columns[1], columns[8]
                # Сравнение имени процесса с искомым именем
                if name == process_name:
                    logger.debug(f"know_pid() > {pid=}")
                    return int(pid)
        # Возврат None, если процесс с заданным именем не найден
        logger.error("know_pid() > None")
        return None

    @staticmethod
    def kill_by_pid(pid: str) -> bool:
        """
        Отправляет сигнал SIGINT для остановки процесса по указанному идентификатору PID с помощью ADB.

        Аргументы:
            pid (str): Идентификатор PID процесса для остановки.

        Возвращает:
            bool: True, если процесс успешно остановлен, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"kill_by_pid() < {pid=}")

        command = ['adb', 'shell', 'kill', '-s', 'SIGINT', str(pid)]
        try:
            subprocess.call(command)
        except subprocess.CalledProcessError as e:
            logger.error("kill_by_pid() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        logger.debug("kill_by_pid() > True")
        return True

    @staticmethod
    def kill_by_name(name: str) -> bool:
        """
        Останавливает все процессы с указанным именем на устройстве с помощью ADB.

        Аргументы:
            name (str): Имя процесса для остановки.

        Возвращает:
            bool: True, если все процессы успешно остановлены, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"kill_by_name() < {name=}")

        command = ['adb', 'shell', 'pkill', '-l', 'SIGINT', str(name)]
        try:
            subprocess.call(command)
        except subprocess.CalledProcessError as e:
            logger.error("kill_by_name() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        logger.debug("kill_by_name() > True")
        return True

    @staticmethod
    def kill_all(name: str) -> bool:
        """
        Останавливает все процессы, соответствующие указанному имени, на устройстве с помощью ADB.

        Аргументы:
            name (str): Имя процесса или шаблон имени для остановки.

        Возвращает:
            bool: True, если все процессы успешно остановлены, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"kill_all() < {name=}")

        command = ['adb', 'shell', 'pkill', '-f', str(name)]
        try:
            subprocess.call(command)
        except subprocess.CalledProcessError as e:
            logger.error("kill_all() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        logger.debug("kill_all() > True")
        return True

    @staticmethod
    def delete_files_from_internal_storage(path: str) -> bool:
        """
        Удаляет файлы из внутреннего хранилища устройства с помощью ADB.

        Аргументы:
            path (str): Путь к файлам для удаления.

        Возвращает:
            bool: True, если файлы успешно удалены, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"delete_files_from_internal_storage() < {path=}")

        command = ['adb', 'shell', 'rm', '-rf', f'{path}*']
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            logger.error("delete_files_from_internal_storage() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        logger.debug("delete_files_from_internal_storage() > True")
        return True

    @staticmethod
    def pull_video(wherefrom: str = None, destination: str = "", delete: bool = True) -> bool:
        """
        Копирует видеофайлы с устройства на компьютер с помощью ADB.

        Аргументы:
            wherefrom (str): Путь к исходным видеофайлам на устройстве.
            destination (str): Путь для сохранения скопированных видеофайлов.
            delete (bool): Удалять исходные видеофайлы с устройства после копирования (по умолчанию True).

        Возвращает:
            bool: True, если видеофайлы успешно скопированы, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"pull_video() < {destination=}")

        if not wherefrom:
            wherefrom = '/sdcard/Movies/'
        if wherefrom.endswith('/'):
            wherefrom = wherefrom + "/"
        if destination.endswith('/'):
            destination = destination + "/"

        command = ['adb', 'pull', f'{wherefrom}', f'{destination}']
        try:
            with subprocess.Popen(command) as process:
                process.communicate()
            time.sleep(30)
        except subprocess.CalledProcessError as e:
            logger.error("pull_video() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

        if delete:
            command = ['adb', 'shell', 'rm', '-rf', f'{wherefrom}*']
            try:
                with subprocess.Popen(command) as process:
                    process.communicate()
            except subprocess.CalledProcessError as e:
                logger.error("pull_video() > False")
                logger.error(e)
                traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
                logger.error(traceback_info)
                return False

            logger.debug("pull_video() > True")
        return True

    @staticmethod
    def stop_video() -> bool:
        """
        Останавливает запись видео на устройстве с помощью ADB.

        Возвращает:
            bool: True, если запись видео успешно остановлена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("stop_video()")

        command = ['adb', 'shell', 'pkill', '-l', 'SIGINT', 'screenrecord']
        try:
            subprocess.call(command)
        except subprocess.CalledProcessError as e:
            logger.error("stop_video() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        logger.debug("stop_video() > True")
        return True

    @staticmethod
    def record_video(filename: str) -> bool:
        """
        Записывает видео на устройстве с помощью ADB.

        Аргументы:
            filename (str): Имя файла для сохранения видео.

        Возвращает:
            bool: True, если запись видео успешно начата, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug(f"record_video() < {filename}")

        command = ['adb', 'shell', 'screenrecord', f'sdcard/Movies/{filename}']
        try:
            # Запускаем команду adb shell screenrecord для начала записи видео
            with subprocess.Popen(command) as process:
                # Ожидаем завершения процесса записи видео
                process.communicate()
        except subprocess.CalledProcessError as e:
            # Если произошла ошибка при выполнении команды, логируем ошибку и возвращаем False
            logger.error("record_video() > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False

        # Возвращаем True, т.к. запись видео начата успешно
        logger.debug("record_video() > True")
        return True

    @staticmethod
    def reboot() -> bool:
        """
        Перезагружает устройство с помощью ADB.

        Возвращает:
            bool: True, если перезагрузка успешно запущена, False в противном случае.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("reboot()")

        command = ['adb', 'shell', 'reboot']
        try:
            subprocess.call(command)
        except subprocess.CalledProcessError as e:
            logger.error("reboot > False")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return False
        logger.debug("reboot() > True")
        return True

    @staticmethod
    def get_screen_resolution() -> Union[Tuple[int, int], None]:
        """
        Возвращает разрешение экрана устройства с помощью ADB.

        Возвращает:
            tuple[int, int] or None: Кортеж с шириной и высотой экрана в пикселях, или None в случае ошибки.
        """
        logger = logging.getLogger(config.APPIUM_LOG_NAME)
        logger.debug("get_screen_resolution()")

        command = ['adb', 'shell', 'wm', 'size']
        try:
            output = str(subprocess.run(command, check=True)).strip()
            if "Physical size" in output:
                resolution_str = output.split(":")[1].strip()
                width, height = resolution_str.split("x")
                logger.debug(f"get_screen_resolution() > {width=}, {height=}")
                return int(width), int(height)
        except subprocess.CalledProcessError as e:
            logger.error("get_screen_resolution() > None")
            logger.error(e)
            traceback_info = "".join(traceback.format_tb(sys.exc_info()[2]))
            logger.error(traceback_info)
            return None

