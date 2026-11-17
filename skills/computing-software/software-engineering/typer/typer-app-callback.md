---
id: computing-software.software-engineering.typer.typer-app-callback
name: typer-app-callback
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, callback, global-options, help-text, python]
level: practitioner
status: docs-checked
description: "Declare app-level CLI options like --verbose with @app.callback(), set callbacks via Typer(callback=...), override them, or use one only for help text."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/callback.md
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/callback/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/callback/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/callback/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/callback/tutorial004_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer callback for app-level parameters

A `typer.Typer()` app is a group of commands, and each command handles its own CLI parameters. To give the main program its own parameters (those placed before the command name), use a callback.

## Declaring a callback

`@app.callback()` is like `@app.command()`, but declares the parameters of the main CLI app. The page's example adds a `--verbose` option in a callback, then stores the flag in a module-level `state` that the commands read. (The page notes there are other ways to share the value; this is just sufficient for the example.)

```python
state = {"verbose": False}

# create/delete commands read state["verbose"]


@app.callback()
def main(verbose: bool = False):
    """
    Manage users in the awesome CLI app.
    """
    if verbose:
        print("Will write verbose output")
        state["verbose"] = True
```

The callback's docstring becomes the main help text, shown under `Usage: main.py [OPTIONS] COMMAND [ARGS]...`. The option appears as `--verbose / --no-verbose  [default: no-verbose]`.

## Option placement gotcha

`--verbose` belongs to the callback, so it must go before the command:

- `main.py --verbose create Camila` works.
- `main.py create --verbose Camila` fails with `Error: No such option: --verbose`.

## Other ways to attach a callback

- On creation: `app = typer.Typer(callback=some_function)` does the same thing as the decorator.

```python
def callback():
    print("Running a command")


app = typer.Typer(callback=callback)
```

- Override: if a callback was set in `typer.Typer(...)`, a later `@app.callback()` replaces it; only the new one runs.

```python
@app.callback()
def new_callback():
    print("Override callback, running a command")
```

- Documentation only: a callback with just a multi-line docstring is a convenient place for long help text, since indentation is handled for you. The help then shows all the lines, and commands work as normal.

```python
@app.callback()
def callback():
    """
    Manage users CLI app.

    Use it with the create command.

    A new user with the given NAME will be created.
    """
```

Verify: with a creation-time callback, `main.py create Camila` prints the callback message first (`Running a command`) and then `Creating user: Camila`; with an `@app.callback()` override, the override's message (`Override callback, running a command`) appears instead.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/commands/callback.md with its four callback examples. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
