---
id: computing-software.web-development.fastapi.debugging-uvicorn-run
name: debugging-uvicorn-run
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, debugging, uvicorn, breakpoints, vscode, pycharm, name-main]
level: intro
status: docs-checked
description: "Debug a FastAPI app in VS Code or PyCharm by calling uvicorn.run under the __name__ == __main__ guard so the debugger can stop at breakpoints."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/debugging.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging

## Method
- In the app file, `import uvicorn` and call `uvicorn.run(app, host="0.0.0.0", port=8000)` inside `if __name__ == "__main__":`.
- The guard runs that code when the file is run directly (e.g. `uv run python myapp.py`, where `__name__` is `"__main__"`) and not when another file does `from myapp import app`.
- Because Uvicorn runs from your code, the editor debugger can launch the program and stop at breakpoints.

## VS Code
Debug panel, "Add configuration...", select Python, run `Python: Current File (Integrated Terminal)`.

## PyCharm
Run menu, "Debug...", choose the file (e.g. `main.py`).

## Verify
A breakpoint in a path operation function is hit when you call the route.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
