---
id: computing-software.software-engineering.typer.typer-add-typer-subcommands
name: typer-add-typer-subcommands
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, add-typer, subcommands, composition, python]
level: practitioner
status: docs-checked
description: "Compose Typer apps by nesting one typer.Typer() inside another with app.add_typer(sub_app, name=...) to make command groups like users and items."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/subcommands/add-typer.md
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/tutorial001_py310/main.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add a Typer app inside another (add_typer)

Core idea: each `typer.Typer()` can be a CLI app by itself, but can also be added as a command group to another Typer app.

## Steps

Suppose `items.py` and `users.py` each define their own `app = typer.Typer()` with commands `create` and `delete` (items also has `sell`), for example:

```python
import typer

app = typer.Typer()


@app.command()
def create(item: str):
    print(f"Creating item: {item}")
...
@app.command()
def sell(item: str):
    print(f"Selling item: {item}")


if __name__ == "__main__":
    app()
```

(`users.py` is the same shape, with a `user_name: str` argument and `Creating user: ...` output.) To combine them as subcommands, like `git remote`, create `main.py`:

```python
import typer

import items
import users

app = typer.Typer()
app.add_typer(users.app, name="users")
app.add_typer(items.app, name="items")

if __name__ == "__main__":
    app()
```

What this does:

1. Imports the modules `users.py` and `items.py`.
2. Creates the main `typer.Typer()` application.
3. Uses `app.add_typer()` to include each sub-app.
4. Defines the `name` used as the command that groups each sub-Typer's commands.

## Result

`python main.py --help` lists the commands `users` and `items`. Each shows its own commands:

- `python main.py items --help` lists `create`, `delete`, `sell`.
- `python main.py items create Wand` prints `Creating item: Wand`.
- `python main.py items sell Vase` prints `Selling item: Vase`.
- `python main.py users create Camila` prints `Creating user: Camila`.

You still call `python main.py`, now followed by the group name.

## Notes

- Do it to any depth: for sub-sub-subcommands, create more `typer.Typer()` apps and chain them with `app.add_typer()`.
- Each module can still run alone with its own `app()`.
- The page says later sections add more features to this core idea.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/subcommands/add-typer.md with items.py, users.py and main.py. Removed or trimmed: the unconfirmed claim that only the final entry file needs the main block when packaged, and the list of what later sections cover.

Method: documentation only; no commands were run.
