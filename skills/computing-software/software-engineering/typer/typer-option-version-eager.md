---
id: computing-software.software-engineering.typer.typer-option-version-eager
name: typer-option-version-eager
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, version-option, is-eager, callback]
level: practitioner
status: docs-checked
description: "Implement a --version option in Typer with a callback that raises typer.Exit, and use is_eager=True so it runs before other parameters' callbacks."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options/version.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options/version/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/version/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/version/tutorial003_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A --version option in Typer, and is_eager

## Basic version callback

Use an option callback: when it receives `True`, print the version and raise `typer.Exit()` so nothing else runs.

```python
__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        print(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()


@app.command()
def main(
    name: Annotated[str, typer.Option()] = "World",
    version: Annotated[
        bool | None, typer.Option("--version", callback=version_callback)
    ] = None,
):
    print(f"Hello {name}")
```

Declare the explicit name `"--version"` so Typer does not generate an awkward `--no-version`. `--help` then lists `--version` and no automatic `--no-version`.

No `ctx.resilient_parsing` check is needed here because the callback prints only when `--version` is passed (see typer-option-callback-context for the completion issue).

## The ordering problem

If `--name` is declared before `--version` and has a callback that can exit, using `--version` after `--name` processes the name callback first:

```python
def name_callback(name: str):
    if name != "Camila":
        raise typer.BadParameter("Only Camila is allowed")
    return name


@app.command()
def main(
    name: Annotated[str, typer.Option(callback=name_callback)],
    version: Annotated[
        bool | None, typer.Option("--version", callback=version_callback)
    ] = None,
):
    print(f"Hello {name}")
```

`python main.py --name Rick --version` prints `Only Camila is allowed` and `Aborted!` instead of the version.

`typer.BadParameter` writes to standard error, so it does not break shell completion.

## Fix: is_eager

Mark the parameter `is_eager=True` (works for options and arguments) so Typer processes it before the others:

```python
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
```

Now `python main.py --name Rick --version` only prints the version.

Verify: with `is_eager=True`, `--name Rick --version` outputs "Awesome CLI Version: 0.1.0" and nothing about the name.

## Checked

2026-11-07. Read in full against options/version.md and docs_src version examples 1-3 (Typer docs repository checkout). Confirmed: callback with typer.Exit, explicit --version name, BadParameter ordering problem, is_eager=True fix. Removed or trimmed: the claim that help lists only --version.

Method: documentation only; no commands were run.
