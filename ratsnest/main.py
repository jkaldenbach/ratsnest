import threading

from ratsnest.agent import NoteAgent, TodoAgent
from ratsnest.config import Config
from ratsnest.startup import startup

if __name__ == '__main__':
    config = Config()
    startup(config)
    run_event = threading.Event()
    run_event.set()
    todo_agent = threading.Thread(target=TodoAgent(config).start,
                                  args=(run_event, ))
    note_agent = threading.Thread(target=NoteAgent(config).start,
                                  args=(run_event, ))
    try:
        todo_agent.start()
        note_agent.start()
        todo_agent.join()
        note_agent.join()
    except KeyboardInterrupt:
        print('Stopping')
        run_event.clear()
        todo_agent.join()
        note_agent.join()
