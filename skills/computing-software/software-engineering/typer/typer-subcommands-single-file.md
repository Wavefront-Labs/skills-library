---
id: computing-software.software-engineering.typer.typer-subcommands-single-file
name: typer-subcommands-single-file
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, subcommands, single-file, command-name, add-typer]
level: practitioner
status: docs-checked
description: "Keep Typer subcommand groups in one file: add apps at the top, give functions unique names, and pass explicit command names so users still type items create."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/subcommands/single-file.md
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/tutorial002_py310/main.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subcommands in a single file

If the whole application must live in one file, the add_typer ideas still apply.

## Create the apps first

You can create the `typer.Typer()` objects and add them to the main one at the top of the file, before defining any commands. Commands added to each sub-app later still work.

```python
import typer

app = typer.Typer()
items_app = typer.Typer()
app.add_typer(items_app, name="items")
users_app = typer.Typer()
app.add_typer(users_app, name="users")
```

## Unique function names

With `create` existing for both `users` and `items`, functions called just `create()` would overwrite each other. Use longer function names, such as `items_create` and `users_create`.

## Explicit command names

You still want `main.py items create`, not `main.py items items-create`. Pass the desired name to the decorator:

```python
@items_app.command("create")
def items_create(item: str):
    print(f"Creating item: {item}")
```

Do the same for each subcommand:

```python
@items_app.command("delete")
def items_delete(item: str):
    print(f"Deleting item: {item}")


@items_app.command("sell")
def items_sell(item: str):
    print(f"Selling item: {item}")


@users_app.command("create")
def users_create(user_name: str):
    print(f"Creating user: {user_name}")


@users_app.command("delete")
def users_delete(user_name: str):
    print(f"Deleting user: {user_name}")
```

## Check it

- `python main.py --help` lists `items` and `users`.
- `python main.py items --help` lists `create`, `delete`, `sell`.
- `python main.py items create Wand` prints `Creating item: Wand`.
- `python main.py items sell Vase` prints `Selling item: Vase`.
- `python main.py users create Camila` prints `Creating user: Camila`.

Gotcha: forgetting the explicit name gives the function-derived command name (for example `items-create`).

## Checked

2026-11-07. Read in full against subcommands/single-file.md and docs_src subcommands/tutorial002_py310/main.py (Typer docs repository checkout). Confirmed: apps at the top, unique function names, explicit command names, the check outputs. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
