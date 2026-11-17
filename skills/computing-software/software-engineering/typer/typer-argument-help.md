---
id: computing-software.software-engineering.typer.typer-argument-help
name: typer-argument-help
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, argument, help-text, metavar, rich-help-panel]
level: practitioner
status: docs-checked
description: "Document Typer CLI arguments in --help: help=, show_default, custom default text, metavar, rich_help_panel, and hiding an argument from the Arguments section."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/arguments/help.md
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/help/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/help/tutorial005_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/help/tutorial006_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/help/tutorial007_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/help/tutorial008_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Help text for Typer CLI arguments

## help parameter

```python
name: Annotated[str, typer.Argument(help="The name of the user to greet")]
```

`--help` shows it in the Arguments section: `name  The name of the user to greet  [required]`. It combines with the function docstring, which appears above the Arguments section.

## Defaults in help

An argument with a default (say `"World"`) shows `[default: World]`.

- `show_default=False` removes that text.
- `show_default="Deadpoolio the amazing's name"` (a string) displays that text instead of the real default; help shows `[default: (Deadpoolio the amazing's name)]`.

```python
name: Annotated[
    str,
    typer.Argument(
        help="Who to greet", show_default="Deadpoolio the amazing's name"
    ),
] = "Wade Wilson",
```

## Custom name: metavar

By default the help shows the declared parameter name with its casing. `metavar` overrides it:

```python
def main(name: Annotated[str, typer.Argument(metavar="✨username✨")] = "World"):
    print(f"Hello {name}")
```

Usage and Arguments then show `✨username✨` instead of `name`.

## Help panels

With Rich installed, set `rich_help_panel="Secondary Arguments"` (any name) on arguments to move them from the default "Arguments" panel into their own panel.

```python
def main(
    name: Annotated[str, typer.Argument(help="Who to greet")],
    lastname: Annotated[
        str, typer.Argument(help="The last name", rich_help_panel="Secondary Arguments")
    ] = "",
    age: Annotated[
        str,
        typer.Argument(help="The user's age", rich_help_panel="Secondary Arguments"),
    ] = "",
):
```

## Hide an argument

`hidden=True` (`name: Annotated[str, typer.Argument(hidden=True)] = "World"`) removes the argument from the Arguments section of the help. The page notes it still appears in the `Usage:` line, e.g. `Usage: main.py [OPTIONS] [name]`.

Rich markup in help text is covered in Commands - Command Help (`commands/help.md`).

Verify: with `hidden=True`, `--help` has no "Arguments" section but the usage line still lists `[name]`.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/arguments/help.md with its eight examples. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
