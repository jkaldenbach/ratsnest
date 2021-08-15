import os
from pathlib import Path

from ratsnest.config import Config
from ratsnest.main import startup

CURRENT_DIR = Path(os.path.dirname(__file__))
NOTES_DIR = CURRENT_DIR / 'files'
EXPECTED_TODOS = CURRENT_DIR / 'expected_todos.md'


def test_startup():
    """Should create a todo file."""
    config = Config(NOTES_DIR)
    startup(config)
    with open(EXPECTED_TODOS) as expected_file:
        with open(config.todo_file) as file:
            assert expected_file.read() == file.read()
