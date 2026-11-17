---
id: computing-software.software-engineering.textual.textual-devtools-console
name: textual-devtools-console
category: computing-software
field: software-engineering
product: textual
tags: [textual, devtools, console, serve, log, dev, live-editing, textual-dev]
level: practitioner
status: docs-checked
description: "Debug Textual apps with the textual command: run, run --dev, console with -v, -x and --port, serve in a browser, the log function and TextualHandler."
sources: [https://textual.textualize.io/guide/devtools/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual devtools and console

Goal: run, serve and debug Textual apps. The `textual` command comes with the `textual-dev` package.

## Method

- Run an app file: `textual run my_app.py` (like `python my_app.py` but with debug switches). Run from an import path: `textual run music.play` (expects an app named `app`) or `textual run music.play:MusicPlayerApp` (instances or classes). Run an installed script with `-c`: `textual run -c textual colors`.
- Dev mode: `textual run --dev my_app.py` enables the console and live editing of CSS; CSS edits show a few milliseconds after saving.
- Console: open two terminals. In one run `textual console`; in the other `textual run --dev my_app.py`. `print` output and Textual log messages appear in the console window (stdout in the app would corrupt the display).
  - `textual console -v` includes verbose events.
  - `-x GROUP` excludes a group: EVENT, DEBUG, INFO, WARNING, ERROR, PRINT, SYSTEM, LOGGING, WORKER. Repeat it, e.g. `textual console -x SYSTEM -x EVENT -x DEBUG -x INFO` to leave only warnings, errors and print.
  - Custom port: `textual console --port 7342` and `textual run --dev --port 7342 my_app.py`.
- Serve in a browser: `textual serve my_app.py`, or a command: `textual serve "textual keys"`. For a module use the full command, `textual serve "python -m textual"`. Multiple instances can be served; refresh the browser to pick up code changes. See `textual serve --help`.
- Log function: `from textual import log`; `log("Hello, World")`, `log(locals())`, `log(children=self.children, pi=3.141592)`, `log(self.tree)` (Rich renderables). Apps and widgets also have `self.log(...)`.
- Standard logging: `logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])` with `from textual.logging import TextualHandler` sends library logs to the console. It handles strings only, not Rich renderables.

## Gotchas

- If the `textual` command is missing, install `textual-dev`.
- The group name is printed after each timestamp in the console.

## Verify

Run `textual console` in one terminal and `textual run --dev my_app.py` in another; anything the app prints appears in the console window.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/devtools. Nothing needed removing.

Method: documentation only; no commands were run.
