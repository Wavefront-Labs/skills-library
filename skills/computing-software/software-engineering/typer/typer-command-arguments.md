---
id: computing-software.software-engineering.typer.typer-command-arguments
name: typer-command-arguments
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, commands, arguments, subcommands, python]
level: intro
status: docs-checked
description: "Give each Typer command its own CLI arguments, and know that parameters belong to the command to their left, before any further subcommand."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/arguments.md
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/callback.md
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/arguments/tutorial001_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer command CLI arguments

Use this when a Typer app has several commands and each needs its own positional input, such as `create` and `delete` both taking a `username`.

## How it works

Commands in a Typer app (registered with `@app.command()`) can each declare their own CLI arguments, exactly like the single-command case. Declare a function parameter such as `username: str` on the command function and Typer turns it into a required positional argument for that command only.

```python
@app.command()
def create(username: str):
    print(f"Creating user: {username}")


@app.command()
def delete(username: str):
    print(f"Deleting user: {username}")
```

```console
$ python main.py create --help
Usage: main.py create [OPTIONS] {username}

Arguments:
  username  [required]
```

Calling `python main.py create Camila` prints `Creating user: Camila`, and `python main.py delete Camila` prints `Deleting user: Camila`.

## Where parameters go

Everything to the right of the command name is a CLI parameter (argument or option) for that command. So `main.py create Camila` passes `Camila` to `create`.

Technically, it is everything to the right of the command and before any further subcommand. When commands are grouped into sub-apps (command groups), those subcommands take their own parameters.

## Checklist

- One `@app.command()` function per command; each function's parameters are independent.
- Check a command's signature with `python main.py <command> --help`.
- Required arguments are marked `[required]` in the help.
- Parameters for the app itself (before the command name) need a callback, not a command; see the callback skill.

Verify: `python main.py create --help` shows `Usage: main.py create [OPTIONS] {username}` and lists `username  [required]` under Arguments.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/commands/arguments.md and docs/tutorial/commands/callback.md. Removed or trimmed: the claim that a group in between can take its own parameters, which the arguments page does not state.

Method: documentation only; no commands were run.
