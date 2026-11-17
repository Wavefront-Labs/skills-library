---
id: computing-software.software-engineering.typer.typer-launch-apps
name: typer-launch-apps
category: computing-software
field: software-engineering
product: typer
tags: [typer, launch, browser, file-browser, operating-system, cli]
level: intro
status: docs-checked
description: "Open a URL or file in the matching desktop application from a Typer CLI with typer.launch(), and reveal a file in the file browser with locate=True."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/launch.md
  - https://github.com/fastapi/typer/blob/master/docs_src/launch/tutorial001_py310.py
  - https://github.com/fastapi/typer/blob/master/docs_src/launch/tutorial002_py310.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Launching applications with typer.launch()

`typer.launch()` asks the operating system to open something with the appropriate application, chosen from the URL or file type you pass.

## Open a URL

```python
import typer

app = typer.Typer()


@app.command()
def main():
    print("Opening Typer's docs")
    typer.launch("https://typer.tiangolo.com")


if __name__ == "__main__":
    app()
```

Running it opens a browser with Typer's docs. The page says the application launched depends on the URL or file type you pass.

## Reveal a file: locate=True

To make the OS open its file browser indicating where a file lives, pass `locate=True`:

```python
from pathlib import Path

import typer

APP_NAME = "my-super-cli-app"

app = typer.Typer()


@app.command()
def main():
    app_dir = typer.get_app_dir(APP_NAME)
    app_dir_path = Path(app_dir)
    app_dir_path.mkdir(parents=True, exist_ok=True)
    config_path: Path = Path(app_dir) / "config.json"
    if not config_path.is_file():
        config_path.write_text('{"version": "1.0.0"}')
    config_file_str = str(config_path)
    print("Opening config directory")
    typer.launch(config_file_str, locate=True)


if __name__ == "__main__":
    app()
```

The page says the rest of the code just makes sure the app directory exists and creates the config file; the important part is `typer.launch(config_file_str, locate=True)`. It opens a file browser indicating where the config file is located. (See the typer-app-dir skill for `typer.get_app_dir()`.)

## Checked

2026-11-07: every claim was compared with the full text and included example files of docs/tutorial/launch.md with its two example files. Removed or trimmed: nothing; all claims matched.

Method: documentation only; no commands were run.
