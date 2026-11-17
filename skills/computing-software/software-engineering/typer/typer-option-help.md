---
id: computing-software.software-engineering.typer.typer-option-help
name: typer-option-help
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, help-text, rich-help-panel, show-default]
level: practitioner
status: docs-checked
description: "Add help text to Typer CLI options with help=, group options into Rich help panels, and hide or customize the default shown in --help."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options/help.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options/help/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/help/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/help/tutorial003_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/help/tutorial004_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer CLI option help text, panels and shown defaults

## Add help text

Put `typer.Option()` inside `Annotated` and pass the `help` keyword:

```python
@app.command()
def main(
    name: str,
    lastname: Annotated[str, typer.Option(help="Last name of person to greet.")] = "",
    formal: Annotated[bool, typer.Option(help="Say hi formally.")] = False,
):
    """
    Say hi to 'name', optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        print(f"Good day Ms. {name} {lastname}.")
    else:
        print(f"Hello {name} {lastname}")
```

The older style (the option as the parameter default value) also works:

```python
lastname: str = typer.Option(default="", help="this option does this and that")
```

Check with `python main.py --help`; the page shows `--lastname <str>  Last name of person to greet.` and `--formal / --no-formal  Say hi formally.  [default: no-formal]`.

## Group options in help panels

With Rich installed, set `rich_help_panel` to a panel name on each option you want moved out of the default "Options" panel:

```python
formal: Annotated[
    bool,
    typer.Option(
        help="Say hi formally.", rich_help_panel="Customization and Utils"
    ),
] = False,
debug: Annotated[
    bool,
    typer.Option(
        help="Enable debugging.", rich_help_panel="Customization and Utils"
    ),
] = False,
```

Options without it stay in "Options"; the others appear in their own panel below.

## Hide the default

`show_default=False` removes the `[default: ...]` text from the option's help line:

```python
@app.command()
def main(fullname: Annotated[str, typer.Option(show_default=False)] = "Wade Wilson"):
    print(f"Hello {fullname}")
```

## Show a custom default string

Pass a string instead of a bool to `show_default`; that text is displayed instead of the real default:

```python
fullname: Annotated[
    str, typer.Option(show_default="Deadpoolio the amazing's name")
] = "Wade Wilson",
```

`--help` shows `--fullname <str>  [default: (Deadpoolio the amazing's name)]` while running with no args still prints `Hello Wade Wilson`.

## Gotchas

- Rich markup in help text is covered by the Commands - Command Help page (`commands/help.md`), not here.

Verify: with `show_default=False` the `--help` output has no `[default: Wade Wilson]`, and running the program with no args still prints "Hello Wade Wilson".

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/options/help.md with its four example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
