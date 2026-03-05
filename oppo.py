from datetime import datetime
import re


class PressureMeasurement:
    def __init__(self, date: str, height: float, value: int):
        self.date = date
        self.height = height
        self.value = value

    def date_as_datetime(self):
        return datetime.strptime(self.date, "%Y.%m.%d")

    def __str__(self) -> str:
        return f"{self.date:12} | {self.height:8.1f} м | {self.value:6} Па"


class PressureParser:
    @staticmethod
    def parse(input_str: str) -> PressureMeasurement:
        # Регулярное выражение для парсинга: ГГГГ.ММ.ДД число число
        pattern = r'^(\d{4}\.\d{2}\.\d{2})\s+(\d+(?:\.\d+)?)\s+(\d+)$'
        match = re.match(pattern, input_str.strip())

        if not match:
            raise ValueError("Неверный формат. Используйте: ГГГГ.ММ.ДД ВЫСОТА ЗНАЧЕНИЕ")

        date = match.group(1)
        height = float(match.group(2))
        value = int(match.group(3))

        # Дополнительная валидация даты
        try:
            datetime.strptime(date, "%Y.%m.%d")
        except ValueError:
            raise ValueError("Некорректная дата")

        if height < 0:
            raise ValueError("Высота не может быть отрицательной")
        if value <= 0:
            raise ValueError("Давление должно быть положительным")

        return PressureMeasurement(date, height, value)


def show_header():
    print("\n=== БАЗА ИЗМЕРЕНИЙ ДАВЛЕНИЯ ===")


def print_table(data):
    if not data:
        print("Нет данных.")
        return
    print("\nДата         | Высота   | Давление")
    print("-" * 36)
    for m in data:
        print(m)
    print("-" * 36)


def add_measurement(measurements):
    """Добавление нового измерения"""
    try:
        inp = input("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ: ")
        m = PressureParser.parse(inp)
        measurements.append(m)
        print("Добавлено!\n")
    except ValueError as e:
        print("Ошибка:", e)


def show_all(measurements):
    """Показать все измерения"""
    print_table(measurements)


def sort_by_date(measurements):
    """Сортировка по дате"""
    measurements.sort(key=lambda x: x.date_as_datetime())
    print("Отсортировано по дате.")


def show_top5(measurements):
    """Показать ТОП-5 максимальных давлений"""
    top5 = sorted(measurements, key=lambda x: x.value, reverse=True)[:5]
    print("\nТОП-5 максимальных давлений:")
    print_table(top5)


def exit_program(measurements):
    """Выход из программы"""
    print("До свидания!")
    return True  # Сигнал для выхода


def main():
    measurements = []

    # Словарь для меню: ключ -> (функция, описание)
    menu_items = {
        "1": (add_measurement, "Добавить измерение"),
        "2": (show_all, "Показать все измерения"),
        "3": (sort_by_date, "Отсортировать по дате"),
        "4": (show_top5, "ТОП-5 максимальных давлений"),
        "0": (exit_program, "Выход")
    }

    show_header()

    while True:
        print("\nМеню:")
        for key, (_, description) in menu_items.items():
            print(f"{key} — {description}")

        choice = input("\nВыбор: ")

        if choice in menu_items:
            func = menu_items[choice][0]
            # Специальная обработка для выхода
            if choice == "0":
                if func(measurements):
                    break
            else:
                func(measurements)
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()