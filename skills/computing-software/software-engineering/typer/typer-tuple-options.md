---
id: computing-software.software-engineering.typer.typer-tuple-options
name: typer-tuple-options
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, options, tuple, multiple-values, python]
level: practitioner
status: docs-checked
description: "Declare a Typer option taking a fixed number of mixed-type values with tuple[str, int, bool] and unpack it in the function."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/multiple-values/options-with-multiple-values.md
  - https://github.com/fastapi/typer/blob/master/docs_src/multiple_values/options_with_multiple_values/tutorial001_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer options with several typed values

Use a `tuple` to make one CLI option take a fixed number of values, each with its own type. The number must be fixed, but can be anything you want.

```python
@app.command()
def main(user: Annotated[tuple[str, int, bool], typer.Option()] = (None, None, None)):
    username, coins, is_wizard = user
    if not username:
        print("No user provided")
        raise typer.Abort()
    print(f"The username {username} has {coins} coins")
    if is_wizard:
        print("And this user is a wizard!")
```

`tuple[str, int, bool]` means three values: first a `str`, second an `int`, third a `bool`. The unpacking `username, coins, is_wizard = user` is equivalent to indexing `user[0]`, `user[1]`, `user[2]`.

## Check it

Help shows the value types: `--user <str int boolean>...`.

- `--user Camila 50 yes` prints `The username Camila has 50 coins` and `And this user is a wizard!`.
- `--user Morty 3 no` prints only the coins line.
- Too few values: `--user Camila 50` gives `Error: Option '--user' requires 3 arguments`.

## Notes

- All values follow a single `--user` flag, unlike a `list` option which repeats the flag.

## Checked

2026-11-07. Read in full against multiple-values/options-with-multiple-values.md and its docs_src example (Typer docs repository checkout). Confirmed: tuple[str, int, bool], unpacking, help text, outputs and the too-few-values error. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
