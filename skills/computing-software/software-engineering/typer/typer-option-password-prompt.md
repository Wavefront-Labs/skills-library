---
id: computing-software.software-engineering.typer.typer-option-password-prompt
name: typer-option-password-prompt
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, python, password, confirmation-prompt, hide-input]
level: intro
status: docs-checked
description: "Ask for a Typer option value twice with confirmation_prompt=True and hide typed characters with hide_input=True for password-style CLI input."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/options/password.md
  - https://github.com/fastapi/typer/blob/master/docs_src/options/password/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/options/password/tutorial002_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer password option with confirmation prompt

Two keyword parameters of `typer.Option()` give you a password-style prompt.

## Confirmation prompt

`confirmation_prompt=True` (used together with a prompt) asks the user to type the value a second time:

```python
@app.command()
def main(
    name: str,
    email: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True)],
):
    print(f"Hello {name}, your email is {email}")
```

`python main.py Camila` prompts `Email:` then `Repeat for confirmation:`; entering `camila@example.com` both times prints `Hello Camila, your email is camila@example.com`.

## Hide what is typed

`hide_input=True` makes the terminal show nothing while typing, not even `****`, like most shells do for passwords. The program still receives the value.

Combine both for a password with double confirmation:

```python
@app.command()
def main(
    name: str,
    password: Annotated[
        str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)
    ],
):
    print(f"Hello {name}. Doing something very secure with password.")
    print(f"...just kidding, here it is, very insecure: {password}")
```

Running it prompts `Password:` then `Repeat for confirmation:` with no echo.

## Gotchas

- The page's demo prints the password back to show it was received; do not do that in real code.
- Use `prompt=True` (see the typer-option-prompt skill) so the option is asked for when missing.

Verify: in the page's example, typing "typerrocks" twice (invisible) leads to the program printing the received value, i.e. both entries were accepted.

## Checked

2026-11-07. Read in full against options/password.md and docs_src password examples 1-2 (Typer docs repository checkout). Confirmed: confirmation_prompt=True, hide_input=True, the prompts and outputs. Removed or trimmed: the claim that the body runs only after confirmation.

Method: documentation only; no commands were run.
