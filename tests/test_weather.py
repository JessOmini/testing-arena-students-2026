"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""
import pytest

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)


def test_parse_time_regular_time():
    assert parse_time("14:21") == 861


def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)


def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]


def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)



# Tests for parse_time()

def test_parse_time_regular_time():
    assert parse_time("14:21") == 861


def test_parse_time_midnight():
    assert parse_time("00:00") == 0


def test_parse_time_last_minute():
    assert parse_time("23:59") == 1439


def test_parse_time_single_digit_hour():
    assert parse_time("9:05") == 545


def test_parse_time_single_digit_minute():
    assert parse_time("9:5") == 545


def test_parse_time_invalid_hour():
    with pytest.raises(ValueError):
        parse_time("24:00")


def test_parse_time_invalid_minute():
    with pytest.raises(ValueError):
        parse_time("12:60")


def test_parse_time_invalid_format():
    with pytest.raises(ValueError):
        parse_time("12:30:40")


def test_parse_time_non_numeric():
    with pytest.raises(ValueError):
        parse_time("ab:12")

def test_parse_time_empty_string():
    with pytest.raises(ValueError):
        parse_time("")


def test_parse_time_missing_hour():
    with pytest.raises(ValueError):
        parse_time(":30")


def test_parse_time_missing_minute():
    with pytest.raises(ValueError):
        parse_time("12:")


def test_parse_time_negative_hour():
    with pytest.raises(ValueError):
        parse_time("-1:30")

# Tests for parse_measurement()

def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == (
        "Köln", 861, 21.7
    )


def test_parse_measurement_whitespace():
    assert parse_measurement(" Köln ; 14:21 ; 21.7 ") == (
        "Köln", 861, 21.7
    )


def test_parse_measurement_negative_temperature():
    assert parse_measurement("Berlin;10:30;-5.5") == (
        "Berlin", 630, -5.5
    )


def test_parse_measurement_invalid_type():
    with pytest.raises(ValueError):
        parse_measurement(123)


def test_parse_measurement_empty_city():
    with pytest.raises(ValueError):
        parse_measurement(";14:21;21.7")


def test_parse_measurement_missing_field():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21")


def test_parse_measurement_extra_field():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;21.7;extra")


def test_parse_measurement_invalid_temperature():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;abc")

def test_parse_measurement_invalid_time():
    with pytest.raises(ValueError):
        parse_measurement("Köln;25:00;21.7")


def test_parse_measurement_city_only_whitespace():
    with pytest.raises(ValueError):
        parse_measurement("   ;14:21;21.7")

# Tests for filter_by_temperature()

def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]


def test_filter_by_temperature_lower_boundary():
    measurements = [
        ("Köln", 600, 10.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 20.0) == measurements


def test_filter_by_temperature_upper_boundary():
    measurements = [
        ("Köln", 600, 20.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 20.0) == measurements


def test_filter_by_temperature_equal_boundaries():
    measurements = [
        ("Köln", 600, 15.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 15.0) == measurements


def test_filter_by_temperature_empty_list():
    assert filter_by_temperature([], 10.0, 20.0) == []


def test_filter_by_temperature_invalid_range():
    with pytest.raises(ValueError):
        filter_by_temperature([], 20.0, 10.0)


def test_filter_by_temperature_duplicates():
    measurements = [
        ("Köln", 600, 15.0),
        ("Köln", 600, 15.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 20.0) == measurements


def test_filter_by_temperature_order():
    measurements = [
        ("Bonn", 900, 18.0),
        ("Köln", 600, 15.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 20.0) == measurements


def test_filter_by_temperature_does_not_modify_input():
    measurements = [
        ("Köln", 600, 10.0),
        ("Bonn", 900, 20.0),
    ]

    original = measurements.copy()

    result = filter_by_temperature(measurements, 10.0, 20.0)

    assert measurements == original
    assert result is not measurements

def test_filter_by_temperature_excludes_values_outside_range():
    measurements = [
        ("Köln", 600, 9.9),
        ("Bonn", 700, 15.0),
        ("Berlin", 800, 20.1),
    ]

    assert filter_by_temperature(measurements, 10.0, 20.0) == [
        ("Bonn", 700, 15.0)
    ]

# Tests for average_temperature()

def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_average_temperature_only_selected_city():
    measurements = [
        ("Köln", 600, 10.0),
        ("Bonn", 720, 100.0),
        ("Köln", 900, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_average_temperature_case_sensitive():
    measurements = [
        ("Köln", 600, 10.0),
        ("köln", 720, 30.0),
    ]

    assert average_temperature(measurements, "Köln") == 10.0


def test_average_temperature_city_not_found():
    measurements = [
        ("Köln", 600, 10.0),
    ]

    with pytest.raises(ValueError):
        average_temperature(measurements, "Berlin")


def test_average_temperature_empty_list():
    with pytest.raises(ValueError):
        average_temperature([], "Köln")


def test_average_temperature_does_not_modify_input():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    original = measurements.copy()

    average_temperature(measurements, "Köln")

    assert measurements == original

def test_average_temperature_single_measurement():
    measurements = [
        ("Köln", 600, 18.5),
    ]

    assert average_temperature(measurements, "Köln") == 18.5

# Tests for hottest_measurement()

def test_hottest_measurement_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == (
        "Düsseldorf", 720, 25.0
    )


def test_hottest_measurement_earliest_time_wins():
    measurements = [
        ("A", 900, 30.0),
        ("B", 600, 30.0),
        ("C", 700, 30.0),
    ]

    assert hottest_measurement(measurements) == (
        "B", 600, 30.0
    )


def test_hottest_measurement_first_entry_wins():
    measurements = [
        ("A", 600, 30.0),
        ("B", 600, 30.0),
    ]

    assert hottest_measurement(measurements) == (
        "A", 600, 30.0
    )


def test_hottest_measurement_single_item():
    measurement = ("Köln", 600, 20.0)

    assert hottest_measurement([measurement]) == measurement


def test_hottest_measurement_empty_list():
    with pytest.raises(ValueError):
        hottest_measurement([])


def test_hottest_measurement_does_not_modify_input():
    measurements = [
        ("A", 900, 20.0),
        ("B", 600, 30.0),
    ]

    original = measurements.copy()

    hottest_measurement(measurements)

    assert measurements == original

def test_hottest_measurement_negative_temperatures():
    measurements = [
        ("Köln", 600, -5.0),
        ("Berlin", 700, -2.0),
        ("Bonn", 800, -8.0),
    ]

    assert hottest_measurement(measurements) == (
        "Berlin", 700, -2.0
    )