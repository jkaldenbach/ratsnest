import os
import pathlib

from ratsnest.config import Config
from ratsnest.parser import parse_file


def startup(config: Config):
    # open todo file and delete existing contents
    with open(config.todo_file, 'w') as todo_file:
        # walk the notes directory
        all_todos = []
        for root, _, files in os.walk(config.notes_dir):
            for file in files:
                if file[-3:] != '.md':
                    continue
                # parse each note
                file_path = pathlib.Path(os.path.join(root, file))
                all_todos += parse_file(file_path, config)

        # write the todos to the file
        for todo in all_todos:
            todo_file.write(str(todo))
