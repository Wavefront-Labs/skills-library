---
id: computing-software.software-engineering.typer.typer-command-help-and-rich
name: typer-command-help-and-rich
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, help, rich, markdown, deprecated, help-panels]
level: practitioner
status: docs-checked
description: "Document Typer commands: app help, docstrings, help= override, deprecated=True, suggest_commands, rich_markup_mode, rich_help_panel, and epilog."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/help.md
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/help/tutorial004_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/help/tutorial006_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/help/tutorial007_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/help/tutorial008_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer command help, Rich markup and panels

## Basic help

- App help: `typer.Typer(help="Awesome CLI user manager.")` shows under the usage line in `main.py --help`.
- Command help comes from the function docstring (shown inline in the Commands list and fully in `main.py create --help`). CLI options and arguments also take a `help` text.
- Override a docstring explicitly with `@app.command(help="Create a new user with username.")`. Docstrings are usually the better place; the override is for special cases.

```python
@app.command(help="Create a new user with username.")
def create(username: str):
    """
    Some internal utility function to create.
    """
```

## Deprecate a command

```python
@app.command(deprecated=True)
def delete(username: str):
```

`@app.command(deprecated=True)` marks it `(deprecated)` in both the main `--help` command list and in that command's own `--help`. It still works.

## Suggest commands

Since version 0.20.0 Typer suggests mistyped command names, enabled by default. Disable with `typer.Typer(suggest_commands=False)`. For `main.py crate` the error is `No such command 'crate'. Did you mean 'create'?`. Close matches come from `difflib.get_close_matches()`; several matches are all suggested.

```python
app = typer.Typer(suggest_commands=True)
```

## Rich markup and Markdown

Typer installs Rich. Set `rich_markup_mode` when creating the app:

- `"rich"` (the default): Rich console markup works in docstrings and in option/argument `help`, including bold/colour tags and emoji.

```python
app = typer.Typer(rich_markup_mode="rich")


@app.command()
def create(
    username: Annotated[
        str, typer.Argument(help="The username to be [green]created[/green]")
    ],
):
    """
    [bold green]Create[/bold green] a new [italic]shiny[/italic] user. :sparkles:

    This requires a [underline]username[/underline].
    """
```
- `"markdown"` (`typer.Typer(rich_markup_mode="markdown")`, e.g. `help="**Delete** a user with *username*."`): Markdown works in docstrings (bold, lists, emoji), but you cannot define colours; use Rich markup for colours.
- `None`: disables rich formatting for that app. Globally, set the environment variable `TYPER_USE_RICH` to `False` or `0`.

## Help panels

Pass `rich_help_panel="Utils and Configs"` to `@app.command()` to group commands into a named panel.

```python
@app.command(rich_help_panel="Utils and Configs")
def config(configuration: str):
    """
    [blue]Configure[/blue] the system. :gear:
    """
    print(f"Configuring the system with: {configuration}")
```

 Commands without one stay in the default `Commands` panel. Arguments and options accept `rich_help_panel` too: unpanelled ones go in `Arguments` and `Options`; custom ones (the page uses `Secondary Arguments` and `Additional Data`) are shown in the order Arguments, custom argument panels, Options, custom option panels. Requires Rich installed.

## Epilog

An `epilog` section can be added to the help of your commands; the page's example renders a footer line `Made with ❤ in Venus` after the options panel.

```python
@app.command(epilog="Made with :heart: in [blue]Venus[/blue]")
def create(username: str):
```

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/commands/help.md with its example files. Removed or trimmed: the claim that custom panels all appear after the defaults (the page orders Arguments, Secondary Arguments, Options, Additional Data).

Method: documentation only; no commands were run.
