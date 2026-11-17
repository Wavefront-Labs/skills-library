---
id: computing-software.software-engineering.python.debugging-with-pdb-and-breakpoint
name: debugging-with-pdb-and-breakpoint
category: computing-software
field: software-engineering
product: python
tags: [python, py-debugging, pdb-breakpoint, pdb, breakpoint, post-mortem, pythonbreakpoint, ipdb, remote-pdb]
level: practitioner
status: docs-checked
description: "Use pdb: breakpoint(), PYTHONBREAKPOINT, post-mortem, stepping and inspection commands, conditional breakpoints and 3.14 remote attach."
sources: ["https://docs.python.org/3/library/pdb.html", "https://docs.python.org/3/library/functions.html#breakpoint"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging with pdb and breakpoint()

## Getting in
```
breakpoint()                          # in code; since 3.7 equivalent to import pdb; pdb.set_trace() with defaults
python -m pdb [-c command] (-m module | -p pid | pyfile) [args ...]
import pdb; pdb.pm()                  # post-mortem after an exception in a REPL
pdb.run("f(2)")                       # run a statement under the debugger
```
- `python -m pdb pyfile` enters post-mortem automatically if the program exits abnormally, then restarts it, preserving breakpoints.
- `-c command` runs commands as if from a `.pdbrc` file; `-m module` pauses before the module's first line.
- `breakpoint()` behaviour can be changed with the `PYTHONBREAKPOINT` environment variable (see `sys.breakpointhook()`); this does not apply if `sys.breakpointhook()` has been replaced.
- Python 3.14: `python -m pdb -p <pid>` attaches to a running process. Attaching to a process blocked in a system call or I/O only works after the next bytecode instruction or a signal. `pdb.set_trace_async()` (3.14) is the async version of `set_trace()` for use with `await`.

## Commands
`s` step into, `n` next, `r` continue until the current function returns, `c` continue, `unt [lineno]` run to a later line, `l`/`ll` list source, `w` stack, `u`/`d` move frames, `p expr`/`pp expr` print, `! statement` execute a statement, `interact` start an interpreter with the current scope, `b [[filename:]lineno | function] [, condition]`, `tbreak` (temporary), `cl` clear, `condition bpnumber [condition]`, `display expr`, `commands [bpnumber]` attach commands to a breakpoint, `run [args]` restart, `q` quit.

## Techniques
- Conditional breakpoint without editing code: `b mod.py:120, user.id == 5`.
- `display` compares with the previous evaluation, so it may miss in-place changes to mutable values; display a copy such as `lst[:]`.
- `interact` assignments do not affect the original namespaces, but changes to mutable objects are visible.

## Gotchas
- In 3.13+, names assigned via pdb affect the active scope immediately, even in optimized scopes.
- A forgotten `breakpoint()` blocks waiting for input in a deployment with no terminal.

## Verify
- [ ] You can stop on a failing line, print the offending value with `p`, and `c` to resume.

## Checked
2026-11-09. Confirmed against the Python 3 `pdb` module docs (CLI usage, -c, -m, -p and its blocked-process note, post-mortem, run, set_trace_async, command list, conditions, display, interact) and the `breakpoint()` entry (PYTHONBREAKPOINT, sys.breakpointhook caveat). Removed: pytest `--pdb`/`--trace`, `PYTHONBREAKPOINT=0` and ipdb values, `pdb.attach(pid)`, `PYTHON_DISABLE_REMOTE_DEBUG`, PEP 768 claims, remote-pdb, ruff/flake8 `T100` rules, thread/asyncio debug-mode advice, and the "p on a command name" claim, none of which the cited pages state. The `sys.breakpointhook` page itself was not fetched.
Method: documentation only; no commands were run.
