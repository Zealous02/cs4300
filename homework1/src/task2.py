"""Task 2: Variables and Data Types

Demonstrates integers, floating-point numbers, strings, and booleans.
"""

integer_value = 42
float_value = 3.14
string_value = "Hello, Python"
boolean_value = True


def integer_operations(a, b):
    """Return the sum, floor division, and remainder of two integers."""
    return a + b, a // b, a % b


def float_operations(a, b):
    """Return the product and the true division of two floats."""
    return a * b, a / b


def string_operations(text):
    """Return the uppercase version, length, and reversed version of a string."""
    return text.upper(), len(text), text[::-1]


def boolean_operations(a, b):
    """Return (a and b, a or b, not a) for two booleans."""
    return a and b, a or b, not a


def main():
    """Print each variable along with its data type."""
    for name, value in [
        ("integer_value", integer_value),
        ("float_value", float_value),
        ("string_value", string_value),
        ("boolean_value", boolean_value),
    ]:
        print(f"{name} = {value!r} ({type(value).__name__})")


if __name__ == "__main__":
    main()
