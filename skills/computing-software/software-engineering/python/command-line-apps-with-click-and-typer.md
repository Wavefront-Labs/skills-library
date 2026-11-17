---
id: computing-software.software-engineering.python.command-line-apps-with-click-and-typer
name: command-line-apps-with-click-and-typer
category: computing-software
field: software-engineering
product: python
tags: [python, py-cli-config, py-cc-click, click-typer-cli, click, typer, cli, subcommands, clirunner]
level: practitioner
status: docs-checked
description: "Build command-line tools with click and typer: groups and subcommands, options and arguments, type validation, context objects, testing with CliRunner and packaging entry points."
sources: ["https://click.palletsprojects.com/en/stable/", "https://click.palletsprojects.com/en/stable/complex/", "https://click.palletsprojects.com/en/stable/exceptions/", "https://click.palletsprojects.com/en/stable/testing/", "https://typer.tiangolo.com/tutorial/testing/", "https://packaging.python.org/en/latest/specifications/pyproject-toml/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CLIs with click and typer

## click
```python
import click

@click.group()
@click.option("--verbose", "-v", is_flag=True, help="More output.")
@click.pass_context
def cli(ctx, verbose):
    ctx.obj = {"verbose": verbose}

@cli.command()
@click.argument("src", type=click.Path(exists=True, dir_okay=False))
@click.option("--count", "-n", default=1, show_default=True, type=click.IntRange(1, 100))
@click.option("--mode", type=click.Choice(["fast", "safe"]), default="safe")
@click.pass_context
def run(ctx, src, count, mode):
    """Process SRC."""
    if ctx.obj["verbose"]:
        click.echo(f"processing {src}", err=True)
    raise click.ClickException("failed")      # shown on stderr, exits with ClickException.exit_code

if __name__ == "__main__":
    cli()
```
- A callback receives the context only if marked with `click.pass_context`; the object stored on `ctx.obj` is shared with subcommands (`click.pass_obj` passes just that object).
- Options can read the environment via `envvar=`, and `required=True` makes them mandatory.
- Helpers: `click.echo`, `click.prompt`, `click.progressbar`, `click.File`, `click.get_app_dir`.
- Click exits with code 0 for `--help` requested by the user and 2 when help is shown because of incorrect input; a `ClickException` exits with its `exit_code`.

## typer (built on click, type hints)
```python
import typer
from typing import Annotated

app = typer.Typer(no_args_is_help=True)

@app.command()
def run(name: str, email: Annotated[str, typer.Option(prompt=True)]):
    print(f"{name} <{email}>")

if __name__ == "__main__":
    app()
```
The typer docs prefer the `Annotated` form (a required option is `Annotated[str, typer.Option()]` with no default). A typer app gets `--install-completion` and `--show-completion` options; completion needs a packaged, installed command, not a bare script.

## Testing and packaging
```python
from click.testing import CliRunner
result = CliRunner().invoke(cli, ["run", "f.txt", "-n", "3"])
assert result.exit_code == 0
print(result.output)
```
Typer ships its own `CliRunner` (see its testing tutorial). Expose a console script with a `[project.scripts]` table in `pyproject.toml`: the key is the command name and the value an object reference such as `"mypkg.cli:cli"`.

## Gotchas
- stdlib `argparse` needs no dependency; choose click/typer for nested commands and completion.
- Keep command bodies thin and call library functions that can be tested without the CLI.
- Print data to stdout and diagnostics to stderr (`err=True`) so pipes work.
- Secrets passed as `--option` values appear in process lists; prefer environment variables or files.

## Verify
- [ ] CliRunner tests for success, a bad option and a missing argument (exit code 2).
- [ ] The installed console script runs `--help`.

## Checked
Date: 2026-11-03. Confirmed against click docs (complex apps, options, arguments, exceptions and exit codes, testing, API) and typer docs (testing, required options, app and completion pages), plus the pyproject.toml specification for `[project.scripts]`. Removed as unconfirmed: `ctx.ensure_object`, typer `Argument(exists=)` and `Option(min=, max=)`, rich-error and version-default remarks, startup-time and lazy-import advice, `--token` example.
Method: documentation only; no commands were run.
