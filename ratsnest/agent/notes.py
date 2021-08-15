"""Agent that watches the notes directory for updates and re-builds the todo file accordiingly."""
from threading import Timer
import time

import watchdog
import watchdog.events
import watchdog.observers

from ratsnest.config import Config
from ratsnest.startup import startup


class ChangeHandler(watchdog.events.PatternMatchingEventHandler):
    DEBOUNCE = 3

    def __init__(self, config: Config):
        super().__init__(patterns=['*.md'], ignore_patterns=[config.todo_file])
        self.config = config
        self._timer = None

    def _run(self):
        self._timer = None
        startup(self.config)

    def on_any_event(self, event):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = Timer(self.DEBOUNCE, self._run)
        self._timer.start()


class NoteAgent:
    def __init__(self, config: Config):
        self.config = config
        self.observer = watchdog.observers.Observer()
        self.observer.schedule(ChangeHandler(self.config),
                               path=self.config.notes_dir,
                               recursive=True)

    def start(self, run_event):
        self.observer.start()
        while run_event.is_set():
            time.sleep(1)
        self.observer.stop()
        self.observer.join()
