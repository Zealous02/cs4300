"""Task 2: Variables and Data Types

Parameterized pytest tests for each data type.
"""
import pytest

import task2


@pytest.mark.parametrize(
    "value, expected_type",
    [
        (task2.integer_value, int),
        (task2.float_value, float),
        (task2.string_value, str),
        (task2.boolean_value, bool),
    ],
)
def test_variable_types(value, expected_type):
    """Each variable should have exactly the expected type."""
    assert type(value) is expected_type


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (7, 2, (9, 3, 1)),
        (10, 5, (15, 2, 0)),
        (-7, 2, (-5, -4, 1)),
        (0, 5, (5, 0, 0)),
    ],
)
def test_integer_operations(a, b, expected):
    assert task2.integer_operations(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2.5, 2.0, (5.0, 1.25)),
        (1.5, 0.5, (0.75, 3.0)),
        (0.1, 0.2, (0.02, 0.5)),
    ],
)
def test_float_operations(a, b, expected):
    """Floats are compared with approx to avoid rounding errors."""
    assert task2.float_operations(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Python", ("PYTHON", 6, "nohtyP")),
        ("abc", ("ABC", 3, "cba")),
        ("", ("", 0, "")),
    ],
)
def test_string_operations(text, expected):
    assert task2.string_operations(text) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (True, True, (True, True, False)),
        (True, False, (False, True, False)),
        (False, True, (False, True, True)),
        (False, False, (False, False, True)),
    ],
)
def test_boolean_operations(a, b, expected):
    assert task2.boolean_operations(a, b) == expected


def test_main_prints_each_type(capsys):
    """main() should print every variable with its type name."""
    task2.main()
    out = capsys.readouterr().out
    assert "integer_value = 42 (int)" in out
    assert "float_value = 3.14 (float)" in out
    assert "string_value = 'Hello, Python' (str)" in out
    assert "boolean_value = True (bool)" in out
