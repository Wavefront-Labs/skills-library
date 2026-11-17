---
id: computing-software.software-engineering.typer.typer-option-autocompletion
name: typer-option-autocompletion
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, autocompletion, shell-completion, yield]
level: practitioner
status: docs-checked
description: "Provide shell completion for Typer option values with an autocompletion function: filter by incomplete text, add help tuples, or yield items."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options-autocompletion.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options_autocompletion/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options_autocompletion/tutorial003_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options_autocompletion/tutorial004_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options_autocompletion/tutorial005_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom value completion for Typer options

Typer completes option names, arguments and subcommands out of the box. To complete **values**, give the option an `autocompletion=` function (like a `callback`).

## Try it quickly

Use the `typer` command without packaging: `typer ./main.py run --name [TAB][TAB]`.

## Basic function

Return a list of strings:

```python
def complete_name():
    return ["Camila", "Carlos", "Sebastian"]


app = typer.Typer()


@app.command()
def main(
    name: Annotated[
        str, typer.Option(help="The name to say hi to.", autocompletion=complete_name)
    ] = "World",
):
    print(f"Hello {name}")
```

## Filter by the incomplete value

Declare a parameter typed `str`; it receives what the user has typed so far, so return only matches:

```python
valid_names = ["Camila", "Carlos", "Sebastian"]


def complete_name(incomplete: str):
    completion = []
    for name in valid_names:
        if name.startswith(incomplete):
            completion.append(name)
    return completion
```

`Ca[TAB]` then offers Camila and Carlos. The incomplete value is always a `str` even if the option is an `int`, and you can only return `str`.

## Help text per item

Return a list of 2-item `tuple`s of `str`: (completion, help). It must be a `tuple`, not a `list`. Zsh, Fish and PowerShell show the help; Bash does not, but completion still works.

```python
valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_name(incomplete: str):
    completion = []
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            completion_item = (name, help_text)
            completion.append(completion_item)
    return completion
```

## Use yield

The function may be a generator; any iterable works, each element a `str` or a help `tuple`:

```python
def complete_name(incomplete: str):
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            yield (name, help_text)
```

Parameter types drive injection (`str`, `typer.Context`, `list[str]`); for the last two see typer-autocompletion-context-args.

Verify: `typer ./main.py run --name Ca[TAB][TAB]` shows only Camila and Carlos, not Sebastian.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/options-autocompletion.md with its nine example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
