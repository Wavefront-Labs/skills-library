---
id: computing-software.software-engineering.typer.typer-autocompletion-context-args
name: typer-autocompletion-context-args
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, autocompletion, context, stderr, multiple-values]
level: advanced
status: docs-checked
description: "In a Typer autocompletion function, use typer.Context to skip already-given values and list[str] for raw args, printing debug output to stderr only."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options-autocompletion.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options_autocompletion/tutorial007_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options_autocompletion/tutorial008_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options_autocompletion/tutorial009_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer autocompletion with Context and raw CLI args

An `autocompletion` function can declare up to three parameters; Typer picks them by type annotation, in any order and with any names:

- `str`: the incomplete value
- `typer.Context`: the current context
- `list[str]`: raw command-line parameters

## Skip values already used

For a repeatable option (used as `--name Camila --name Sebastian`), read earlier values from the context:

```python
valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_name(ctx: typer.Context, incomplete: str):
    names = ctx.params.get("name") or []
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete) and name not in names:
            yield (name, help_text)


@app.command()
def main(
    name: Annotated[
        list[str],
        typer.Option(help="The name to say hi to.", autocompletion=complete_name),
    ] = ["World"],
):
    for n in name:
        print(f"Hello {n}")
```

`ctx.params.get("name")` is keyed by the option's parameter name (`name` here); with none given yet it is `None`, hence `or []`.

## Raw args

Declare `args: list[str]` to receive everything before the incomplete value, e.g. `["typer", "main.py", "run", "--name"]`:

```python
def complete_name(ctx: typer.Context, args: list[str], incomplete: str):
    err_console.print(f"{args}")
    names = ctx.params.get("name") or []
    ...
```

(`err_console = Console(stderr=True)`, from `rich.console`.) The page calls this an advanced case; the Context is usually better. It contains options and values too, not only arguments.

## Do not print to stdout

Completion reads only standard output, so a normal print corrupts it. Debug to standard error: a Rich `Console(stderr=True)`, or `print(..., file=sys.stderr)` or `typer.echo("text", err=True)` if Rich is disabled.

Verify: after `--name Sebastian --name Ca[TAB][TAB]`, only Camila and Carlos are offered; if one name is left, the shell may complete it directly instead of listing.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/options-autocompletion.md with its nine example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
