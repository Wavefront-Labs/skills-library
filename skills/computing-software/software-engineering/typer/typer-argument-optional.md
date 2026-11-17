---
id: computing-software.software-engineering.typer.typer-argument-optional
name: typer-argument-optional
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, argument, optional-argument, annotated]
level: intro
status: docs-checked
description: "Make a Typer CLI argument optional with typer.Argument() inside Annotated plus a default, and read the older typer.Argument(default=...) style."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/arguments/optional.md
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/optional/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/optional/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/optional/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/optional/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/optional/tutorial003_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optional Typer CLI arguments

By default options are optional and arguments are required, but optional arguments are very common (like `ls` with or without a directory).

## Explicit argument declaration

Wrapping the type in `Annotated` with `typer.Argument()` is still a required argument when there is no default:

```python
def main(name: Annotated[str, typer.Argument()]):
    print(f"Hello {name}")
```

It behaves exactly like `name: str`; missing it gives `Error: Missing argument 'name'.` `Annotated` support needs Typer 0.9.0 or newer (older versions error).

## Make it optional

Add a default:

```python
@app.command()
def main(name: Annotated[str, typer.Argument()] = "World"):
    print(f"Hello {name}!")
```

Typer still treats `name` as an argument (not an option) because of `typer.Argument()`. `--help` shows `name  [default: World]`; usage shows `[name]` in square brackets for optional (curly brackets `{name}` for required). `python main.py` greets World; `python main.py Camila` greets Camila.

## Older style

`typer.Argument()` as the parameter default value is also supported, but prefer `Annotated`. Then the first parameter of `typer.Argument` is `default`:

```python
name: str = typer.Argument()               # required
name: str = typer.Argument(default=...)    # required, explicit Ellipsis
name: str = typer.Argument(default="World")  # optional
```

No value for `default` means required; `...` is the Ellipsis constant meaning required. The value is often passed positionally: `typer.Argument(...)` or `typer.Argument("World")`.

Verify: `python main.py` with a required argument prints "Error: Missing argument 'name'."; with default "World" the page shows a greeting using World.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/arguments/optional.md with its example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
