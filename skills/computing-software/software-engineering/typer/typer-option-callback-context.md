---
id: computing-software.software-engineering.typer.typer-option-callback-context
name: typer-option-callback-context
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, callback, context, resilient-parsing, completion]
level: advanced
status: docs-checked
description: "Validate Typer parameters with callback=, raise typer.BadParameter, and guard against breaking shell completion using ctx.resilient_parsing and CallbackParam."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options/callback-and-context.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options/callback/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/callback/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/callback/tutorial003_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/callback/tutorial004_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer parameter callbacks, Context and completion safety

## Validate with a callback

Pass a function via `callback=` to `typer.Option()` or `typer.Argument()`. It receives the command-line value, may do anything, and must return the value:

```python
def name_callback(value: str):
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value


@app.command()
def main(name: Annotated[str | None, typer.Option(callback=name_callback)] = None):
    print(f"Hello {name}")
```

`typer.BadParameter` is special: the error names the parameter, e.g. `Error: Invalid value for '--name': Only Camila is allowed`.

## Callbacks break completion if they print

Shell completion works by the shell calling your program with special environment variables and reading what it prints. Callbacks also run during completion, so adding `print("Validating name")` as the first line of `name_callback` corrupts the completion output (the page shows a broken `(eval):1: command not found: Validating` error).

## Fix with the Context

Declare a parameter typed `typer.Context`; when `ctx.resilient_parsing` is `True` (completion is happening) return early without printing:

```python
def name_callback(ctx: typer.Context, value: str):
    if ctx.resilient_parsing:
        return
    print("Validating name")
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value
```

## CallbackParam

Declare a parameter typed `typer.CallbackParam` to get the specific parameter object (useful when one callback serves several parameters):

```python
def name_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if ctx.resilient_parsing:
        return
    print(f"Validating param: {param.name}")
    if value != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return value
```

`python main.py --name Camila` prints `Validating param: name` then `Hello Camila`.

## Signature flexibility

Typer decides what to pass by type annotation: `typer.Context` and `typer.CallbackParam` can be in any order with any names, either or both may be omitted. The value parameter can have any name and should have the same type annotation as the main function's parameter (annotation optional; the value parameter itself may even be omitted).

Verify: after adding the `resilient_parsing` guard, `typer ./main.py run --[TAB][TAB]` lists `--help` and `--name`, and a normal run prints "Validating name" then "Hello Camila".

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/options/callback-and-context.md with its four example files. Removed or trimmed: the unsourced claim that printing to standard error is safe during completion (it is on the autocompletion page, not this one) and the unstated 'on standard output' detail.

Method: documentation only; no commands were run.
