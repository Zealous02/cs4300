"""Task 4: Functions and Duck Typing

Pytest tests for calculate_discount with various numeric types and
invalid inputs.
"""
from decimal import Decimal
from fractions import Fraction

import pytest

import task4
from task4 import calculate_discount


@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (100, 20, 80),            # int, int
        (200, 50, 100),           # int, int
        (100.0, 20.0, 80.0),      # float, float
        (59.99, 15.5, 50.69155),  # float with a fractional percent
        (50, 10.0, 45.0),         # mixed int and float
        (19.99, 0, 19.99),        # no discount
        (100, 100, 0),            # full discount
        (0, 25, 0),               # free item stays free
    ],
)
def test_numeric_types(price, discount, expected):
    assert calculate_discount(price, discount) == pytest.approx(expected)


def test_decimal_duck_typing():
    """Decimal isn't int or float, but it quacks like a number."""
    result = calculate_discount(Decimal("100"), Decimal("25"))
    assert isinstance(result, Decimal)
    assert result == Decimal("75")


def test_fraction_duck_typing():
    result = calculate_discount(Fraction(200), Fraction(50))
    assert isinstance(result, Fraction)
    assert result == Fraction(100)


@pytest.mark.parametrize(
    "price, discount",
    [
        ("100", 20),
        (100, "20"),
        (None, 20),
        (100, None),
        ([100], 20),
        (True, 20),      # bool is technically an int, but not a sensible price
        (100, False),
        (1 + 2j, 20),    # complex numbers can't be compared
    ],
)
def test_invalid_types_raise_type_error(price, discount):
    with pytest.raises(TypeError):
        calculate_discount(price, discount)


@pytest.mark.parametrize(
    "price, discount",
    [
        (-1, 20),
        (-0.01, 10),
        (100, -1),
        (100, 100.01),
        (100, 101),
    ],
)
def test_invalid_values_raise_value_error(price, discount):
    with pytest.raises(ValueError):
        calculate_discount(price, discount)


def test_main_output(capsys):
    task4.main()
    out = capsys.readouterr().out.split()
    assert out[0] == "80.0"
    assert out[2] == "75"
    assert out[3] == "100"
