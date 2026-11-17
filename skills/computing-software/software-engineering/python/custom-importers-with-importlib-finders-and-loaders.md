---
id: computing-software.software-engineering.python.custom-importers-with-importlib-finders-and-loaders
name: custom-importers-with-importlib-finders-and-loaders
category: computing-software
field: software-engineering
product: python
tags: [python, py-import-system, importlib-finders-loaders, meta-path, find-spec, module-spec, import-hooks]
level: advanced
status: docs-checked
description: "Hook the import system with sys.meta_path finders, ModuleSpec and loaders: blocking imports, virtual modules, create_module and exec_module, and reload caveats."
sources: ["https://docs.python.org/3/reference/import.html", "https://docs.python.org/3/library/importlib.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom importers: finders and loaders

Import = **find** a `ModuleSpec` (finders on `sys.meta_path`; the path-based finder consults `sys.path_hooks` per path entry) then **load** it (loader `create_module` + `exec_module`).

## Rules from the reference
- If the module is not in `sys.modules`, `sys.meta_path` finders are queried in order. A meta path finder implements `find_spec(fullname, path, target=None)`: it returns a spec if it can handle the module, else `None`. If the list is exhausted, `ModuleNotFoundError` is raised; any other exception propagates and aborts the import.
- The default `sys.meta_path` has three finders: built-in, frozen and the path-based finder. `find_module()` was removed in 3.12; use `find_spec()`.
- To selectively prevent an import from an early hook, raise `ModuleNotFoundError` directly from `find_spec()`; returning `None` means keep searching, raising terminates. To replace the whole import system, delete the default contents of `sys.meta_path` and install a custom hook.
- A loader's `exec_module(module)` executes the module; its return value is ignored. It should raise `ImportError` if it cannot execute the module. `create_module(spec)` returns the new module or `None` to let the machinery create it; it must be defined when `exec_module()` is (an `ImportError` since 3.6).
- Finder and loader may be the same object (`find_spec` returns a spec with the loader set to `self`). `importlib.util.spec_from_loader()` helps build specs.
- If a module is already in `sys.modules`, the loader must reuse it, or `importlib.reload()` will not work.
- If loading fails, only the failing module is removed from `sys.modules`.
- Loaders supporting resource reading should implement `get_resource_reader()` (3.7).

## A meta path finder that blocks imports
```python
import sys, importlib.abc

class Block(importlib.abc.MetaPathFinder):
    def __init__(self, names): self.names = set(names)
    def find_spec(self, fullname, path, target=None):
        if fullname.split(".")[0] in self.names:
            raise ModuleNotFoundError(f"{fullname} is banned in this environment")
        return None                       # None = "not mine", continue with the next finder

sys.meta_path.insert(0, Block({"requests"}))
```

## Virtual module from a loader
```python
import importlib.abc, importlib.util

class Virtual(importlib.abc.Loader):
    def create_module(self, spec): return None          # default module creation
    def exec_module(self, module): module.ANSWER = 42

class Finder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "virt":
            return importlib.util.spec_from_loader(fullname, Virtual())
sys.meta_path.append(Finder())
```

## Reload and cache notes
- `importlib.reload()` reruns the module code in the same module object; instances made earlier keep the old class definitions, and `from x import y` names in other modules are not redefined.
- Call `importlib.invalidate_caches()` if modules are created or installed while the program runs, so finders notice them.
- `reload()` is not thread-safe.

## Gotchas
- Order matters: a finder earlier in `sys.meta_path` is asked first, and meta hooks can override `sys.path` processing, frozen and built-in modules.
- `sys.meta_path` is global; restore it after tests (`try/finally`).

## Verify
- [ ] A test blocks `import requests` and asserts the optional-dependency fallback path runs.

## Checked
Date: 2026-11-03. Confirmed against the import system reference and the `importlib` documentation (meta path finders, `find_spec`, loaders, `create_module`/`exec_module`, blocking via `ModuleNotFoundError`, `reload`, `invalidate_caches`). Fixed: the blocking example raised `ImportError`; the reference says to raise `ModuleNotFoundError`. Removed as unconfirmed: the `LazyLoader` recipe, PEP 810 lazy import statement claim, `-X importtime` and `-v` diagnostics, `tuna`/sort advice, `pkgutil` and zipimport remarks, performance advice.
Method: documentation only; no commands were run.
