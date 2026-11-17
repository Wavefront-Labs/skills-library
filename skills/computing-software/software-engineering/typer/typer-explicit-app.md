---
id: computing-software.software-engineering.typer.typer-explicit-app
name: typer-explicit-app
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, app-command, decorator, completion, python]
level: practitioner
status: docs-checked
description: "Replace typer.run() with an explicit typer.Typer() app and @app.command(), and why that is the first step toward shell completion and an installable package."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/typer-app.md
  - https://github.com/fastapi/typer/blob/master/docs_src/typer_app/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/first_steps/tutorial002_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer explicit application

`typer.run(main)` is a shortcut. Under the hood Typer does three things: it creates a `typer.Typer()` application, registers your function as a "command", and calls the application as a function with `app()`.

## The explicit form

```python
import typer

app = typer.Typer()


@app.command()
def main(name: str):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
```

`@app.command()` is a decorator: it tells Typer the function below is a command. The behaviour is the same as with `typer.run()`:

- No argument: usage line plus `Error: Missing argument 'name'.`
- `python main.py Camila` prints `Hello Camila`.
- `--help` lists the `name` argument as `[required]`.

## When to use which

If `typer.run()` solves your case, keep it; you do not have to create `app` and use `@app.command()`. Move to the explicit app when you need extra features (more commands are covered in the commands section of the docs).

## Completion options appear

With the explicit app, `--help` now shows two extra options:

- `--install-completion`: install completion for the current shell.
- `--show-completion`: show completion for the current shell, to copy it or customize the installation.

Shell/tab completion needs a package that you and your users can install and call directly (for example `magic-app` instead of `python main.py`). Using an explicit `typer.Typer()` app is the first step toward building that installable package; packaging itself is a later part of the tutorial.

## Checklist

1. Create `app = typer.Typer()`.
2. Decorate each command function with `@app.command()`.
3. Call `app()` under `if __name__ == "__main__":`.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/typer-app.md with its two example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
