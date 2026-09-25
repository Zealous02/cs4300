"""Task 6: File Handling

Reads task6_read_me.txt and counts the number of words in it.
"""
from pathlib import Path

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "task6_read_me.txt"


def count_words(path=DEFAULT_FILE):
    """Return the number of whitespace-separated words in a text file.

    Raises:
        FileNotFoundError: if the file does not exist.
        IsADirectoryError: if the path is a directory.
    """
    with open(path, "r", encoding="utf-8") as f:
        return len(f.read().split())


def main():
    """Print the word count of task6_read_me.txt."""
    print(f"Word count: {count_words()}")


if __name__ == "__main__":
    main()
