---
id: computing-software.software-engineering.textual.textual-install-and-first-app
name: textual-install-and-first-app
category: computing-software
field: software-engineering
product: textual
tags: [textual, install, getting-started, pip, textual-dev, demo, python, tui]
level: intro
status: docs-checked
description: "Install Textual and its developer tools, run the built-in demo, try the repository examples, and write the smallest runnable App subclass."
sources: [https://textual.textualize.io/getting_started/, https://textual.textualize.io/guide/app/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Textual and run a first app

Goal: get Textual installed with the developer tools, see what it can do, and run a minimal app.

## Method

Requirements: Python 3.9 or later (the most recent if you have a choice). Linux, macOS and Windows are supported. On macOS the default terminal is limited to 256 colors, so a newer terminal (iterm2, Ghostty, Kitty, WezTerm) is recommended; on Windows the new Windows Terminal is recommended.

1. Install from PyPI:
   ```
   pip install textual
   ```
2. For developing apps also install the developer tools (this provides the `textual` command):
   ```
   pip install textual-dev
   ```
3. For syntax highlighting in the TextArea widget, install the extra:
   ```
   pip install "textual[syntax]"
   ```
4. conda-forge alternative (micromamba preferred): `micromamba install -c conda-forge textual` and `micromamba install -c conda-forge textual-dev`.
5. List the CLI sub-commands:
   ```bash
   textual --help
   ```
6. Run the demo:
   ```bash
   python -m textual
   ```
7. Try the repository examples: clone `https://github.com/Textualize/textual.git`, then
   ```bash
   cd textual/examples/
   python code_browser.py ../
   ```
   Code listings used in the docs live in `docs/examples`.

## Minimal app

```python
from textual.app import App


class MyApp(App):
    pass


if __name__ == "__main__":
    app = MyApp()
    app.run()
```

Run it with `python simple02.py` (any filename). `run()` puts the terminal into application mode; you see a blank screen. Press ctrl+q to exit and return to the prompt, with earlier terminal content restored. Keep the run call inside the `__name__ == "__main__"` block so the module can be imported without starting the app, and so the devtools `run` command can run it.

## Gotchas

- If the `textual` command is not on your path, you probably forgot to install `textual-dev`.

## Verify

`python -m textual` opens the demo; the minimal app above shows a blank screen until you press ctrl+q.

## Checked

2026-11-07: every claim was read against the full text of these pages: getting_started, guide/app. Nothing needed removing.

Method: documentation only; no commands were run.
