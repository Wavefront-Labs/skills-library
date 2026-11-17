---
id: computing-software.software-engineering.typer.typer-app-dir
name: typer-app-dir
category: computing-software
field: software-engineering
product: typer
tags: [typer, app-dir, configuration, pathlib, config-file, cross-platform]
level: intro
status: docs-checked
description: "Find the per-user config directory for a CLI with typer.get_app_dir(), build the config file path with pathlib Path, and check whether it exists."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/app-dir.md
  - https://github.com/fastapi/typer/blob/master/docs_src/app_dir/tutorial001_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application directory with typer.get_app_dir()

`typer.get_app_dir()` returns the directory suited to storing configuration for your CLI program, for the current user, on each operating system. That avoids hard-coding paths per platform.

## Usage

```python
from pathlib import Path

import typer

APP_NAME = "my-super-cli-app"

app = typer.Typer()


@app.command()
def main():
    app_dir = typer.get_app_dir(APP_NAME)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        print("Config file doesn't exist yet")


if __name__ == "__main__":
    app()
```

You pass your application name; the first run, with no file yet, prints `Config file doesn't exist yet`.

## About Path

- `Path(app_dir) / "config.json"`: a `Path` supports `/` and converts it to the current system's separator (`/` on Unix, `\` on Windows).
- If the first element is a `Path`, the following elements may be plain `str`; the result is a new `Path`.
- Annotating `config_path: Path` explicitly helps the editor: otherwise it may infer a sub-type (`PurePath`) and stop completing some methods.

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/app-dir.md with its example. Removed or trimmed: the unsourced advice to pair with typer.launch and to create the directory before writing.

Method: documentation only; no commands were run.
