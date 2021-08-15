import os
from pathlib import Path

from ratsnest.config import Config
from ratsnest.parser import parse_file, Todo

NOTES_DIR = Path(os.path.dirname(__file__)) / 'files'


class TestParser:
    config = Config(NOTES_DIR)
    file_path = NOTES_DIR / 'note_with_todos.md'

    def test_parse_file(self):
        result = parse_file(self.file_path, self.config)
        assert len(result) == 2
        assert result[0] == Todo(path=Path('note_with_todos.md'),
                                 linenum=6,
                                 text="* [ ] this one's a task")
        assert result[1] == Todo(path=Path('note_with_todos.md'),
                                 linenum=10,
                                 text='[ ] this task is not a bullet')
