---
id: computing-software.software-engineering.typer.typer-parameters-reference
name: typer-parameters-reference
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, argument, option, annotated, parameters]
level: intro
status: docs-checked
description: "Declare Typer CLI arguments and options with Annotated[..., typer.Argument()] and typer.Option(), and know where their full parameter lists live."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/reference/parameters.md
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options/required.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer parameters: Argument and Option

Parameters of a Typer command line interface are either CLI Options or CLI Arguments. Both are declared with `typing.Annotated` metadata, using `typer.Argument()` or `typer.Option()`.

```python
from typing import Annotated
import typer

app = typer.Typer()


@app.command()
def register(
    user: Annotated[str, typer.Argument()],
    age: Annotated[int, typer.Option(min=18)],
    score: Annotated[float, typer.Option(max=100)] = 0,
):
    print(f"User is {user}")
    print(f"--age is {age}")
    print(f"--score is {score}")


if __name__ == "__main__":
    app()
```

## Reading the example

- `user` is a CLI argument, declared with `typer.Argument()`.
- `age` is a CLI option declared with `min=18`. It is required because `typer.Option()` sits in `Annotated` and the parameter has no default (the options/required tutorial page).
- `score` is a CLI option declared with `max=100` and a default of `0`.

## Where to look next

The reference page is generated from the `typer.Argument` and `typer.Option` docstrings (shown there without overloads), so it holds the complete list of accepted parameters. The page links to the tutorial sections for CLI Options and CLI Arguments.

Thin skill: the source page is one example plus those generated listings; look parameter names up there, not here.

## Checked

2026-11-07. Read in full against reference/parameters.md and options/required.md (Typer docs repository checkout). Confirmed: the register example and that the reference lists Argument and Option parameters without overloads. Removed or trimmed: the "pick Argument or Option" tip and the claims about what Typer() and command() do. Thin skill: one example page.

Method: documentation only; no commands were run.
