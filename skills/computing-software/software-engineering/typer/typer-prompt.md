---
id: computing-software.software-engineering.typer.typer-prompt
name: typer-prompt
category: computing-software
field: software-engineering
product: typer
tags: [typer, prompt, confirm, interactive, abort, rich]
level: intro
status: docs-checked
description: "Ask for input in a Typer app with typer.prompt() and typer.confirm(abort=True), prefer prompting CLI options for scripts, and optionally prompt with Rich."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/prompt.md
  - https://github.com/fastapi/typer/blob/master/docs_src/prompt/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/prompt/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/prompt/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/prompt/tutorial004_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interactive prompts in Typer

## Prefer CLI options with prompt

When you need user input interactively, normally use a *CLI option* with a prompt. That keeps the program usable non-interactively (for example from a Bash script). Use the functions below only if you absolutely need to ask without a CLI option.

## typer.prompt()

```python
@app.command()
def main():
    person_name = typer.prompt("What's your name?")
    print(f"Hello {person_name}")
```

Running it shows `What's your name?:` and waits; typing `Camila` prints `Hello Camila`.

## typer.confirm()

```python
@app.command()
def main():
    delete = typer.confirm("Are you sure you want to delete it?")
    if not delete:
        print("Not deleting")
        raise typer.Abort()
    print("Deleting it!")
```

The prompt appears as `Are you sure you want to delete it? [y/N]:`. Answering `y` continues; answering `n` prints `Not deleting` then `Aborted!` (via `typer.Abort()`).

## Confirm or abort in one step

Aborting when the user declines is so common that `typer.confirm()` has an `abort` parameter:

```python
@app.command()
def main():
    delete = typer.confirm("Are you sure you want to delete it?", abort=True)
    print("Deleting it!")
```

Answering `n` prints `Aborted!` and the code after it never runs.

## Prompt with Rich

Rich has its own prompt:

```python
from rich.prompt import Prompt

@app.command()
def main():
    name = Prompt.ask("Enter your name :sunglasses:")
    print(f"Hey there {name}!")
```

It supports emoji in the prompt text (the page shows the prompt as `Enter your name 😎:`).

## Checked

2026-11-07. Read in full against prompt.md and docs_src prompt examples 1-4 (Typer docs repository checkout). Confirmed: typer.prompt, typer.confirm, abort=True, Rich Prompt.ask and the outputs. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
