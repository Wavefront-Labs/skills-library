---
id: computing-software.software-engineering.typer.typer-single-vs-multiple-commands
name: typer-single-vs-multiple-commands
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, commands, callback, single-command, python]
level: intro
status: docs-checked
description: "Understand why one Typer command becomes the main program, and keep a single command as a real subcommand by adding a callback, optionally for docs."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/one-or-multiple.md
  - https://github.com/fastapi/typer/blob/master/docs_src/typer_app/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/index/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/one_or_multiple/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/one_or_multiple/tutorial002_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One command or multiple commands in Typer

## Single command collapses into the app

If a Typer app has only one command, Typer makes that function the main CLI program, not a subcommand:

```python
@app.command()
def main(name: str):
    print(f"Hello {name}")
```

- `python main.py` without the argument fails: `Error: Missing argument 'name'.`
- `python main.py Camila` prints `Hello Camila`.
- `--help` shows `Usage: main.py [OPTIONS] {name}` and no command called `main`, even though the function is named `main`.

## Multiple commands become subcommands

Register a second command and Typer creates one CLI command per function:

```python
@app.command()
def create():
    print("Creating user: Hiro Hamada")


@app.command()
def delete():
    print("Deleting user: Hiro Hamada")
```

With `create` and `delete`, `main.py --help` shows `Usage: main.py [OPTIONS] COMMAND [ARGS]...` with both under Commands.

## One command that stays a subcommand

To keep a single command as `main.py create` (a real subcommand), add a callback to the app. The callback can do nothing:

```python
@app.callback()
def callback():
    pass
```

Now `--help` lists the single command `create`, and `python main.py create` prints `Creating user: Hiro Hamada`.

## Use the callback for documentation

Since the callback exists anyway, give it a docstring and it becomes the help text:

```python
@app.callback()
def callback():
    """
    Creates a single user Hiro Hamada.

    In the next version it will create 5 more users.
    """
```

`--help` shows that text under the usage line. The callback does nothing else and the command still works the same.

## Checked

2026-11-07. Read in full against commands/one-or-multiple.md and docs_src examples (Typer docs repository checkout). Confirmed: single command collapses into the app, two commands, callback keeps a subcommand, docstring help. Removed or trimmed: an unsupported "why use this" sentence.

Method: documentation only; no commands were run.
