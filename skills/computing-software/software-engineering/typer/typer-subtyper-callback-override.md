---
id: computing-software.software-engineering.typer.typer-subtyper-callback-override
name: typer-subtyper-callback-override
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, callback, add-typer, precedence, subcommands]
level: advanced
status: docs-checked
description: "Know which Typer sub-app callback wins: Typer(callback=), @app.callback(), then add_typer(callback=) with the highest priority regardless of order."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/subcommands/callback-override.md
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/callback_override/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/callback_override/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/callback_override/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/callback_override/tutorial004_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sub-Typer callback and override order

A callback always executes and defines the CLI arguments and options that go before a command. A sub-Typer (an app added into another with `app.add_typer()`) can have its own callback for parameters that go before its commands and any extra code.

## Four places to set a sub-app callback

1. `@users_app.callback()` decorator on a function. In the example it defines no parameters and only prints `Running a users command`; `main.py users create Camila` then prints that message before `Creating user: Camila`.
2. At creation: `users_app = typer.Typer(callback=some_function)`. Same result, another place.
3. Override the creation callback with `@users_app.callback()`. The decorator takes precedence over `typer.Typer(callback=...)`, so the new function (e.g. `user_callback()`) runs and its message (`Callback override, running users command`) appears.
4. Override when adding: `app.add_typer(users_app, callback=callback_for_add_typer)`. This has the highest priority.

Decorator form (1):

```python
@users_app.callback()
def users_callback():
    print("Running a users command")
```

Creation form (2), then override (3) with the decorator:

```python
def default_callback():
    print("Running a users command")


users_app = typer.Typer(callback=default_callback)
app.add_typer(users_app, name="users")


@users_app.callback()
def user_callback():
    print("Callback override, running users command")
```

Highest priority (4):

```python
def callback_for_add_typer():
    print("I have the high land! Running users command")


app.add_typer(users_app, name="users", callback=callback_for_add_typer)
```

## Gotcha: order of execution does not matter

Precedence belongs to `app.add_typer()` and is not affected by where in the file things appear. Even if another callback is defined further down, the one from `add_typer()` wins. In the example the output starts with that function's message (`I have the high land! Running users command`) before `Creating user: Camila`.

## Priority summary (lowest to highest)

`Typer(callback=...)`, then `@sub_app.callback()`, then `add_typer(callback=...)`.

## Checked

2026-11-07. Read in full against subcommands/callback-override.md and docs_src callback_override examples 1-4 (Typer docs repository checkout). Confirmed: the four callback places, precedence and the order-independence note, output messages. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
