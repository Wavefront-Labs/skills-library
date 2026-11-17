---
id: computing-software.software-engineering.typer.typer-custom-command-name
name: typer-custom-command-name
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, commands, naming, decorator, python]
level: intro
status: docs-checked
description: "Set a Typer command name explicitly with @app.command(\"create\") when the function name clashes, and know the underscore-to-dash default."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/commands/name.md
  - https://github.com/fastapi/typer/blob/master/docs_src/commands/name/tutorial001_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom command name in Typer

By default a Typer command is named after its function: `def create(username: str): ...` becomes the command `create`.

## When to override

If a function called `create()` already exists elsewhere in your code, you must name the CLI function differently, yet you may still want the command to be `create`. Pass the name as the first parameter of the decorator:

```python
@app.command("create")
def cli_create_user(username: str):
    print(f"Creating user: {username}")


@app.command("delete")
def cli_delete_user(username: str):
    print(f"Deleting user: {username}")
```

Even though the functions are `cli_create_user()` and `cli_delete_user()`, `python main.py --help` lists the commands `create` and `delete`, and `python main.py create Camila` prints `Creating user: Camila`.

## Default naming rule

Underscores in a function name are replaced with dashes. So `def create_user(username: str): ...` yields the command `create-user`.

## Tips

- Use the explicit name when a function with the command's name already exists in your code, as in the example above.
- Check the resulting names with `python main.py --help`.

Verify: with the renamed functions above, the Commands section of `--help` shows `create` and `delete`, not the function names.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/commands/name.md with its example file. Removed or trimmed: the tip about unique function names in one module and the claim about how sub-app group names are set (neither is on the page).

Method: documentation only; no commands were run.
