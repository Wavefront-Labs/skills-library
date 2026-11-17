---
id: computing-software.software-engineering.typer.typer-subcommand-name-and-help-precedence
name: typer-subcommand-name-and-help-precedence
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, add-typer, help, naming, precedence]
level: advanced
status: docs-checked
description: "Resolve the name and help text of a Typer sub-command group from Typer(), @callback, and add_typer, with the full precedence order from lowest to highest."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/subcommands/name-and-help.md
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/name_help/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/name_help/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/name_help/tutorial005_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/name_help/tutorial006_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/name_help/tutorial007_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/name_help/tutorial008_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sub-command name and help precedence

When adding a Typer app to another, you set the group command name with `name`, e.g. `app.add_typer(users.app, name="users")`, and may set `help` there too. `help` can come from several places; each later one overrides the previous.

## Inferred help (from callback docstrings)

A command made with `@app.command()` takes its name from the function name and its help from the docstring. For sub-apps, help is inferred from callback docstrings. Lowest to highest priority:

1. `sub_app = typer.Typer(callback=some_function)`
2. `@sub_app.callback()`
3. `app.add_typer(sub_app, callback=new_function)`

Example: a callback docstring `Manage users in the app.` shows up beside `users` in the main help and under `main.py users --help`.

```python
users_app = typer.Typer()
app.add_typer(users_app, name="users")


@users_app.callback()
def users():
    """
    Manage users in the app.
    """
```

With all three set, `add_typer(..., callback=...)` wins and its docstring replaces the earlier ones:

```python
def old_callback():
    """
    Old callback help.
    """


users_app = typer.Typer(callback=old_callback, name="users")


def new_users():
    """
    I have the highland! Create some users.
    """


app.add_typer(users_app, callback=new_users, name="new-users")


@users_app.callback()
def users():
    """
    Manage users in the app.
    """
```

Here the help shown is `I have the highland! Create some users.` and the command is named `new-users`.

## Explicit help and name (always beat inferred help)

Explicit help ranks higher than any inferred help. Full recap of help, lowest to highest:

- inferred from `Typer(callback=...)`
- inferred from `@sub_app.callback()`
- inferred from `add_typer(sub_app, callback=...)`
- explicit `sub_app = typer.Typer(help="Some help.")`
- explicit `app.add_typer(sub_app, help="Some help.")`

Explicit help on `typer.Typer`, with the other callbacks present only to show they do not matter (the command shows as `exp-users` with help `Explicit help.`):

```python
users_app = typer.Typer(callback=old_callback, name="exp-users", help="Explicit help.")
```

The page also shows `help` in the callback decorator, `@users_app.callback(help="Help from callback for users.")`, overriding the `Typer(help="Explicit help.")` text in that example (result `Help from callback for users.`).

Name, lowest to highest:

- `typer.Typer(name="some-name")`
- `app.add_typer(sub_app, name="some-name")`

So `app.add_typer(sub_app, name="some-name", help="Some help.")` always wins; e.g. name `cake-sith-users` with help `Unlimited powder! Eh, users.`:

```python
app.add_typer(
    users_app,
    callback=new_users,
    name="cake-sith-users",
    help="Unlimited powder! Eh, users.",
)
```

## Gotcha

Before Typer 0.14.0 the command name was also inferred from the callback function name. That is no longer the case; set `name` explicitly.

## Checked

2026-11-07. Read in full against subcommands/name-and-help.md and docs_src name_help examples 1-8 (Typer docs repository checkout). Confirmed: inferred and explicit help precedence, name precedence, 0.14.0 note, example outputs. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
