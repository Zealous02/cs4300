"""Task 6: File Handling

Parametrized pytest tests that verify the word count for each text file.
"""
import pytest

import task6


@pytest.mark.parametrize(
    "content, expected",
    [
        ("hello world", 2),
        ("one", 1),
        ("", 0),
        ("   \n\t  ", 0),
        ("  spaced   out \n words\there  ", 4),
        ("line one\nline two\nline three", 6),
        ("Hello, world. Punctuation, stays attached!", 5),
        ("unicode café naïve 日本語", 4),
    ],
)
def test_count_words_in_temp_files(tmp_path, content, expected):
    """Each parametrized case is written to its own temporary text file."""
    file = tmp_path / "sample.txt"
    file.write_text(content, encoding="utf-8")
    assert task6.count_words(file) == expected


def test_count_words_in_assignment_file():
    """The real task6_read_me.txt contains 104 words."""
    assert task6.count_words(task6.DEFAULT_FILE) == 104


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        task6.count_words(tmp_path / "does_not_exist.txt")


def test_directory_raises(tmp_path):
    with pytest.raises(IsADirectoryError):
        task6.count_words(tmp_path)


def test_main_output(capsys):
    task6.main()
    assert capsys.readouterr().out.strip() == "Word count: 104"
