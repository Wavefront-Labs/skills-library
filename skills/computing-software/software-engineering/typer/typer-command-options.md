---
id: computing-software.software-engineering.typer.typer-command-options
name: typer-command-options
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, commands, options, prompt, force, python]
level: intro
status: docs-checked
description: "Give each Typer command different CLI options and arguments, such as a --force flag that skips a confirmation prompt, and what the help and names look like."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/options.md
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/options/tutorial001_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command CLI options in Typer

Each command in a Typer app can have its own, different mix of CLI arguments and CLI options.

## The page's example app

| Command | Parameters |
| --- | --- |
| `create` | `username` argument |
| `delete` | `username` argument, `--force` option (prompted if not provided) |
| `delete-all` | `--force` option (prompted if not provided) |
| `init` | none |

```python
@app.command()
def delete(
    username: str,
    force: Annotated[
        bool, typer.Option(prompt="Are you sure you want to delete the user?")
    ],
):
    if force:
        print(f"Deleting user: {username}")
    else:
        print("Operation cancelled")


@app.command()
def delete_all(
    force: Annotated[
        bool, typer.Option(prompt="Are you sure you want to delete ALL users?")
    ],
):
    if force:
        print("Deleting all users")
    else:
        print("Operation cancelled")
```

`create(username: str)` and `init()` are plain commands. `python main.py --help` lists `create`, `delete`, `delete-all`, `init`.

Gotcha/tip: command names are generated from function names with `_` replaced by `-`, so the function `delete_all` is the command `delete-all`.

## Behaviour to expect

- `main.py create Camila` prints `Creating user: Camila`.
- `main.py delete Camila` asks `Are you sure you want to delete the user? [y/n]:`. Answering `y` prints `Deleting user: Camila`; answering `n` prints `Operation cancelled`.
- `main.py delete-all` asks `Are you sure you want to delete ALL users? [y/n]:`, with the same `y` / `n` outcomes (`Deleting all users` or `Operation cancelled`).
- `main.py delete-all --force` skips the confirmation and prints `Deleting all users`.
- `main.py init` takes no parameters and prints `Initializing user database`.

## How to apply

1. Declare the argument or option as a parameter on the specific command function only.
2. For a confirmable destructive action, give a required `bool` option a `prompt=` (as above), so it asks unless `--force` is passed.

Verify: `main.py delete-all --force` runs without a prompt and prints `Deleting all users`.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/commands/options.md with its example file. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
