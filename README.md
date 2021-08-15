# Ratsnest

Ratsnest is a service for aggregating checklist items in markdown notes files into a centralized todo list. Todos that are checked-off in the aggregated list are updated in the source note.

## Requirements

Ratsnest uses `poetry` and is written in Python 3.9.

## Configuration

Config file and command line args are currently not supported. Notes should be in `~/notes`, and the todo file will be generated at `~/notes/todo.md`.

## Running

```bash
poetry run ratsnest/main.py
```
