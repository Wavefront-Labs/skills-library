---
id: computing-software.software-engineering.typer.typer-bool-flags
name: typer-bool-flags
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, bool, flags, options, python]
level: intro
status: docs-checked
description: "Customise Typer bool option names: only --force, paired --accept/--reject, short -f/-F, and false-only names with a leading-space slash."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/bool.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/bool/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/bool/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/bool/tutorial003_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/bool/tutorial004_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer boolean flag names

By default a `bool` CLI option in Typer produces `--something` and `--no-something`. You can override those names by passing a string to `typer.Option()`.

## Only `--force`

Pass the exact single name to drop the `--no-force` form:

```python
@app.command()
def main(force: Annotated[bool, typer.Option("--force")] = False):
    if force:
        print("Forcing operation")
    else:
        print("Not forcing")
```

Help shows only `--force`. Passing `--no-force` fails with `Error: No such option: --no-force`.

## Alternative on/off names

Give one string with both names separated by `/`:

```python
@app.command()
def main(accept: Annotated[bool | None, typer.Option("--accept/--reject")] = None):
    if accept is None:
        print("I don't know what you want yet")
    elif accept:
        print("Accepting!")
    else:
        print("Rejecting!")
```

Help shows `--accept / --reject`. With neither flag the page's example prints `I don't know what you want yet`. Use this when `--no-accept` reads badly.

## Short names

Declare short versions on either side of the slash, e.g. `-f` for `--force` and `-F` for `--no-force`:

```python
def main(force: Annotated[bool, typer.Option("--force/--no-force", "-f/-F")] = False):
```

Help shows `-f, --force / -F, --no-force  [default: no-force]`.

## Names for False only

To declare only names that set `False`, start each string with a space and then `/`, then the negative name:

```python
def main(in_prod: Annotated[bool, typer.Option(" /--demo", " /-d")] = True):
    if in_prod:
        print("Running in production")
    else:
        print("Running demo")
```

The page's tip stresses this: it is a string with a preceding space and then a slash, so it is `" /-S"` and not `"/-S"`. The example help shows ` / -d, --demo  [default: True]`; running with no flag prints `Running in production`, and `--demo` prints `Running demo`. The page notes this might not be a good idea, so prefer the paired forms above.

## Gotchas

- The leading space in the false-only string is required.
- A paired name like `"--force/--no-force"` is one single `str` with a slash, not two arguments.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/parameter-types/bool.md with its four example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
