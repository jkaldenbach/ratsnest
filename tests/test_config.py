import os

from ratsnest.config import Config


def test_todo_file():
    config = Config()
    assert config.todo_file == os.path.expanduser(
        f'{config.notes_dir}/todo.md')


def test_update_todo_file():
    config = Config()
    config.todo_file = '~/stuffigottado.md'
    assert config.todo_file == os.path.expanduser('~/stuffigottado.md')
