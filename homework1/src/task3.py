"""Task 3: Control Structures

Demonstrates an if statement (positive/negative/zero), a for loop
(first 10 prime numbers), and a while loop (sum of 1 to 100).
"""
import itertools
import math


def classify_number(n):
    """Return 'positive', 'negative', or 'zero' for a given number."""
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


def is_prime(n):
    """Return True if n is a prime number, otherwise False."""
    if n < 2:
        return False
    for divisor in range(2, math.isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


def first_primes(count=10):
    """Return a list of the first `count` prime numbers using a for loop."""
    if count <= 0:
        return []
    primes = []
    for candidate in itertools.count(2):
        if is_prime(candidate):
            primes.append(candidate)
            if len(primes) == count:
                break
    return primes


def print_first_primes(count=10):
    """Print the first `count` prime numbers, one per line."""
    for prime in first_primes(count):
        print(prime)


def sum_to_n(n=100):
    """Return the sum of all whole numbers from 1 to n using a while loop."""
    total = 0
    i = 1
    while i <= n:
        total += i
        i += 1
    return total


def main():
    """Demonstrate each control structure."""
    for number in (7, -3, 0):
        print(f"{number} is {classify_number(number)}")
    print("First 10 primes:")
    print_first_primes(10)
    print(f"Sum of 1 to 100: {sum_to_n(100)}")


if __name__ == "__main__":
    main()
