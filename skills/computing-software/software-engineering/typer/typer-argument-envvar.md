---
id: computing-software.software-engineering.typer.typer-argument-envvar
name: typer-argument-envvar
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, argument, envvar, environment-variables]
level: practitioner
status: docs-checked
description: "Let a Typer CLI argument fall back to environment variables via envvar=, with several variables, precedence rules and show_envvar=False."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/arguments/envvar.md
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/envvar/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/envvar/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/arguments/envvar/tutorial003_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer arguments read from environment variables

Use the `envvar` parameter of `typer.Argument()` so a value can come from the environment when not given on the command line.

```python
@app.command()
def main(name: Annotated[str, typer.Argument(envvar="AWESOME_NAME")] = "World"):
    print(f"Hello Mr. {name}")
```

`--help` shows `name  [env var: AWESOME_NAME; default: World]`.

## Precedence

1. A CLI argument wins: `AWESOME_NAME=Wednesday python main.py Czernobog` greets Czernobog.
2. Otherwise the env var: `AWESOME_NAME=Wednesday python main.py` greets Wednesday.
3. Otherwise the default ("World").

PowerShell: set the variable first (`$Env:AWESOME_NAME = "Wednesday"`) and then run the command.

## Several environment variables

Pass a list:

```python
name: Annotated[str, typer.Argument(envvar=["AWESOME_NAME", "GOD_NAME"])] = "World"
```

Help shows `[env var: AWESOME_NAME, GOD_NAME; default: World]`. Either variable works (`GOD_NAME=Anubis python main.py` greets Anubis).

## Hide from help

Env vars are listed in help by default. Add `show_envvar=False` to hide them; the variable is still read:

```python
name: Annotated[
    str, typer.Argument(envvar="AWESOME_NAME", show_envvar=False)
] = "World"
```

Help then shows only `name  [default: World]`, yet `AWESOME_NAME=Wednesday python main.py` still prints "Hello Mr. Wednesday".

Verify: with the env var set and an explicit argument, the explicit argument is used.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/arguments/envvar.md with its three examples. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
