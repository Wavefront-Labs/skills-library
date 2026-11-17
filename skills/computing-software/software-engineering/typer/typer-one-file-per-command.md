---
id: computing-software.software-engineering.typer.typer-one-file-per-command
name: typer-one-file-per-command
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, project-structure, add-typer, modules, callbacks]
level: practitioner
status: docs-checked
description: "Split a Typer CLI into one module per command with add_typer; an unnamed sub-app puts commands at top level, a named one groups them, which affects callbacks."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/one-file-per-command.md
  - https://github.com/fastapi/typer/blob/master/docs_src/one_file_per_command/app_py310/main.py
  - https://github.com/fastapi/typer/blob/master/docs_src/one_file_per_command/app_py310/version.py
  - https://github.com/fastapi/typer/blob/master/docs_src/one_file_per_command/app_py310/users/__init__.py
  - https://github.com/fastapi/typer/blob/master/docs_src/one_file_per_command/app_py310/users/add.py
  - https://github.com/fastapi/typer/blob/master/docs_src/one_file_per_command/app_py310/users/delete.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One file per command in Typer

As a CLI grows, split it into modules and combine them with `app.add_typer()`.

## Layout

Target commands: `version`, `users add 'name'`, `users delete 'name'`.

```text
mycli/
├── __init__.py
├── main.py
├── users/
│   ├── __init__.py
│   ├── add.py
│   └── delete.py
└── version.py
```

## Pattern

- Every module (`version.py`, `users/add.py`, `users/delete.py`, and the `users` package `__init__.py`) creates its own `typer.Typer()` app. That is unnecessary in a single-file app, but here it lets the parent include it with `add_typer()`.
- `users/__init__.py` defines the `users` app and includes the `add` and `delete` apps.
- `main.py` imports `version` and `users` and registers them. For `users` it passes `name="users"`; for `version` it passes no name.

`mycli/version.py`:

```python
import typer

app = typer.Typer()


@app.command()
def version():
    print("My CLI Version 1.0")
```

`mycli/users/add.py` (`delete.py` is the same with `delete` and `Deleting user: {name}`):

```python
import typer

app = typer.Typer()


@app.command()
def add(name: str):
    print(f"Adding user: {name}")
```

`mycli/users/__init__.py`:

```python
import typer

from .add import app as add_app
from .delete import app as delete_app

app = typer.Typer()

app.add_typer(add_app)
app.add_typer(delete_app)
```

`mycli/main.py`:

```python
import typer

from .users import app as users_app
from .version import app as version_app

app = typer.Typer()

app.add_typer(version_app)
app.add_typer(users_app, name="users")


if __name__ == "__main__":
    app()
```

## Name or no name

- With no name (or `None`), the sub-app's commands are added directly at the top level. So the `version` command is top-level.
- With a name, the commands are grouped under a sub-command: `users add` and `users delete`.

## Running

`python -m mycli.main version` prints `My CLI Version 1.0`; `python -m mycli.main users add Camila` prints `Adding user: Camila`. Once packaged and installed, use `mycli version` and `mycli users add Camila`.

## Callback gotcha

An unnamed sub-app is merged into the top level, so only the main app's callback is used. To use a sub-app's callback, include it with a name. Here a `users` callback would run; a `version` callback would not.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/one-file-per-command.md with its example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
