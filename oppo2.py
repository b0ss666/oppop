from datetime import datetime
import re
from typing import List, Tuple, Dict, Callable


class PressureMeasurement:
    """Класс для хранения данных измерения давления."""

    def __init__(self, date: str, height: float, value: int):
        """Инициализирует измерение давления.

        Args:
            date: Дата в формате ГГГГ.ММ.ДД
            height: Высота в метрах
            value: Значение давления в Па
        """
        self.date = date
        self.height = height
        self.value = value

    def date_as_datetime(self) -> datetime:
        """Преобразует строковую дату в объект datetime.

        Returns:
            Объект datetime
        """
        return datetime.strptime(self.date, "%Y.%m.%d")

    def __str__(self) -> str:
        """Возвращает строковое представление измерения.

        Returns:
            Отформатированная строка с данными измерения
        """
        return f"{self.date:12} | {self.height:8.1f} м | {self.value:6} Па"


class PressureParser:
    """Парсер для строк с данными измерения давления."""

    # Регулярное выражение для парсинга: ГГГГ.ММ.ДД число число
    _PATTERN = r'^(\d{4}\.\d{2}\.\d{2})\s+(\d+(?:\.\d+)?)\s+(\d+)$'

    @classmethod
    def parse(cls, input_str: str) -> PressureMeasurement:
        """Парсит строку и создает объект измерения.

        Args:
            input_str: Входная строка в формате "ГГГГ.ММ.ДД ВЫСОТА ЗНАЧЕНИЕ"

        Returns:
            Объект PressureMeasurement

        Raises:
            ValueError: При неверном формате или некорректных значениях
        """
        cls._validate_format(input_str)
        date, height, value = cls._extract_values(input_str)
        cls._validate_date(date)
        cls._validate_measurement_values(height, value)

        return PressureMeasurement(date, height, value)

    @classmethod
    def _validate_format(cls, input_str: str) -> None:
        """Проверяет формат входной строки.

        Args:
            input_str: Входная строка

        Raises:
            ValueError: При неверном формате строки
        """
        if not re.match(cls._PATTERN, input_str.strip()):
            raise ValueError("Неверный формат. Используйте: ГГГГ.ММ.ДД ВЫСОТА ЗНАЧЕНИЕ")

    @classmethod
    def _extract_values(cls, input_str: str) -> Tuple[str, float, int]:
        """Извлекает значения из строки.

        Args:
            input_str: Входная строка

        Returns:
            Кортеж (дата, высота, значение)
        """
        match = re.match(cls._PATTERN, input_str.strip())
        date = match.group(1)
        height = float(match.group(2))
        value = int(match.group(3))
        return date, height, value

    @staticmethod
    def _validate_date(date: str) -> None:
        """Проверяет корректность даты.

        Args:
            date: Строка с датой

        Raises:
            ValueError: При некорректной дате
        """
        try:
            datetime.strptime(date, "%Y.%m.%d")
        except ValueError:
            raise ValueError("Некорректная дата")

    @staticmethod
    def _validate_measurement_values(height: float, value: int) -> None:
        """Проверяет корректность значений измерения.

        Args:
            height: Высота
            value: Значение давления

        Raises:
            ValueError: При отрицательной высоте или неположительном давлении
        """
        if height < 0:
            raise ValueError("Высота не может быть отрицательной")
        if value <= 0:
            raise ValueError("Давление должно быть положительным")


class MenuItem:
    """Класс для представления пункта меню."""

    def __init__(self, key: str, description: str, handler: Callable):
        """Инициализирует пункт меню.

        Args:
            key: Клавиша для выбора пункта
            description: Описание пункта меню
            handler: Функция-обработчик
        """
        self.key = key
        self.description = description
        self.handler = handler


class UserInterface:
    """Класс для работы с пользовательским интерфейсом."""

    @staticmethod
    def show_header() -> None:
        """Отображает заголовок программы."""
        print("\n=== БАЗА ИЗМЕРЕНИЙ ДАВЛЕНИЯ ===")

    @staticmethod
    def print_table(measurements: List[PressureMeasurement]) -> None:
        """Выводит таблицу с измерениями.

        Args:
            measurements: Список измерений
        """
        if not measurements:
            print("Нет данных.")
            return

        print("\nДата         | Высота   | Давление")
        print("-" * 36)
        for measurement in measurements:
            print(measurement)
        print("-" * 36)

    @staticmethod
    def get_user_input(prompt: str) -> str:
        """Получает ввод от пользователя.

        Args:
            prompt: Приглашение для ввода

        Returns:
            Введенная пользователем строка
        """
        return input(prompt).strip()

    @staticmethod
    def show_message(message: str) -> None:
        """Отображает сообщение пользователю.

        Args:
            message: Сообщение для отображения
        """
        print(message)

    @staticmethod
    def show_error(message: str) -> None:
        """Отображает сообщение об ошибке.

        Args:
            message: Сообщение об ошибке
        """
        print("Ошибка:", message)


class MeasurementManager:
    """Класс для управления коллекцией измерений."""

    def __init__(self):
        """Инициализирует менеджер измерений."""
        self.measurements: List[PressureMeasurement] = []

    def add_measurement(self, measurement: PressureMeasurement) -> None:
        """Добавляет измерение в коллекцию.

        Args:
            measurement: Объект измерения
        """
        self.measurements.append(measurement)

    def get_all(self) -> List[PressureMeasurement]:
        """Возвращает все измерения.

        Returns:
            Список всех измерений
        """
        return self.measurements.copy()

    def sort_by_date(self) -> None:
        """Сортирует измерения по дате."""
        self.measurements.sort(key=lambda x: x.date_as_datetime())

    def get_top_n(self, n: int) -> List[PressureMeasurement]:
        """Возвращает топ-N измерений по давлению.

        Args:
            n: Количество измерений

        Returns:
            Список топ-N измерений
        """
        return sorted(self.measurements, key=lambda x: x.value, reverse=True)[:n]

    def is_empty(self) -> bool:
        """Проверяет, пуста ли коллекция.

        Returns:
            True если коллекция пуста, иначе False
        """
        return len(self.measurements) == 0

    def save_to_file(self, filename: str) -> bool:
        """Сохраняет все измерения в текстовый файл.

        Args:
            filename: Имя файла для сохранения

        Returns:
            True если сохранение успешно, иначе False
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("Дата         | Высота   | Давление\n")
                file.write("-" * 36 + "\n")
                for measurement in self.measurements:
                    file.write(str(measurement) + "\n")
                file.write("-" * 36)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False


def handle_add_measurement(manager: MeasurementManager, ui: UserInterface) -> None:
    """Обрабатывает добавление нового измерения.

    Args:
        manager: Менеджер измерений
        ui: Пользовательский интерфейс
    """
    try:
        input_str = ui.get_user_input("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ: ")
        measurement = PressureParser.parse(input_str)
        manager.add_measurement(measurement)
        ui.show_message("Добавлено!\n")
    except ValueError as e:
        ui.show_error(str(e))


def handle_show_all(manager: MeasurementManager, ui: UserInterface) -> None:
    """Обрабатывает показ всех измерений.

    Args:
        manager: Менеджер измерений
        ui: Пользовательский интерфейс
    """
    if manager.is_empty():
        ui.show_message("Нет данных для отображения.")
    else:
        ui.print_table(manager.get_all())


def handle_sort_by_date(manager: MeasurementManager, ui: UserInterface) -> None:
    """Обрабатывает сортировку по дате.

    Args:
        manager: Менеджер измерений
        ui: Пользовательский интерфейс
    """
    if manager.is_empty():
        ui.show_message("Нет данных для сортировки.")
    else:
        manager.sort_by_date()
        ui.show_message("Отсортировано по дате.")


def handle_show_top5(manager: MeasurementManager, ui: UserInterface) -> None:
    """Обрабатывает показ топ-5 измерений.

    Args:
        manager: Менеджер измерений
        ui: Пользовательский интерфейс
    """
    if manager.is_empty():
        ui.show_message("Нет данных для отображения топа.")
    else:
        top5 = manager.get_top_n(5)
        ui.show_message("\nТОП-5 максимальных давлений:")
        ui.print_table(top5)


def handle_save_to_file(manager: MeasurementManager, ui: UserInterface) -> None:
    """Обрабатывает сохранение данных в файл.

    Args:
        manager: Менеджер измерений
        ui: Пользовательский интерфейс
    """
    if manager.is_empty():
        ui.show_message("Нет данных для сохранения.")
        return

    filename = ui.get_user_input("Введите имя файла для сохранения: ")
    if manager.save_to_file(filename):
        ui.show_message(f"Данные успешно сохранены в файл '{filename}'")
    else:
        ui.show_error("Не удалось сохранить данные в файл.")


def handle_exit(manager: MeasurementManager, ui: UserInterface) -> bool:
    """Обрабатывает выход из программы.

    Args:
        manager: Менеджер измерений
        ui: Пользовательский интерфейс

    Returns:
        True для выхода из программы
    """
    ui.show_message("До свидания!")
    return True


def create_menu() -> Dict[str, MenuItem]:
    """Создает меню программы.

    Returns:
        Словарь с пунктами меню
    """
    menu_items = {
        "1": MenuItem("1", "Добавить измерение", handle_add_measurement),
        "2": MenuItem("2", "Показать все измерения", handle_show_all),
        "3": MenuItem("3", "Отсортировать по дате", handle_sort_by_date),
        "4": MenuItem("4", "ТОП-5 максимальных давлений", handle_show_top5),
        "5": MenuItem("5", "Сохранить данные в файл", handle_save_to_file),
        "0": MenuItem("0", "Выход", handle_exit)
    }
    return menu_items


def display_menu(menu_items: Dict[str, MenuItem], ui: UserInterface) -> None:
    """Отображает меню пользователю.

    Args:
        menu_items: Словарь с пунктами меню
        ui: Пользовательский интерфейс
    """
    ui.show_message("\nМеню:")
    for item in menu_items.values():
        ui.show_message(f"{item.key} — {item.description}")


def process_user_choice(choice: str,
                        menu_items: Dict[str, MenuItem],
                        manager: MeasurementManager,
                        ui: UserInterface) -> bool:
    """Обрабатывает выбор пользователя.

    Args:
        choice: Выбор пользователя
        menu_items: Словарь с пунктами меню
        manager: Менеджер измерений
        ui: Пользовательский интерфейс

    Returns:
        True если программа должна завершиться, иначе False
    """
    if choice not in menu_items:
        ui.show_message("Неверный пункт меню.")
        return False

    menu_item = menu_items[choice]

    # Специальная обработка для выхода
    if choice == "0":
        return menu_item.handler(manager, ui)

    menu_item.handler(manager, ui)
    return False


def main() -> None:
    """Главная функция программы."""
    manager = MeasurementManager()
    ui = UserInterface()
    menu_items = create_menu()

    ui.show_header()

    should_exit = False
    while not should_exit:
        display_menu(menu_items, ui)
        choice = ui.get_user_input("\nВыбор: ")
        should_exit = process_user_choice(choice, menu_items, manager, ui)


if __name__ == "__main__":
    main()