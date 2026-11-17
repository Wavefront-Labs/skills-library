---
id: computing-software.software-engineering.typer.typer-repeatable-options
name: typer-repeatable-options
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, options, list, repeatable, float]
level: intro
status: docs-checked
description: "Let a Typer CLI option be repeated (--user A --user B) by annotating it as list[str] or list[float] and handling the None default."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/multiple-values/multiple-options.md
  - https://github.com/fastapi/typer/blob/master/docs_src/multiple_values/multiple_options/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/multiple_values/multiple_options/tutorial002_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer options that can be repeated

Declare a CLI option with a standard Python `list` and users may repeat the option; you receive all values in order.

```python
@app.command()
def main(user: Annotated[list[str] | None, typer.Option()] = None):
    if not user:
        print(f"No provided users (raw input = {user})")
        raise typer.Abort()
    for u in user:
        print(f"Processing user: {u}")
```

Check it:

- No option: the value is `None`, so the example prints `No provided users (raw input = None)` and `Aborted!`. Handle that case.
- `--user Camila` prints `Processing user: Camila`.
- `--user Camila --user Rick --user Morty` processes each in turn.

## Other element types

Typer converts values to the declared element type. With floats:

```python
@app.command()
def main(number: Annotated[list[float], typer.Option()] = []):
    print(f"The sum is {sum(number)}")
```

- No option: `The sum is 0`.
- `--number 2`: `The sum is 2.0`.
- `--number 2 --number 3 --number 4.5`: `The sum is 9.5`.

## Notes

- For an option that takes several values after a single flag, see the typer-tuple-options skill.

## Checked

2026-11-07. Read in full against multiple-values/multiple-options.md and docs_src examples 1-2 (Typer docs repository checkout). Confirmed: list[str] and list[float] options, None default, outputs. Removed or trimmed: an unsupported note about one value per flag occurrence.

Method: documentation only; no commands were run.
