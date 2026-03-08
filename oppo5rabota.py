from datetime import datetime
import re
from typing import List, Tuple, Dict, Optional
import heapq  # Для оптимизации top_n


class PressureMeasurement:
    """Класс для хранения данных измерения давления."""
    def __init__(self, date: str, height: float, value: int):
        self.date = date
        self.height = height
        self.value = value

    def date_as_datetime(self) -> datetime:
        return datetime.strptime(self.date, "%Y.%m.%d")

    def __str__(self) -> str:
        return f"{self.date:12} | {self.height:8.1f} м | {self.value:6} Па"


class PressureParser:
    """Парсер для строк с данными измерения давления."""
    _PATTERN = r'^(\d{4}\.\d{2}\.\d{2})\s+(\d+(?:\.\d+)?)\s+(\d+)$'

    @classmethod
    def parse(cls, input_str: str) -> PressureMeasurement:
        cls._validate_format(input_str)
        date, height, value = cls._extract_values(input_str)
        cls._validate_date(date)
        cls._validate_measurement_values(height, value)
        return PressureMeasurement(date, height, value)

    @classmethod
    def _validate_format(cls, input_str: str) -> None:
        if not re.match(cls._PATTERN, input_str.strip()):
            raise ValueError("Неверный формат. Используйте: ГГГГ.ММ.ДД ВЫСОТА ЗНАЧЕНИЕ")

    @classmethod
    def _extract_values(cls, input_str: str) -> Tuple[str, float, int]:
        match = re.match(cls._PATTERN, input_str.strip())
        date = match.group(1)
        height = float(match.group(2))
        value = int(match.group(3))
        return date, height, value

    @staticmethod
    def _validate_date(date: str) -> None:
        try:
            datetime.strptime(date, "%Y.%m.%d")
        except ValueError:
            raise ValueError("Некорректная дата")

    @staticmethod
    def _validate_measurement_values(height: float, value: int) -> None:
        if height < 0:
            raise ValueError("Высота не может быть отрицательной")
        if value <= 0:
            raise ValueError("Давление должно быть положительным")


class UserInterface:
    """Класс для работы с пользовательским интерфейсом."""
    @staticmethod
    def show_header() -> None:
        print("\n=== БАЗА ИЗМЕРЕНИЙ ДАВЛЕНИЯ ===")

    @staticmethod
    def print_table(measurements: List[PressureMeasurement]) -> None:
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
        return input(prompt).strip()

    @staticmethod
    def show_message(message: str) -> None:
        print(message)

    @staticmethod
    def show_error(message: str) -> None:
        print("Ошибка:", message)


class MeasurementManager:
    """Класс для управления коллекцией измерений."""

    def __init__(self):
        """Инициализирует менеджер измерений."""
        self.measurements: List[PressureMeasurement] = []

    def add_measurement(self, measurement: PressureMeasurement) -> None:
        """Добавляет измерение в коллекцию."""
        self.measurements.append(measurement)

    def get_all(self) -> List[PressureMeasurement]:
        """Возвращает все измерения."""
        return self.measurements.copy()

    def sort_by_date(self) -> None:
        """Сортирует измерения по дате."""
        self.measurements.sort(key=lambda x: x.date_as_datetime())

    def get_top_n(self, n: int) -> List[PressureMeasurement]:
        """Возвращает топ-N измерений по давлению (оптимизированная версия)."""
        return heapq.nlargest(n, self.measurements, key=lambda x: x.value)

    # Метод is_empty() удален как избыточный.

    def save_to_file(self, filename: str) -> bool:
        """Сохраняет все измерения в текстовый файл."""
        if not self.measurements:  # Прямая проверка
            print("Нет данных для сохранения.")
            return False

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("Дата         | Высота   | Давление\n")
                file.write("-" * 36 + "\n")
                for measurement in self.measurements:
                    file.write(str(measurement) + "\n")
                file.write("-" * 36)
            return True
        except IOError as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False


class Application:
    """Главный класс приложения, объединяющий все компоненты."""

    TOP_N_COUNT = 5  # Константа для устранения магического числа

    def __init__(self):
        """Инициализирует приложение."""
        self.manager = MeasurementManager()
        self.ui = UserInterface()
        self.menu_items = self._create_menu()
        self.running = False

    def _create_menu(self) -> Dict[str, Dict[str, any]]:
        """Создает меню программы."""
        return {
            "1": {"desc": "Добавить измерение", "handler": self._handle_add_measurement},
            "2": {"desc": "Показать все измерения", "handler": self._handle_show_all},
            "3": {"desc": "Отсортировать по дате", "handler": self._handle_sort_by_date},
            "4": {"desc": f"ТОП-{self.TOP_N_COUNT} максимальных давлений", "handler": self._handle_show_top},
            "5": {"desc": "Сохранить данные в файл", "handler": self._handle_save_to_file},
            "0": {"desc": "Выход", "handler": self._handle_exit}
        }

    def _display_menu(self) -> None:
        """Отображает меню пользователю."""
        self.ui.show_message("\nМеню:")
        for key, item in self.menu_items.items():
            self.ui.show_message(f"{key} — {item['desc']}")

    def _handle_add_measurement(self) -> None:
        """Обрабатывает добавление нового измерения."""
        try:
            input_str = self.ui.get_user_input("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ: ")
            measurement = PressureParser.parse(input_str)
            self.manager.add_measurement(measurement)
            self.ui.show_message("Добавлено!\n")
        except ValueError as e:
            self.ui.show_error(str(e))

    def _handle_show_all(self) -> None:
        """Обрабатывает показ всех измерений."""
        if not self.manager.measurements:  # Прямая проверка вместо is_empty()
            self.ui.show_message("Нет данных для отображения.")
        else:
            self.ui.print_table(self.manager.get_all())

    def _handle_sort_by_date(self) -> None:
        """Обрабатывает сортировку по дате."""
        if not self.manager.measurements:
            self.ui.show_message("Нет данных для сортировки.")
        else:
            self.manager.sort_by_date()
            self.ui.show_message("Отсортировано по дате.")

    def _handle_show_top(self) -> None:
        """Обрабатывает показ топ-N измерений."""
        if not self.manager.measurements:
            self.ui.show_message("Нет данных для отображения топа.")
        else:
            top = self.manager.get_top_n(self.TOP_N_COUNT)
            self.ui.show_message(f"\nТОП-{self.TOP_N_COUNT} максимальных давлений:")
            self.ui.print_table(top)

    def _handle_save_to_file(self) -> None:
        """Обрабатывает сохранение данных в файл."""
        filename = self.ui.get_user_input("Введите имя файла для сохранения: ")
        if self.manager.save_to_file(filename):
            self.ui.show_message(f"Данные успешно сохранены в файл '{filename}'")
        # Сообщение об ошибке выводится внутри save_to_file, но можно и здесь добавить.
        # else:
        #     self.ui.show_error("Не удалось сохранить данные в файл.")

    def _handle_exit(self) -> None:
        """Обрабатывает выход из программы."""
        self.ui.show_message("До свидания!")
        self.running = False

    def _process_user_choice(self, choice: str) -> None:
        """Обрабатывает выбор пользователя."""
        if choice not in self.menu_items:
            self.ui.show_message("Неверный пункт меню.")
            return
        self.menu_items[choice]["handler"]()

    def run(self) -> None:
        """Запускает главный цикл программы."""
        self.ui.show_header()
        self.running = True
        while self.running:
            self._display_menu()
            choice = self.ui.get_user_input("\nВыбор: ")
            self._process_user_choice(choice)


def main() -> None:
    """Точка входа в программу."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()