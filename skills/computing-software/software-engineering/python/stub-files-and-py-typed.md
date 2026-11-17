---
id: computing-software.software-engineering.python.stub-files-and-py-typed
name: stub-files-and-py-typed
category: computing-software
field: software-engineering
product: python
tags: [python, stub-files, pyi-stubs, py-typed, typeshed, stubgen, type-hints]
level: advanced
status: verified
description: "Ship and consume type information: py.typed marker for inline-typed packages, writing .pyi stubs, stubgen/stubtest, types-* packages from typeshed and local stub paths."
sources: ["https://typing.python.org/en/latest/spec/distributing.html", "https://mypy.readthedocs.io/en/stable/stubs.html", "https://mypy.readthedocs.io/en/stable/stubtest.html", "https://github.com/python/typeshed"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stub files and py.typed

**Goal:** make your library's types visible to users' type checkers, and get types for
untyped third-party code.

## Publishing an inline-typed package
Type checkers ignore installed packages' inline annotations unless the package contains a
`py.typed` marker (PEP 561).
```
src/mylib/__init__.py
src/mylib/py.typed        # empty file
```
Make sure the build includes it: hatchling includes all files in the package by default;
setuptools >= 69.0 includes `py.typed` and `*.pyi` by default (setuptools 84 build tested: `py.typed` shipped, a `data.json` did not), older setuptools needs
`[tool.setuptools.package-data] mylib = ["py.typed"]`. Check:
`unzip -l dist/mylib-*.whl | grep py.typed`.

## Writing .pyi stubs
Stubs hold signatures only; the checker reads `mod.pyi` instead of `mod.py`.
```python
# fastmath.pyi (next to the compiled fastmath.*.so)
from collections.abc import Sequence
def dot(a: Sequence[float], b: Sequence[float], /) -> float: ...
class Matrix:
    rows: int
    def __init__(self, data: list[list[float]]) -> None: ...
    def __matmul__(self, other: Matrix) -> Matrix: ...
```
Use for C extensions, generated code, or adding types to a package you cannot annotate.
Bodies are `...`; defaults written as `= ...`.

## Generating and checking stubs
```bash
stubgen -p mylib -o stubs/          # mypy's generator: a starting point, needs editing
pyright --createstub somepkg        # pyright's equivalent into typings/
python -m mypy.stubtest mylib       # compare stubs to the runtime module: missing/extra/wrong args
```
Run stubtest in CI for stub packages; drift is the main failure mode.

## Consuming types for untyped libraries
1. Look for `types-<pkg>` on PyPI (typeshed's third-party stubs): `pip install types-requests types-PyYAML`.
2. Otherwise local stubs: put `stubs/<pkg>/__init__.pyi` and set `mypy_path = stubs`
   (mypy) or `stubPath = "stubs"` (pyright, default `typings`).
3. Last resort: `[[tool.mypy.overrides]] module = ["legacylib.*"] ignore_missing_imports = true`.

Stub-only packages for your own lib: name the distribution `<pkg>-stubs`, containing a
`<pkg>-stubs/` directory; checkers prefer it over inline types.

## Gotchas
- A `.pyi` next to a `.py` completely shadows it for the checker; stale stubs hide real types.
- `py.typed` with `partial\n` content marks a partially stubbed stub package.
- Re-exports: in stubs and py.typed packages, `from x import y` is private unless written
  `from x import y as y` or listed in `__all__`.

## Verify
- [ ] In a fresh venv, `pip install mylib && mypy -c "import mylib; reveal_type(mylib.f)"` shows real types.
- [ ] stubtest passes in CI for any hand-written stubs.
