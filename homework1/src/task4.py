"""Task 4: Functions and Duck Typing

calculate_discount works with any numeric type (int, float, Decimal,
Fraction, ...) because it only relies on arithmetic operators, not on a
specific class. Inputs are validated before any math is done.
"""
from numbers import Number


def _check_number(value, name):
    """Raise TypeError unless value is a real numeric type (bools are rejected)."""
    if isinstance(value, bool) or not isinstance(value, Number):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")


def calculate_discount(price, discount):
    """Return the final price after applying a percentage discount.

    Args:
        price: original price, any numeric type, must be >= 0.
        discount: discount percentage, any numeric type, from 0 to 100.

    Returns:
        price * (100 - discount) / 100, in the same numeric family as the inputs.

    Raises:
        TypeError: if price or discount is not a number.
        ValueError: if price is negative or discount is outside 0-100.
    """
    _check_number(price, "price")
    _check_number(discount, "discount")
    if price < 0:
        raise ValueError("price must not be negative")
    if not 0 <= discount <= 100:
        raise ValueError("discount must be between 0 and 100")
    return price * (100 - discount) / 100


def main():
    """Demonstrate duck typing with several numeric types."""
    from decimal import Decimal
    from fractions import Fraction

    print(calculate_discount(100, 20))
    print(calculate_discount(59.99, 15.5))
    print(calculate_discount(Decimal("100"), Decimal("25")))
    print(calculate_discount(Fraction(200), Fraction(50)))


if __name__ == "__main__":
    main()
