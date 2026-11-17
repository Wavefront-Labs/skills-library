---
id: computing-software.software-engineering.typer.typer-printing-rich
name: typer-printing-rich
category: computing-software
field: software-engineering
product: typer
tags: [typer, rich, printing, colors, stderr, echo]
level: practitioner
status: docs-checked
description: "Print from a Typer app with Rich print, markup and tables, write to stderr via Console(stderr=True), and know when typer.echo, style and secho still apply."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/printing.md
  - https://github.com/fastapi/typer/blob/master/docs_src/printing/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/printing/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/printing/tutorial004_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/printing/tutorial005_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/printing/tutorial006_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Printing and colors in Typer

Plain `print()` works. For richer output use **Rich**, which is installed by default with `typer`. Typer structures the app (options, arguments, subcommands, validation); Rich displays things. Combine both.

## Rich print and markup

```python
from rich import print

print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")
```

Importing `print` from `rich` pretty-prints dicts and lists with colors and structure. Markup supports styles, colors and emojis (see Rich's markup docs).

## Rich tables with a Console

Rich's `print` creates a `Console` for you. For advanced cases make one yourself:

```python
from rich.console import Console
from rich.table import Table

console = Console()


@app.command()
def main():
    table = Table("Name", "Item")
    table.add_row("Rick", "Portal Gun")
    table.add_row("Morty", "Plumbus")
    console.print(table)
```

## Standard output and standard error

The OS treats printed text as writing to a virtual file called standard output; errors normally go to standard error. Print to stderr with `Console(stderr=True)`:

```python
err_console = Console(stderr=True)


@app.command()
def main():
    err_console.print("Here is something written to standard error")
```

Both show in the terminal. In PowerShell, stderr output may not appear (check `$Error`); Bash, Zsh and Fish are fine.

Standard input is the third virtual file (what you type); it matters later for completion and testing.

## typer.echo, typer.style, typer.secho

Mostly unnecessary; prefer Rich.

- `typer.echo()` converts binary data to strings and similar checks.
- It preserves terminal control sequences (including colors). For untrusted text, escape control characters first; `typer.echo(repr(value))` is a diagnostic form. `color=False` disables styling but does not sanitize all control sequences.
- `typer.style(text, fg=..., bg=..., bold=..., dim=..., underline=..., blink=..., reverse=..., reset=...)` returns a colored `str` to pass to `typer.echo()`. `dim` is badly supported; `reset=False` lets styles compose.
- Colors are strings (`fg="green"`) or `typer.colors.GREEN` for autocompletion.
- `typer.secho()` = echo plus style in one call.

```python
@app.command()
def main(good: bool = True):
    message_start = "everything is "
    if good:
        ending = typer.style("good", fg=typer.colors.GREEN, bold=True)
    else:
        ending = typer.style("bad", fg=typer.colors.WHITE, bg=typer.colors.RED)
    message = message_start + ending
    typer.echo(message)
```

```python
@app.command()
def main(name: str):
    typer.secho(f"Welcome here {name}", fg=typer.colors.MAGENTA)
```

## Checked

2026-11-07. Read in full against printing.md and docs_src printing examples 2-6 (Typer docs repository checkout). Confirmed: Rich print, markup, Table with Console, Console(stderr=True), PowerShell note, echo/style/secho parameters. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
