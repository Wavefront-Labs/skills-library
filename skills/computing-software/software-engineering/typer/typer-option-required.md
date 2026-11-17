---
id: computing-software.software-engineering.typer.typer-option-required
name: typer-option-required
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, required-option, annotated, ellipsis]
level: intro
status: docs-checked
description: "Make a Typer CLI option required by using typer.Option() in Annotated with no default, or the older default=... Ellipsis style."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options/required.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options/required/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/required/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/required/tutorial002_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Required Typer CLI options

By default options are optional and arguments are required. To flip an option to required:

## Preferred: Annotated, no default

```python
@app.command()
def main(name: str, lastname: Annotated[str, typer.Option()]):
    print(f"Hello {name} {lastname}")
```

No default value on the parameter plus `typer.Option()` in `Annotated` means: still an option (`--lastname`), but required.

## Older style

Using `typer.Option()` as the parameter default, either pass nothing to `default`:

```python
def main(name: str, lastname: str = typer.Option()):
```

or pass the Ellipsis explicitly:

```python
def main(name: str, lastname: str = typer.Option(default=...)):
```

`...` is Python's `Ellipsis` constant; it tells Typer "no default, required". The page recommends the `Annotated` version so the code means the same in plain Python and in Typer.

## Behaviour

Omitting it gives:

```
Error: Missing option '--lastname'.
```

and `--help` shows `--lastname <str>  [required]`. Supplying it (`python main.py Camila --lastname Gutiérrez`) works.

Verify: running without `--lastname` prints "Error: Missing option '--lastname'." after the usage line.

## Checked

2026-11-07. Read in full against options/required.md and docs_src required examples (Typer docs repository checkout). Confirmed: Annotated with no default, Option() and default=... styles, Missing option error, [required] in help. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
