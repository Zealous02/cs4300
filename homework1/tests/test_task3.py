"""Task 3: Control Structures

Pytest tests for the if statement, for loop, and while loop.
"""
import pytest

import task3


@pytest.mark.parametrize(
    "number, expected",
    [
        (5, "positive"),
        (-5, "negative"),
        (0, "zero"),
        (0.0, "zero"),
        (-0.0, "zero"),
        (0.001, "positive"),
        (-0.001, "negative"),
        (10**12, "positive"),
        (-(10**12), "negative"),
    ],
)
def test_classify_number(number, expected):
    assert task3.classify_number(number) == expected


@pytest.mark.parametrize(
    "number, expected",
    [
        (-7, False),
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (9, False),
        (25, False),
        (97, True),
        (100, False),
    ],
)
def test_is_prime(number, expected):
    assert task3.is_prime(number) == expected


def test_first_ten_primes():
    assert task3.first_primes() == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


@pytest.mark.parametrize(
    "count, expected",
    [
        (1, [2]),
        (3, [2, 3, 5]),
        (0, []),
        (-4, []),
    ],
)
def test_first_primes_other_counts(count, expected):
    assert task3.first_primes(count) == expected


def test_print_first_primes(capsys):
    """The for loop should print exactly ten primes, one per line."""
    task3.print_first_primes()
    lines = capsys.readouterr().out.split()
    assert lines == ["2", "3", "5", "7", "11", "13", "17", "19", "23", "29"]


@pytest.mark.parametrize(
    "n, expected",
    [
        (100, 5050),
        (10, 55),
        (1, 1),
        (0, 0),
        (-5, 0),
    ],
)
def test_sum_to_n(n, expected):
    assert task3.sum_to_n(n) == expected


def test_main_output(capsys):
    task3.main()
    out = capsys.readouterr().out
    assert "7 is positive" in out
    assert "-3 is negative" in out
    assert "0 is zero" in out
    assert "5050" in out
