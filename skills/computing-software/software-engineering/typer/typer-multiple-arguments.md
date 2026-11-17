---
id: computing-software.software-engineering.typer.typer-multiple-arguments
name: typer-multiple-arguments
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, arguments, list, tuple, variadic]
level: practitioner
status: docs-checked
description: "Accept many values for one Typer CLI argument with list, or a fixed count with tuple and defaults; note the last-command limit for lists."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/multiple-values/arguments-with-multiple-values.md
  - https://github.com/fastapi/typer/blob/master/docs_src/multiple_values/arguments_with_multiple_values/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/multiple_values/arguments_with_multiple_values/tutorial002_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer arguments with multiple values

## Variable count: list

Declare a CLI argument as a `list` and the user can pass as many values as they like:

```python
from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def main(files: list[Path], celebration: str):
    for path in files:
        if path.is_file():
            print(f"This file exists: {path.name}")
            print(celebration)


if __name__ == "__main__":
    app()
```

Verify: `python main.py ./index.md ./first-steps.md woohoo!` processes both files and prints `woohoo!` after each. A final argument such as `celebration` is still filled correctly even after an arbitrary number of `files`.

Gotcha: a `list` argument can only be used in the last command when you have subcommands, because it takes everything to the right and treats it as its own values.

## Fixed count: tuple

Use a `tuple` when you need an exact number of values and types; it can also carry defaults:

```python
@app.command()
def main(
    names: Annotated[
        tuple[str, str, str], typer.Argument(help="Select 3 characters to play with")
    ] = ("Harry", "Hermione", "Ron"),
):
    for name in names:
        print(f"Hello {name}")
```

Help shows `names...  Select 3 characters to play with  [default: Harry, Hermione, Ron]`.

- No values: the defaults are used (`Hello Harry`, `Hello Hermione`, `Hello Ron`).
- Wrong count: `python main.py Draco Hagrid` gives `Error: Argument 'names' takes 3 values`.
- Exact count: `Draco Hagrid Dobby` works.

## Choosing

- Unknown number of items: `list[...]`.
- Known number, perhaps with defaults: `tuple[...]`.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/multiple-values/arguments-with-multiple-values.md with its two example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
