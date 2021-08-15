import os
from dataclasses import asdict, dataclass


@dataclass
class Config:
    notes_dir: str = '~/notes'
    _todo_file: str = '{notes_dir}/todo.md'

    def __getattribute__(self, name):
        """Expanduser for all config vars that are paths."""
        if name in ['notes_dir', 'todo_file']:
            return os.path.expanduser(object.__getattribute__(self, name))
        return object.__getattribute__(self, name)

    @property
    def todo_file(self):
        """Format the todo_file on demand."""
        return self._todo_file.format(**asdict(self))

    @todo_file.setter
    def todo_file(self, value):
        self._todo_file = value
