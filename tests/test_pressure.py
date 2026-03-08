import pytest
from datetime import datetime
from oppo2_improved import PressureParser, PressureMeasurement, MeasurementManager

# --- Тесты для PressureParser ---

def test_parse_valid_input():
    """Тест успешного парсинга корректной строки."""
    input_str = "2023.10.26 150.5 101325"
    measurement = PressureParser.parse(input_str)
    assert isinstance(measurement, PressureMeasurement)
    assert measurement.date == "2023.10.26"
    assert measurement.height == 150.5
    assert measurement.value == 101325
    assert measurement.date_as_datetime() == datetime(2023, 10, 26)

def test_parse_invalid_format():
    """Тест на выброс исключения при неверном формате."""
    with pytest.raises(ValueError, match="Неверный формат"):
        PressureParser.parse("2023.10.26 150.5")

    with pytest.raises(ValueError, match="Неверный формат"):
        PressureParser.parse("26.10.2023 150.5 101325") # Неправильный формат даты

    with pytest.raises(ValueError, match="Неверный формат"):
        PressureParser.parse("2023.10.26 abc 101325")

def test_parse_invalid_date():
    """Тест на выброс исключения при некорректной дате."""
    with pytest.raises(ValueError, match="Некорректная дата"):
        PressureParser.parse("2023.13.26 150.5 101325") # Несуществующий месяц

    with pytest.raises(ValueError, match="Некорректная дата"):
        PressureParser.parse("2023.10.32 150.5 101325") # Несуществующий день

def test_parse_invalid_height():
    """Тест на выброс исключения при отрицательной высоте."""
    with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
        PressureParser.parse("2023.10.26 -10.0 101325")

def test_parse_invalid_value():
    """Тест на выброс исключения при неположительном давлении."""
    with pytest.raises(ValueError, match="Давление должно быть положительным"):
        PressureParser.parse("2023.10.26 150.5 0")

    with pytest.raises(ValueError, match="Давление должно быть положительным"):
        PressureParser.parse("2023.10.26 150.5 -100")

# --- Тесты для MeasurementManager ---

def test_manager_sort_by_date():
    """Тест сортировки измерений по дате."""
    manager = MeasurementManager()
    m1 = PressureParser.parse("2024.01.15 100 1000")
    m2 = PressureParser.parse("2023.12.31 200 2000")
    m3 = PressureParser.parse("2024.06.01 150 1500")

    manager.add_measurement(m1)
    manager.add_measurement(m2)
    manager.add_measurement(m3)

    manager.sort_by_date()
    sorted_list = manager.get_all()

    assert sorted_list[0].date == "2023.12.31"
    assert sorted_list[1].date == "2024.01.15"
    assert sorted_list[2].date == "2024.06.01"

def test_manager_get_top_n():
    """Тест получения топ-N измерений по давлению."""
    manager = MeasurementManager()
    manager.add_measurement(PressureParser.parse("2024.01.01 100 500"))
    manager.add_measurement(PressureParser.parse("2024.01.02 100 1000"))
    manager.add_measurement(PressureParser.parse("2024.01.03 100 700"))
    manager.add_measurement(PressureParser.parse("2024.01.04 100 900"))

    top2 = manager.get_top_n(2)
    assert len(top2) == 2
    assert top2[0].value == 1000
    assert top2[1].value == 900

    top5 = manager.get_top_n(5) # Запрашиваем больше, чем есть
    assert len(top5) == 4 # Должен вернуть все 4

def test_manager_is_empty():
    """Тест проверки на пустоту."""
    manager = MeasurementManager()
    assert manager.is_empty() is True
    manager.add_measurement(PressureParser.parse("2024.01.01 100 500"))
    assert manager.is_empty() is False