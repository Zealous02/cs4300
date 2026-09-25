"""Task 5: Lists and Dictionaries

Pytest tests for the book list (slicing) and the student dictionary.
"""
import pytest

import task5


@pytest.fixture
def database():
    """A fresh copy of the student database so tests never change the original."""
    return dict(task5.student_database)


# ---------- list of books ----------

def test_book_list_has_titles_and_authors():
    assert len(task5.favorite_books) >= 3
    for book in task5.favorite_books:
        assert isinstance(book["title"], str) and book["title"]
        assert isinstance(book["author"], str) and book["author"]


def test_first_three_books_slice():
    result = task5.first_three_books(task5.favorite_books)
    assert len(result) == 3
    assert result == task5.favorite_books[:3]


@pytest.mark.parametrize(
    "books, expected_count",
    [
        ([], 0),
        ([{"title": "A", "author": "X"}], 1),
        ([{"title": "A", "author": "X"}, {"title": "B", "author": "Y"}], 2),
        ([{"title": t, "author": "X"} for t in "ABCD"], 3),
    ],
)
def test_slice_handles_short_and_long_lists(books, expected_count):
    """Slicing never raises, even when the list has fewer than three items."""
    assert len(task5.first_three_books(books)) == expected_count


def test_slice_does_not_modify_original():
    before = list(task5.favorite_books)
    task5.first_three_books(task5.favorite_books)
    assert task5.favorite_books == before


def test_print_first_three(capsys):
    task5.print_first_three()
    lines = capsys.readouterr().out.splitlines()
    expected = [f"{b['title']} by {b['author']}" for b in task5.favorite_books[:3]]
    assert lines == expected


# ---------- student dictionary ----------

def test_database_maps_names_to_ids():
    assert isinstance(task5.student_database, dict)
    for name, student_id in task5.student_database.items():
        assert isinstance(name, str)
        assert isinstance(student_id, int)


def test_student_ids_are_unique():
    ids = list(task5.student_database.values())
    assert len(ids) == len(set(ids))


def test_lookup_existing_students(database):
    for name, student_id in task5.student_database.items():
        assert task5.get_student_id(database, name) == student_id


def test_lookup_missing_student_returns_none(database):
    assert task5.get_student_id(database, "Nobody Here") is None


def test_add_student(database):
    task5.add_student(database, "Dana Lee", 2001)
    assert database["Dana Lee"] == 2001
    assert len(database) == len(task5.student_database) + 1


def test_add_duplicate_student_raises(database):
    existing = next(iter(database))
    with pytest.raises(ValueError):
        task5.add_student(database, existing, 9999)


def test_remove_student(database):
    name = next(iter(database))
    expected_id = database[name]
    assert task5.remove_student(database, name) == expected_id
    assert name not in database


def test_remove_missing_student_raises(database):
    with pytest.raises(KeyError):
        task5.remove_student(database, "Nobody Here")


def test_main_output(capsys):
    task5.main()
    out = capsys.readouterr().out
    first = task5.favorite_books[0]
    assert f"{first['title']} by {first['author']}" in out
    assert "Alice Johnson: 1001" in out
