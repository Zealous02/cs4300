"""Task 1: Introduction to Python and Testing

Pytest test that captures stdout and verifies the script's output.
"""
import task1


def test_hello_world_output(capsys):
    """main() should print exactly 'Hello, World!' followed by a newline."""
    task1.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"
