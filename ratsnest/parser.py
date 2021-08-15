from dataclasses import dataclass
import os
import pathlib
import re
import typing as t
from uuid import uuid4

from ratsnest.config import Config

TODO_PATTERN = re.compile(r'^(( {0,3})([\*\+-]|\d{1,9}[.)]) )?(\[( +)?\])')
# CHECKED_TODO_PATTERN = re.compile(r'(\[[xX]\])\s+')


@dataclass
class Todo:
    linenum: int
    path: str
    text: str
    checked: bool = False

    def __str__(self):
        return f'{self.text.strip()} @[{self.path}:{self.linenum}]\n'


def parse_file(file_path: t.Union[str, pathlib.Path],
               config: Config) -> t.List[Todo]:
    notes_path = pathlib.Path(config.notes_dir)
    path = file_path.relative_to(notes_path)

    todos = []
    try:
        with open(file_path, 'r') as file:
            for linenum, line in enumerate(file, 1):
                if TODO_PATTERN.match(line):
                    todos.append(
                        Todo(linenum=linenum, path=path, text=line.strip()))
    except FileNotFoundError:
        pass
    return todos
