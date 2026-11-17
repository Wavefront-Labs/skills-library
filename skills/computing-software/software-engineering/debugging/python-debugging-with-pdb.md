---
id: computing-software.software-engineering.debugging.python-debugging-with-pdb
name: python-debugging-with-pdb
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, python, pdb-debugger, breakpoint-function, post-mortem-debugging, debugpy]
level: practitioner
status: verified
description: "Debug Python with breakpoint() and pdb: core commands, post-mortem debugging, conditional breakpoints, debugging tests with pytest --pdb, and remote attach with debugpy."
sources: ["https://docs.python.org/3/library/pdb.html", "https://peps.python.org/pep-0553/", "https://docs.pytest.org/en/stable/how-to/failures.html", "https://github.com/microsoft/debugpy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Python debugging with pdb and breakpoint()

## Entering the debugger
- `breakpoint()` in code (PEP 553, 3.7+). Controlled by `PYTHONBREAKPOINT`: `=0` disables all,
  `=ipdb.set_trace` or `=pudb.set_trace` swaps debuggers, `=debugpy.breakpoint` for IDE attach.
- `python -m pdb script.py args` starts at the first line; `c` to run until an exception, which drops
  into post-mortem automatically (run: "Uncaught exception. Entering post mortem debugging", then `!n = 7` and `p n` work in the failing frame).
- Post-mortem after a crash in a REPL/notebook: `import pdb; pdb.pm()` or `%debug` in IPython/Jupyter.
- Tests: `pytest --pdb` (debugger on failure), `pytest --trace` (break at start of each test),
  `pytest -x --pdb -p no:randomly`.

## Commands
| Cmd | Does |
|---|---|
| `l` / `ll` | list around line / whole function |
| `n` / `s` / `r` | next (step over) / step into / return from function |
| `c` / `unt N` | continue / until line N |
| `b file.py:42, cond` | breakpoint with condition (`b 42, order.total < 0`); a condition that raises (for example a name not yet assigned on that line) also stops there |
| `tbreak`, `cl N`, `disable N` | temporary breakpoint, clear, disable |
| `w` / `u` / `d` | where (stack) / up / down frames |
| `p expr` / `pp expr` | print / pretty-print |
| `a` | function arguments |
| `display expr` | show expr whenever it changes (3.2+) |
| `interact` | full Python REPL in the current frame |
| `!stmt` | run a statement that clashes with a command name (`!n = 5`) |
| `q` | quit |
Python 3.14 adds `python -m pdb -p PID` to attach to a running process.

## Tips
- Variables named like commands (`n`, `c`, `l`) need `p n` or `!n`.
- `.pdbrc` in home or project dir for aliases (`alias pl pp locals()`).
- Debugging multiprocessing or forked workers: pdb on a child needs a TTY; use
  `remote-pdb`/`debugpy` listening on a port instead.
- Remote/containers: `python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py`, then attach
  from VS Code (launch config `"request": "attach"`, `pathMappings` to map container paths). Never
  expose the port publicly.
- Async code: pdb works inside coroutines, but a plain `breakpoint()` there gives `SyntaxError: 'await' outside function` for `await ...` at the prompt (run on 3.14.0). Stop with `await pdb.set_trace_async()` (3.14+) instead and `x = await work()` then `p x` works. For task-level
  problems use asyncio debug mode (`PYTHONASYNCIODEBUG=1`) and logging around tasks.
