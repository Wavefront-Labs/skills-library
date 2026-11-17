---
id: computing-software.web-development.webassembly.pyodide-python-in-browser
name: pyodide-python-in-browser
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, pyodide, micropip, pyodide-js-bridge, blazor-wasm, wasm-ui, wasm]
level: practitioner
status: docs-checked
description: "Python in the browser"
sources: ["https://pyodide.org/en/stable/usage/quickstart.html", "https://pyodide.org/en/stable/usage/loading-packages.html", "https://pyodide.org/en/stable/usage/type-conversions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pyodide

Goal: run Python client-side.
- `loadPyodide()`, `pyodide.runPython()`, `pyodide.loadPackage('numpy')`, `micropip.install()` for pure-Python wheels.
- JS bridge converts types with `toJs()`.
Verify: NumPy calculation runs in the page.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: `loadPyodide()`, `runPython`, `loadPackage("numpy")`, `micropip.install`, `toJs()`.
Removed or reworded as unconfirmed: the 'initial download is large' sentence.
Method: documentation only; no commands were run.
