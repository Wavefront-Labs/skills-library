---
id: computing-software.software-engineering.typer.typer-uuid-parameter
name: typer-uuid-parameter
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, uuid, argument, validation, python]
level: intro
status: docs-checked
description: "Accept a UUID CLI argument or option in Typer and receive a standard Python UUID object with automatic validation of the input text."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/uuid.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/uuid/tutorial001_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer UUID parameters

A UUID ("Universally Unique Identifier") is a standard identifier format that is long and random enough to treat as unique across applications, databases and systems, such as `d48edaa6-871a-4082-a196-4daab372d4a1`. That makes UUIDs safer than plain `int` ids when mixing data from different systems.

## Declaring one

Annotate the parameter with `uuid.UUID`:

```python
from uuid import UUID

import typer

app = typer.Typer()


@app.command()
def main(user_id: UUID):
    print(f"User ID is {user_id}")
    print(f"UUID version is: {user_id.version}")


if __name__ == "__main__":
    app()
```

Your code receives a standard Python `UUID` object with all its attributes and methods, and because the parameter is annotated you get type checking and editor completion.

## Behaviour

- Valid input: `python main.py d48edaa6-871a-4082-a196-4daab372d4a1` prints `User ID is d48edaa6-871a-4082-a196-4daab372d4a1` and `UUID version is: 4`.
- Invalid input is rejected with an error. `python main.py 7479706572-72756c6573` prints `Error: Invalid value for 'user_id': 7479706572-72756c6573 is not a valid UUID.`

## Notes

- As written above (no default), the parameter is a required CLI argument and appears in usage as `{user_id}`.

## Checked

2026-11-07. Read in full against parameter-types/uuid.md and its docs_src example (Typer docs repository checkout). Confirmed: UUID annotation, valid and invalid outputs, usage line. Removed or trimmed: the claims that Typer rejects input "before your code runs" and that no validation code is needed.

Method: documentation only; no commands were run.
