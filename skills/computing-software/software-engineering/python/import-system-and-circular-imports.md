---
id: computing-software.software-engineering.python.import-system-and-circular-imports
name: import-system-and-circular-imports
category: computing-software
field: software-engineering
product: python
tags: [python, import-system, circular-imports, sys-path, relative-imports, python-m, namespace-packages]
level: practitioner
status: verified
description: "Understand how Python finds and runs modules: sys.path, packages and __init__, absolute vs relative imports, python -m, and breaking circular imports without hacks."
sources: ["https://docs.python.org/3/reference/import.html", "https://docs.python.org/3/tutorial/modules.html", "https://docs.python.org/3/library/sys_path_init.html", "https://peps.python.org/pep-0420/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The import system and circular imports

**Goal:** stop "ModuleNotFoundError", "attempted relative import with no known parent
package" and "partially initialized module" errors by knowing what import actually does.

## What `import pkg.mod` does
1. Check `sys.modules` (cache). If present, return it - even if half-initialised.
2. Find a spec via `sys.meta_path` finders searching `sys.path`.
3. Create the module, **insert it into `sys.modules`**, then execute its code top to bottom.
4. Bind the name in the importer's namespace.

`sys.path[0]` is the directory of the script being run (or cwd for `-m`/`-c`/REPL), then
`PYTHONPATH`, then the stdlib and site-packages.

## Running code inside a package
```
project/
  src/app/__init__.py
  src/app/cli.py        # from .core import run
  src/app/core.py
```
- `python src/app/cli.py` -> relative import error: run as a script, there is no parent package.
- `python -m app.cli` (with `src` installed via `pip install -e .`) -> works; `-m` sets the package.
- Never fix this with `sys.path.insert(0, ...)`; install the project (editable) instead.

## Absolute vs relative
Inside a package prefer absolute `from app.core import run` (greppable) or explicit relative
`from .core import run`. Implicit relative imports are gone since Python 3.

## Namespace packages
A directory without `__init__.py` on `sys.path` is a namespace package (PEP 420). Handy for
plugins split across distributions; a trap when a missing `__init__.py` makes tools (pytest,
mypy) resolve modules differently. Add `__init__.py` unless you need namespace behaviour.

## Circular imports
```
# orders.py                      # customers.py
from customers import Customer   from orders import Order   <- ImportError: cannot import name 'Order'
                                                               from partially initialized module 'orders'
```
`orders` is in `sys.modules` but has not yet defined `Order` when `customers` asks for it.
(That is the message when the module is imported from a library directory. On 3.14 a module in the
current directory or script directory instead gets "cannot import name 'Order' from 'orders'
(consider renaming '<path>' if it has the same name as a library you intended to import)".)

Fixes, best first:
1. **Restructure:** move the shared pieces into a third module both import, or merge the
   two modules. Cycles usually mean a muddled dependency direction.
2. **Import the module, not the name:** `import orders` and use `orders.Order` at call time;
   attribute lookup happens after both modules finished loading.
3. **Type-hint-only cycles:** 
```python
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from orders import Order
```
4. **Local import inside the function** that needs it - acceptable for rarely called paths,
   costs a dict lookup per call.

## Shadowing
A local `random.py`, `logging.py` or `test.py` shadows the stdlib module for every import.
Check with `python -c "import random; print(random.__file__)"`.

## Debugging
`python -X importtime -c "import app" 2>&1 | sort -t'|' -k2 -n | tail` (slow imports),
`python -v` (every import), `python -c "import sys; print(sys.path)"`.

## Verify
- [ ] Entry points run via `python -m` or console scripts, no `sys.path` hacks.
- [ ] `python -X importtime` shows no surprising heavy imports at startup.

## Checked
- Python 3.14.0 scratch packages: running `python src/app/cli.py` gave "attempted relative import with no known parent package", `python -m app.cli` from `src` worked; a circular `from` import reproduced (message variants described above) and `import orders` at call time fixed it; a directory without `__init__.py` imported as a namespace package; a local `random.py` shadowed the stdlib; `sys.path[0]` was the script dir for scripts and '' for `-c`; `-X importtime` prints the self/cumulative table. `python -v` and the editable-install advice were not run.
