"""Task 5: Lists and Dictionaries

A list of favorite books (title and author), list slicing to get the first
three, and a dictionary acting as a basic student database.
"""

favorite_books = [
    {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"title": "Dune", "author": "Frank Herbert"},
    {"title": "1984", "author": "George Orwell"},
    {"title": "The Martian", "author": "Andy Weir"},
    {"title": "Project Hail Mary", "author": "Andy Weir"},
]

# Student name -> student ID
student_database = {
    "Alice Johnson": 1001,
    "Bob Smith": 1002,
    "Carla Gomez": 1003,
}


def first_three_books(books):
    """Return the first three books using list slicing."""
    return books[:3]


def print_first_three(books=None):
    """Print the first three books as 'Title by Author', one per line."""
    if books is None:
        books = favorite_books
    for book in first_three_books(books):
        print(f"{book['title']} by {book['author']}")


def add_student(database, name, student_id):
    """Add a student to the database. Raises ValueError if the name exists."""
    if name in database:
        raise ValueError(f"{name} is already in the database")
    database[name] = student_id


def get_student_id(database, name):
    """Return a student's ID, or None if the student isn't in the database."""
    return database.get(name)


def remove_student(database, name):
    """Remove a student and return their ID. Raises KeyError if missing."""
    return database.pop(name)


def main():
    """Print the first three books and the student database."""
    print_first_three()
    for name, student_id in student_database.items():
        print(f"{name}: {student_id}")


if __name__ == "__main__":
    main()
