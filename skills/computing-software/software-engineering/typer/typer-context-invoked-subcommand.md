---
id: computing-software.software-engineering.typer.typer-context-invoked-subcommand
name: typer-context-invoked-subcommand
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, context, callback, invoke-without-command, extra-args]
level: advanced
status: docs-checked
description: "Use typer.Context in a callback to read the subcommand name, run the callback with no command via invoke_without_command, and capture extra raw args."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/context.md
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/context/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/context/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/context/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/context/tutorial004_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer Context in callbacks and commands

Every Typer app has a special hidden Context object. Declare a function parameter of type `typer.Context` in a command or in the main callback and Typer injects it.

## Read the invoked subcommand

In a callback, `ctx.invoked_subcommand` holds the name of the command about to run:

```python
@app.callback()
def main(ctx: typer.Context):
    print(f"About to execute command: {ctx.invoked_subcommand}")
```

Running `main.py create Camila` prints `About to execute command: create` and then `Creating user: Camila`; `delete` behaves the same with its own name.

## Run the callback without a subcommand

By default the callback only runs right before a command, and with no command the help is shown. Pass `invoke_without_command=True` to the callback to make it run anyway:

```python
@app.callback(invoke_without_command=True)
def main():
    print("Initializing database")
```

Now `main.py` alone prints `Initializing database` instead of help, and `main.py create Camila` still runs the callback first.

## Make the callback exclusive

To run the callback body only when no subcommand is given, combine `invoke_without_command=True` with a context check: if `ctx.invoked_subcommand is None`, you are calling the main program directly.

```python
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Manage users in the awesome CLI app.
    """
    if ctx.invoked_subcommand is None:
        print("Initializing database")
```

Then `main.py` prints `Initializing database`, while `main.py create Camila` skips it and only prints `Creating user: Camila`.

## Configure the context and keep extra args

Context settings can be passed when creating a command or callback. The page uses `ignore_unknown_options` and `allow_extra_args` to accept parameters not declared in your program, then reads them from `ctx.args`, a `list` of `str`.

```python
@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def main(ctx: typer.Context):
    for extra_arg in ctx.args:
        print(f"Got extra arg: {extra_arg}")
```

Example result of `main.py --name Camila --city Berlin`: it prints `Got extra arg: --name`, `Got extra arg: Camila`, `Got extra arg: --city`, `Got extra arg: Berlin`, one per line.

Gotcha: `ctx.args` is raw. Option names and values are all saved together as a raw list of strings.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/commands/context.md with its four example files. Removed or trimmed: the Click-style description of the context and the claim that extra args must be paired by hand.

Method: documentation only; no commands were run.
