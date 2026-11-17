---
id: computing-software.software-engineering.typer.typer-first-steps
name: typer-first-steps
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, arguments, options, python, help-text]
level: intro
status: docs-checked
description: "Build a first Typer CLI: how a function's parameters become required CLI arguments or optional CLI options, bool flags, and --help text from a docstring."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/first-steps.md
  - https://github.com/fastapi/typer/blob/master/docs_src/first_steps/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/first_steps/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/first_steps/tutorial004_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/first_steps/tutorial005_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/first_steps/tutorial006_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer first steps: arguments, options and help text

Typer turns the parameters of a plain Python function into a command line interface. Put the function in `main.py` and pass it to `typer.run()`.

## Arguments vs options

- A **CLI argument** depends on position and is **required** by default (like `./myproject` in `ls ./myproject`).
- A **CLI option** starts with `--`, does not depend on order and is **optional** by default (like `--size`). It is also called a flag or switch.
- **CLI parameter** means either one. The required/optional defaults can be changed.

The simplest file:

```python
import typer


def main():
    print("Hello World")


if __name__ == "__main__":
    typer.run(main)
```

## How the function signature maps

A parameter with no default, e.g. `name: str`, becomes a required CLI argument. Missing it prints a usage error containing `Missing argument 'name'.`

```python
def main(name: str):
    print(f"Hello {name}")
```

Two such parameters become two positional arguments; order matters, and `main.py Gutiérrez Camila` cannot be disambiguated:

```python
def main(name: str, lastname: str):
    print(f"Hello {name} {lastname}")
```

A `bool` parameter with default `False` automatically creates both `--formal` and `--no-formal` (help shows `[default: no-formal]`). It can appear anywhere on the command line:

```python
def main(name: str, lastname: str, formal: bool = False):
    if formal:
        print(f"Good day Ms. {name} {lastname}.")
    else:
        print(f"Hello {name} {lastname}")
```

Giving a parameter a default value such as `lastname: str = ""` turns it from an argument into an option `--lastname`, which takes whatever value is to its right. `--lastname Gutiérrez Camila` works.

```python
def main(name: str, lastname: str = "", formal: bool = False):
```

To pass one value containing spaces to an argument, quote it: `"Camila Gutiérrez"`.

## Document the app

A docstring on the function is used as the help text shown by `--help`:

```python
def main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to 'name', optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
```

`python main.py --help` shows Usage, the docstring, an Arguments panel (marked `[required]`) and an Options panel.

## Run it

```console
$ uv run python main.py Camila --lastname Gutiérrez
$ typer main.py run
```

The `typer` command (after activating the project's virtual environment, and once completion is installed) is an alternative to `uv run python main.py` that gives TAB completion for your own scripts. A packaged app does not need it.

## Terminology tip

In Python, "parameter" and "argument" are used almost interchangeably; in CLIs neither word implies required or ordered. This guide uses "CLI argument", "CLI option" and "CLI parameter" to stay unambiguous.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/first-steps.md with its example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
