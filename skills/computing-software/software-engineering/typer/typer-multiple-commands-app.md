---
id: computing-software.software-engineering.typer.typer-multiple-commands-app
name: typer-multiple-commands-app
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, commands, no-args-is-help, ordering, decorator]
level: intro
status: docs-checked
description: "Create a Typer app with several commands, show help when no command is given with no_args_is_help=True, and control the order commands appear in help."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/index.md
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/index/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/index/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/index/tutorial004_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A Typer app with multiple commands

A Typer CLI can contain several commands (also called subcommands), like `git push` and `git pull`, each with its own CLI arguments and options. A command looks like a CLI argument (a name with no `--`), but its name is predefined and it groups functionality.

## Create commands

Make an explicit `typer.Typer()` app and decorate one function per command with `@app.command()`. For a user manager with `create` and `delete`:

```python
import typer

app = typer.Typer()


@app.command()
def create():
    print("Creating user: Hiro Hamada")


@app.command()
def delete():
    print("Deleting user: Hiro Hamada")


if __name__ == "__main__":
    app()
```

`python main.py --help` shows `Usage: main.py [OPTIONS] COMMAND [ARGS]...` and the commands `create` and `delete`. Command names come from the function names by default.

## Help when no command is given

By default you must pass `--help`. Create the app with `no_args_is_help=True` and running `python main.py` alone shows the help:

```python
app = typer.Typer(no_args_is_help=True)
```

## Order in help

Commands are listed in the order they are declared in the file. Declare `delete` before `create` (same bodies as above) and `delete` is listed first:

```python
@app.command()
def delete():
    print("Deleting user: Hiro Hamada")


@app.command()
def create():
    print("Creating user: Hiro Hamada")
```

## Decorator facts

`@app.command()` registers the function in the app and leaves the function itself unmodified. If it is simple enough to work without `typer.Option()` or `typer.Argument()`, the same function could be used by both a Typer app and a FastAPI app by stacking both decorators.

Terminology: "command" can mean the program or one of its subcommands; the docs use "CLI application" for the program built with Typer and "command" for each subcommand.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/commands/index.md with its three example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
