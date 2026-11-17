---
id: computing-software.software-engineering.typer.typer-nested-subcommands
name: typer-nested-subcommands
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, nested-subcommands, add-typer, command-groups, python]
level: practitioner
status: docs-checked
description: "Build a deep command tree in Typer by adding a lands app (reigns, towns) into main with add_typer, so commands like lands reigns conquer work."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/subcommands/nested-subcommands.md
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/tutorial003_py310/reigns.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/tutorial003_py310/towns.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/tutorial003_py310/lands.py
  - https://github.com/fastapi/typer/blob/master/docs_src/subcommands/tutorial003_py310/main.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested subcommands in Typer

Extend the `add_typer` idea to many levels. The example adds `lands`, where a land is a `reign` or a `town`, each with its own commands.

## Build bottom-up

1. `reigns.py`: a Typer app with commands `conquer` and `destroy`. `python reigns.py conquer Cintra` prints `Conquering reign: Cintra`.
2. `towns.py`: a Typer app with commands `found` and `burn`. `python towns.py found "New Asgard"` prints `Founding town: New Asgard`.
3. `lands.py`: a Typer app that includes both with `add_typer`, named `reigns` and `towns`.
4. `main.py`: add the `lands` app next to `users` and `items`.

`reigns.py` (`towns.py` has the same shape with `found` and `burn`):

```python
import typer

app = typer.Typer()


@app.command()
def conquer(name: str):
    print(f"Conquering reign: {name}")


@app.command()
def destroy(name: str):
    print(f"Destroying reign: {name}")


if __name__ == "__main__":
    app()
```

`lands.py`:

```python
import typer

import reigns
import towns

app = typer.Typer()
app.add_typer(reigns.app, name="reigns")
app.add_typer(towns.app, name="towns")

if __name__ == "__main__":
    app()
```

`main.py`:

```python
import typer

import items
import lands
import users

app = typer.Typer()
app.add_typer(users.app, name="users")
app.add_typer(items.app, name="items")
app.add_typer(lands.app, name="lands")

if __name__ == "__main__":
    app()
```

## Resulting tree

- `users`: `create`, `delete`
- `items`: `create`, `delete`, `sell`
- `lands`: `reigns` (`conquer`, `destroy`) and `towns` (`found`, `burn`)

Examples from the page:

- `python main.py lands reigns conquer Gondor` prints `Conquering reign: Gondor`.
- `python main.py lands towns found Cartagena` prints `Founding town: Cartagena`.
- `python lands.py --help` lists `reigns` and `towns`; `python lands.py reigns --help` lists `conquer` and `destroy`.

## Tips

- Every file can carry an `if __name__ == "__main__"` block to run standalone; for the final app only `main.py` needs it.
- Deeply nested programs benefit from shell auto completion; the page points to the completion docs.
- A simpler design is often easier to use; nest only when requirements demand it.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/subcommands/nested-subcommands.md with its example files. Removed or trimmed: the claim that python main.py lands --help was shown (the page shows lands.py --help).

Method: documentation only; no commands were run.
