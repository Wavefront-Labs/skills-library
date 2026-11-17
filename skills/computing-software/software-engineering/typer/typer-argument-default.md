---
id: computing-software.software-engineering.typer.typer-argument-default
name: typer-argument-default
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, argument, default-value, default-factory]
level: practitioner
status: docs-checked
description: "Give a Typer CLI argument a default value or a dynamically generated one with default_factory, and why not to wrap it in Optional."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/arguments/default.md
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/default/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/default/tutorial002_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer CLI arguments with defaults

A `typer.Argument()` with a default makes the argument optional.

## Static default

```python
@app.command()
def main(name: Annotated[str, typer.Argument()] = "Wade Wilson"):
    print(f"Hello {name}")
```

`--help` shows `name  [default: Wade Wilson]` and the usage line shows `[name]`. Running with no argument uses the default; `python main.py Camila` overrides it.

## Do not use Optional here

The value is always a `str` (user-supplied or the default), never `None`, so do not annotate `Optional[str]`. `Optional` only tells Python the value could be `None`; it does not tell Typer whether the parameter is required.

## Dynamic default: default_factory

Pass a function as `default_factory`; it is called to create the default each time:

```python
def get_name():
    return random.choice(["Deadpool", "Rick", "Morty", "Hiro"])


@app.command()
def main(name: Annotated[str, typer.Argument(default_factory=get_name)]):
    print(f"Hello {name}")
```

Help shows `name  [default: (dynamic)]`. Each run without an argument yields a fresh value; passing an argument overrides the factory.

"Factory" simply means "function that creates the default value".

Verify: repeated runs with no argument print different greetings (the page shows Deadpool, Hiro, Rick), while `python main.py Camila` prints "Hello Camila".

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/arguments/default.md with its two examples. Removed or trimmed: the gloss that brackets mean optional.

Method: documentation only; no commands were run.
