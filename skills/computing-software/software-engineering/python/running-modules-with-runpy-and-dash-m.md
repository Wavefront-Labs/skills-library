---
id: computing-software.software-engineering.python.running-modules-with-runpy-and-dash-m
name: running-modules-with-runpy-and-dash-m
category: computing-software
field: software-engineering
product: python
tags: [python, py-runtime-entry, runpy-main-module, python-m, main-py, if-name-main, run-module, run-path]
level: practitioner
status: docs-checked
description: "Make packages runnable with __main__.py and python -m, use runpy.run_module and run_path in tools, and know the sys.path and thread-safety caveats."
sources: ["https://docs.python.org/3/library/runpy.html", "https://docs.python.org/3/using/cmdline.html#cmdoption-m"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running modules with runpy and python -m

## `python -m package`
```
mypkg/
  __init__.py
  __main__.py        # executed by: python -m mypkg
  cli.py
```
```python
# mypkg/__main__.py
from .cli import main
raise SystemExit(main())
```
`-m` locates the module with the standard import mechanism and runs it as `__main__`; given a package (including a namespace package) it executes `<pkg>.__main__`. Give a module name without `.py`. `sys.argv[0]` becomes the full path to the module file, and the current directory is added to the start of `sys.path`. `-m` cannot run built-in or C extension modules. `-I` runs in isolated mode (no current directory or user site on `sys.path`).

## `if __name__ == "__main__":`
Keeps import side-effect free: code under the guard runs only when the module is executed as `__main__`, as `python -m pkg.module` does.

## runpy for tooling
```python
import runpy
ns = runpy.run_module("mypkg.tool", run_name="__main__", alter_sys=True)   # executes the module, returns its globals dict
ns = runpy.run_path("scripts/job.py", init_globals={"DEBUG": True})         # run a file, or a sys.path entry (directory or zip) with __main__
```
`run_module` takes an absolute module name; if it names a package, that package's `__main__` submodule is executed. `init_globals` pre-populates the module globals (the dict is not modified). `run_path` accepts a Python source file, a compiled bytecode file, or a valid `sys.path` entry containing a `__main__` module (for example a zipfile with a top-level `__main__.py`).

## Gotchas
- Because `-m` puts the current directory at the start of `sys.path`, a local file named like a standard-library module can shadow it; `-P` (3.11+) stops the cwd being prepended for `-m`, and `-I` implies it.
- With `alter_sys=True`, `sys.argv[0]` and `sys.modules[__name__]` are temporarily replaced; the docs say this manipulation of `sys` is not thread-safe, so avoid it in threaded code (`run_path` has the same limitation).
- Exit codes: `raise SystemExit(main())` makes the return value the exit status.

## Verify
- [ ] `python -m mypkg --help` works as expected.
- [ ] A test using `runpy.run_module` captures `SystemExit` and checks the code.

## Checked

- 2026-11-03: checked against the CPython docs `library/runpy.rst` (`run_module`, `run_path`, `init_globals`, `alter_sys`, thread-safety note) and `using/cmdline.rst` (`-m`, `-I`, `-P`).
- Removed: the relative-import error message, `[project.scripts]`, `__package__` claim, pytest `--pyargs`, cProfile and zipapp uses, the list of stdlib `-m` tools, the double-import gotcha and the missing-`__main__` error text (not in these pages).

Method: documentation only; no commands were run.
