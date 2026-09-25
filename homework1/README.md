# CS 4300 - Homework 1

Python fundamentals with pytest: one script and one test file per task.

## Setup

```bash
cd /coursework
python3 -m venv hw1_env --system-site-packages
source hw1_env/bin/activate
cd cs4300/homework1
python3 -m pip install -r requirements.txt
```

## Run the tests

From the `homework1` folder:

```bash
pytest
```

All 115 tests should pass. The pytest settings live in `pyproject.toml`, which puts `src/` on the import path.

## Run a task

```bash
python3 src/task1.py    # replace 1 with 1-7
```

Task 7 makes a live call to the GitHub API. Its tests mock the network, so they run offline.

## Layout

| Path | Contents |
|------|----------|
| `src/task1.py` - `src/task7.py` | The seven task scripts |
| `tests/test_task1.py` - `tests/test_task7.py` | Pytest tests for each task |
| `task6_read_me.txt` | Text file read by Task 6 |
| `requirements.txt` | Recorded dependencies (pytest, requests) |
| `pyproject.toml` | Pytest configuration |

## Tasks

1. Introduction to Python and Testing
2. Variables and Data Types
3. Control Structures
4. Functions and Duck Typing
5. Lists and Dictionaries
6. File Handling
7. Package Management (`requests`)
