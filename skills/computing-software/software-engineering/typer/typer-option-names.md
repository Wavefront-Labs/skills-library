---
id: computing-software.software-engineering.typer.typer-option-names
name: typer-option-names
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, option-names, short-options, flags]
level: intro
status: docs-checked
description: "Rename Typer CLI options and add short names like -n by passing positional strings to typer.Option(); covers long-plus-short pairs and combined flags."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options/name.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options/name/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/name/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/name/tutorial003_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/name/tutorial004_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/name/tutorial005_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customizing Typer CLI option names and short names

## Default name

A parameter `user_name` becomes the option `--user-name` automatically.

## Rename it

Pass the wanted name as a **positional** string to `typer.Option()` (no keyword):

```python
@app.command()
def main(user_name: Annotated[str, typer.Option("--name")]):
    print(f"Hello {user_name}")
```

Now the option is `--name`, not `--user-name`. Keyword arguments such as `show_default=True`, `prompt=True` or `help="..."` still need their keyword.

## Add a short name

Pass several positional names:

```python
def main(user_name: Annotated[str, typer.Option("--name", "-n")]):
```

`--help` then shows `-n, --name <str>`.

## Only a short name

If you declare only `"-n"`, that is the only name: neither `--name` nor `--user-name` exists (help shows `-n <str>  [required]`):

```python
def main(user_name: Annotated[str, typer.Option("-n")]):
```

To get the default long name plus a short one you must list both explicitly (help shows `-n, --user-name <str>`):

```python
def main(user_name: Annotated[str, typer.Option("--user-name", "-n")]):
```

## Combining short flags

Single-letter short names can be combined behind one dash, for example `-fn` with options `-n/--name` and `-f/--formal`. An option that takes a value must come last in the group so the value that follows goes to it: `-fn Camila` works. (The page compares to `tar -xvf file` vs the broken `tar -fxv file`.) Boolean flags can go in any order.

Declare both long and short versions for every option you want combinable; nothing else is needed:

```python
@app.command()
def main(
    name: Annotated[str, typer.Option("--name", "-n")],
    formal: Annotated[bool, typer.Option("--formal", "-f")] = False,
):
    if formal:
        print(f"Good day Ms. {name}.")
    else:
        print(f"Hello {name}")
```

Verify: `python main.py -fn Camila` prints "Good day Ms. Camila." in the page's example, and `--help` lists `-n, --name <str>` and `-f, --formal`.

## Checked

2026-11-07. Read in full against options/name.md and its five docs_src name examples (Typer docs repository checkout). Confirmed: long and short names, short-only names, combined short flags with the value-taking option last, the help output lines. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
