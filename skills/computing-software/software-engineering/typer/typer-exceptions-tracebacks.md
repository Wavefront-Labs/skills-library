---
id: computing-software.software-engineering.typer.typer-exceptions-tracebacks
name: typer-exceptions-tracebacks
category: computing-software
field: software-engineering
product: typer
tags: [typer, exceptions, traceback, rich, debugging, environment-variables]
level: practitioner
status: docs-checked
description: "Control Typer error output: Rich short tracebacks, pretty_exceptions_show_locals, pretty_exceptions_short, pretty_exceptions_enable, TYPER_USE_RICH, TYPER_STANDARD_TRACEBACK."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/exceptions.md
  - https://github.com/fastapi/typer/blob/master/docs_src/exceptions/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/exceptions/tutorial002_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/exceptions/tutorial003_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/exceptions/tutorial004_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions and tracebacks in Typer

When your command code raises, Typer shapes how the error is shown. The page's broken app:

```python
import typer

app = typer.Typer()


@app.command()
def main(name: str = "morty"):
    print(name + 3)


if __name__ == "__main__":
    app()
```

`name + 3` gives `TypeError: can only concatenate str (not "int") to str`.

## Default: Rich, short

Typer uses Rich to print the error nicely and **omits** traceback frames from Typer's internals, so you see mostly your own code and the exception. This is the clearest view.

## Without Rich

Disable Rich globally with the environment variable `TYPER_USE_RICH`. Typer still prints a simplified traceback (your frames plus the exception) as clearly as possible.

## Parameters on typer.Typer()

Each example differs only in the line creating the app:

```python
app = typer.Typer(pretty_exceptions_show_locals=True)
app = typer.Typer(pretty_exceptions_short=False)
app = typer.Typer(pretty_exceptions_enable=False)
```

- `pretty_exceptions_show_locals=True` (Rich only): print local variable values with the error. **Disabled by default since Typer 0.23.0** to avoid leaking passwords, keys or tokens, especially in CI logs. Enable only when no sensitive data is involved; it is very helpful for debugging.
- `pretty_exceptions_short=False`: show the full traceback including Typer internals.
- `pretty_exceptions_enable=False`: turn off pretty exceptions entirely; you get the standard Python traceback as in any other program.

## Standard traceback via environment variable

`TYPER_STANDARD_TRACEBACK=1` gives the same plain Python traceback without code changes (the older `_TYPER_STANDARD_TRACEBACK=1` is deprecated). It works for any Typer program, useful when debugging an app someone else wrote:

```console
$ export TYPER_STANDARD_TRACEBACK=1
$ uv run python main.py
```

## Quick decision

- Need variable values: `pretty_exceptions_show_locals=True` (locally, not where logs are recorded).
- Need to see Typer's own frames: `pretty_exceptions_short=False`.
- Need ordinary Python behaviour: `pretty_exceptions_enable=False` or `TYPER_STANDARD_TRACEBACK=1`.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/exceptions.md with its four example files. Removed or trimmed: the unsourced mention of tooling and other debuggers.

Method: documentation only; no commands were run.
