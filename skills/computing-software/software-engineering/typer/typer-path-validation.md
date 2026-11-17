---
id: computing-software.software-engineering.typer.typer-path-validation
name: typer-path-validation
category: computing-software
field: software-engineering
product: typer
tags: [typer, cli, path, pathlib, validation, exists, resolve-path]
level: practitioner
status: docs-checked
description: "Declare pathlib.Path Typer parameters and validate them with exists, file_okay, dir_okay, writable, readable, resolve_path, allow_dash and path_type."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/parameter-types/path.md
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/path/tutorial001_an_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/parameter_types/path/tutorial002_an_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typer Path parameters and validation

Annotate a parameter as `pathlib.Path` for file or directory paths. You receive a standard `Path`, so editors complete its attributes and methods.

```python
@app.command()
def main(config: Annotated[Path | None, typer.Option()] = None):
    if config is None:
        print("No config file")
        raise typer.Abort()
    if config.is_file():
        text = config.read_text()
        print(f"Config file contents: {text}")
    elif config.is_dir():
        print("Config is a directory, will use all its config files")
    elif not config.exists():
        print("The config doesn't exist")
```

## Validations

Pass these as arguments to `typer.Option()` (as the page's example does) for a `Path` CLI parameter:

- `exists`: the file or directory must exist. If not required and the file does not exist, all further checks are silently skipped.
- `file_okay`: whether a file is a possible value.
- `dir_okay`: whether a directory is a possible value.
- `writable`: perform a writable check.
- `readable`: perform a readable check.
- `resolve_path`: fully resolve the path (absolute, symlinks resolved) before passing it on.

```python
@app.command()
def main(
    config: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
):
    text = config.read_text()
    print(f"Config file contents: {text}")
```

Verify: a missing file gives `Error: Invalid value for '--config': File 'config.txt' does not exist.`; passing `./` with directories disallowed gives `Error: Invalid value for '--config': File './' is a directory.`

## Gotcha

Typer does not expand a tilde prefix like `~/Documents/`; that is the shell's job.

## Advanced

- `allow_dash`: permit a single dash to mean standard streams.
- `path_type`: optional string type used to represent the path. Default `None` returns bytes or unicode depending on the input.

## Checked

2026-11-07. Read in full against parameter-types/path.md and docs_src path examples 1-2 (Typer docs repository checkout). Confirmed: exists, file_okay, dir_okay, writable, readable, resolve_path, allow_dash, path_type, tilde note, error messages. Removed or trimmed: the claim that the validations apply to typer.Argument.

Method: documentation only; no commands were run.
