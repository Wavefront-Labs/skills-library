---
id: computing-software.software-engineering.typer.typer-command-runner
name: typer-command-runner
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, completion, markdown-docs, scripts, python-m-typer]
level: advanced
status: docs-checked
description: "Use the typer command to run scripts or modules with TAB completion, pick the app with --app or --func, and generate Markdown docs with typer utils docs."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/typer-command.md
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/help/tutorial001_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The typer command: run scripts with completion, generate docs

The `typer` command gives TAB completion for your own small scripts (even ones that do not use Typer internally) and can generate Markdown docs for Typer apps. It suits scripts not worth packaging.

## Setup

```console
$ uv add typer
$ source .venv/bin/activate        # Linux, macOS
$ .venv\Scripts\Activate.ps1       # Windows PowerShell
$ source .venv/Scripts/activate    # Windows Bash
$ typer --install-completion
```

Using `typer` from the project environment keeps the same Typer version as the project. Without activating, use `uv run python -m typer ...`.

## Run a script

```console
$ typer my_custom_script.py run hello --name Camila
```

Replace `python` with `typer`, and add the subcommand `run` after the file name. With completion installed, TAB completes subcommands and options. Plain `python my_custom_script.py hello` works but gives no completion (and is best when other programs call your script).

Because `typer` ignores the `if __name__ == "__main__": app()` block, you may delete it if you only use `typer`.

## Any file, or a module

- A file with only `def main(name: str = "World")` and no Typer import still works: `typer main.py run --name Camila`; the docstring becomes help text.
- Pass a module path instead of a file: `typer my_package.main run --name Camila`.

## Choosing the app

CLI options: `--app` (variable holding a `Typer()` object) and `--func` (variable holding a function, as with `typer.run()`). Default priority:

1. App from `--app`.
2. Function from `--func`.
3. A Typer app named `app`, `cli` or `main`.
4. First Typer app in the file.
5. A function named `main`, `cli` or `app`.
6. First function in the file.

## Generate Markdown docs

```console
$ typer my_package.main utils docs --name awesome-cli --output README.md
```

Options: `--name <str>` (program name in docs), `--output <file>` (file to write, e.g. README.md), `--title <str>` (default: the command name). Output is Markdown with a section per command listing Usage, Options and Commands. Also works as `uv run python -m typer some_script.py utils docs`.

Verify: after running with `--output README.md`, it prints `Docs saved to: README.md`.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/typer-command.md. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
