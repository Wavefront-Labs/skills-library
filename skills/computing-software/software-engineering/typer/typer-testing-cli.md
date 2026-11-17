---
id: computing-software.software-engineering.typer.typer-testing-cli
name: typer-testing-cli
category: computing-software
field: software-engineering
product: typer
tags: [typer, testing, pytest, clirunner, stdin, cli]
level: advanced
status: docs-checked
description: "Test Typer apps with pytest and CliRunner: invoke with an argument list, assert exit_code and stdout, feed prompts via input=, and test a bare function."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/testing.md
  - https://github.com/fastapi/typer/blob/master/docs_src/testing/app01_py310/main.py
  - https://github.com/fastapi/typer/blob/master/docs_src/testing/app01_py310/test_main.py
  - https://github.com/fastapi/typer/blob/master/docs_src/testing/app02_an_py310/main.py
  - https://github.com/fastapi/typer/blob/master/docs_src/testing/app02_py310/test_main.py
  - https://github.com/fastapi/typer/blob/master/docs_src/testing/app03_py310/main.py
  - https://github.com/fastapi/typer/blob/master/docs_src/testing/app03_py310/test_main.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Typer applications with pytest

Layout: `app/main.py` (the CLI), an empty `app/__init__.py` (making `app` a package) and `app/test_main.py`. File and function names must start with `test_` so pytest discovers them.

## Basic test

The app under test (`app/main.py`):

```python
@app.command()
def main(name: str, city: str | None = None):
    print(f"Hello {name}")
    if city:
        print(f"Let's have a coffee in {city}")
```

The test (`app/test_main.py`):

```python
from typer.testing import CliRunner

from .main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["Camila", "--city", "Berlin"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
    assert "Let's have a coffee in Berlin" in result.output
```

- `runner.invoke(app, args)`: first parameter is the `Typer` app, second a `list` of `str` with exactly what you would type on the command line.
- Exit code `0` means the program ended without errors.
- The examples assert on `result.output`; `result.stdout` and `result.stderr` can be checked independently.

Run with `uv run pytest`; a passing run ends with `1 passed`.

## Testing prompts (standard input)

What the user types goes to "standard input". Use `input=` with a trailing newline, which stands for pressing ENTER:

App with a prompted option:

```python
@app.command()
def main(name: str, email: Annotated[str, typer.Option(prompt=True)]):
    print(f"Hello {name}, your email is: {email}")
```

Test:

```python
def test_app():
    result = runner.invoke(app, ["Camila"], input="camila@example.com\n")
    assert result.exit_code == 0
    assert "Hello Camila, your email is: camila@example.com" in result.output
```

## Testing a function without an explicit app

If `main.py` only defines a function run via `typer.run(main)`, create the app inside the test:

```python
def main(name: str = "World"):
    print(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
```

Test:

```python
import typer
from typer.testing import CliRunner

from .main import main

app = typer.Typer()
app.command()(main)

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
```

Then `runner.invoke(app, [...])` as usual. Why it works: `@app.command()` is a decorator that registers the function and returns it unmodified, so `app.command()(main)` is the same as decorating without the `@` syntax. It is usually cleaner to create the explicit app in `main.py`.

## Checked

2026-11-07. Read in full against testing.md and docs_src testing app01-app03 (Typer docs repository checkout). Confirmed: CliRunner invoke, exit_code, output, input= with newline, testing a bare function, decorator explanation. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
