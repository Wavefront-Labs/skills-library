---
id: computing-software.software-engineering.typer.typer-option-prompt
name: typer-option-prompt
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, prompt, interactive, confirmation-prompt]
level: intro
status: docs-checked
description: "Make a Typer CLI option ask the user interactively when missing with prompt=True, a custom prompt string, or confirmation_prompt=True for typing twice."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options/prompt.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options/prompt/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/prompt/tutorial002_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/prompt/tutorial003_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prompting for a Typer CLI option

Instead of erroring on a missing option, ask for it in the terminal.

## Basic prompt

```python
@app.command()
def main(name: str, lastname: Annotated[str, typer.Option(prompt=True)]):
    print(f"Hello {name} {lastname}")
```

Run `python main.py Camila` and the program asks `Lastname:`, then continues, e.g. printing `Hello Camila Gutiérrez`.

## Custom prompt text

Pass a string instead of `True`:

```python
@app.command()
def main(
    name: str,
    lastname: Annotated[str, typer.Option(prompt="Please tell me your last name")],
):
    print(f"Hello {name} {lastname}")
```

The terminal shows `Please tell me your last name:`.

## Confirmation prompt

`confirmation_prompt=True` makes the user type the value twice, the page's example is a CLI app that deletes a project:

```python
@app.command()
def main(
    project_name: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True)],
):
    print(f"Deleting project {project_name}")
```

The prompts are `Project name:` then `Repeat for confirmation:`. If the two entries differ, Typer prints `Error: The two entered values do not match` and prompts again.

## Notes

- For a hidden-input password variant see the typer-option-password-prompt skill.

Verify: entering "Old Project" then "New Spice" gives "Error: The two entered values do not match" and a fresh prompt; matching entries proceed.

## Checked

2026-11-07. Read in full against options/prompt.md and docs_src prompt examples 1-3 (Typer docs repository checkout). Confirmed: prompt=True, custom prompt string, confirmation_prompt=True and the mismatch error text. Removed or trimmed: the "destructive actions" generalisation.

Method: documentation only; no commands were run.
