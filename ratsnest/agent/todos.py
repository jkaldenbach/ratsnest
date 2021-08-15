"""Agent that watches the todo file for completion state changes and updates the notes files accordingly."""
import hashlib
import pathlib
import re
import time

from ratsnest.config import Config

BLOCKSIZE = 65536


class TodoAgent:
    LOC_RE = re.compile(r'\@\[(.+)\:(\d+)\]')
    COMPLETED_RE = re.compile(r'(\[[xX]\])\s+')

    def __init__(self, config: Config):
        self.config = config
        self.current_hash = None

    def start(self, run_event):
        self.current_hash = self.compute_hash()
        print(f'Watching for changes to {self.config.todo_file}')
        while run_event.is_set():
            time.sleep(1)
            new_hash = self.compute_hash()
            if self.current_hash == new_hash:
                continue
            print(f'{self.config.todo_file} has changed')
            self.current_hash = new_hash
            self.update_todo_files()

    def compute_hash(self):
        hasher = hashlib.md5()
        with open(self.config.todo_file, 'rb') as file:
            buffer = file.read(BLOCKSIZE)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = file.read(BLOCKSIZE)
        return hasher.hexdigest()

    def update_todo_files(self):
        todos_to_complete = []
        with open(self.config.todo_file) as todos:
            for todo in todos:
                if self.COMPLETED_RE.search(todo):
                    print(f'Completed todo {todo}')
                    location = self.LOC_RE.search(todo)
                    filename, linenum = location.group(1, 2)
                    linenum = int(linenum)
                    file_path = pathlib.Path(self.config.notes_dir) / filename
                    new_note = ''
                    with open(file_path, 'r') as note_file:
                        for n, line in enumerate(note_file, 1):
                            if n == linenum:
                                new_note += todo.replace(location.group(0), '')
                            else:
                                new_note += line
                    with open(file_path, 'w') as note_file:
                        note_file.write(new_note)
