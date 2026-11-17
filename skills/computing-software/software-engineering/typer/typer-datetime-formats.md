---
id: computing-software.software-engineering.typer.typer-datetime-formats
name: typer-datetime-formats
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, datetime, formats, strptime, python]
level: intro
status: docs-checked
description: "Declare datetime CLI parameters in Typer, know the three default accepted formats, and add custom strptime formats with the formats parameter."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/datetime.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/datetime/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/datetime/tutorial002_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer datetime parameters

Annotate a CLI argument or option as Python `datetime` and your function receives a standard `datetime` object.

```python
from datetime import datetime

import typer

app = typer.Typer()


@app.command()
def main(birth: datetime):
    print(f"Interesting day to be born: {birth}")
    print(f"Birth hour: {birth.hour}")


if __name__ == "__main__":
    app()
```

## Default accepted formats

Typer accepts a string in any of:

- `%Y-%m-%d`
- `%Y-%m-%dT%H:%M:%S`
- `%Y-%m-%d %H:%M:%S`

The help text lists them: `{birth}:<%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S>`.

Verify: `python main.py 1956-01-31T10:00:00` prints `Interesting day to be born: 1956-01-31 10:00:00` and `Birth hour: 10`. An unmatched value such as `july-19-1989` gives `Error: Invalid value for 'birth': 'july-19-1989' does not match the formats ...`.

## Custom formats

Use the `formats` parameter of `typer.Argument()` or `typer.Option()`. It takes a list of strings, each passed to `datetime.strptime()`:

```python
@app.command()
def main(
    launch_date: Annotated[
        datetime,
        typer.Argument(
            formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y"]
        ),
    ],
):
    print(f"Launch will be at: {launch_date}")
```

The example accepts ISO dates plus a month/day/year form separated with `/`. Verify: both `1969-10-29` and `10/29/1969` print `Launch will be at: 1969-10-29 00:00:00`.

## Gotchas

- The page's example lists the three ISO formats explicitly alongside `"%m/%d/%Y"`.
- Date-only input yields midnight (`00:00:00`).

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/parameter-types/datetime.md with its two example files. Removed or trimmed: the advice that custom formats replace the defaults (the page does not say so).

Method: documentation only; no commands were run.
