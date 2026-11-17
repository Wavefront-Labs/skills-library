---
id: computing-software.software-engineering.python.configuring-mypy-and-pyright
name: configuring-mypy-and-pyright
category: computing-software
field: software-engineering
product: python
tags: [python, python-typing, type-hints, mypy, pyright, basedpyright, gradual-typing, strict-mode, type-checking, py-typed]
level: practitioner
status: verified
description: "Set up mypy or pyright in pyproject.toml, adopt strict checking gradually per module, handle untyped dependencies and ship py.typed for your own package."
sources: ["https://mypy.readthedocs.io/en/stable/config_file.html", "https://mypy.readthedocs.io/en/stable/existing_code.html", "https://microsoft.github.io/pyright/#/configuration", "https://typing.python.org/en/latest/spec/distributing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuring mypy and pyright

**Goal:** a type checker that runs in CI, catches real bugs, and can be tightened module
by module on a legacy codebase without a thousand-error big bang.

## mypy in pyproject.toml
```toml
[tool.mypy]
python_version = "3.12"
files = ["src", "tests"]
strict = true                 # enables disallow_untyped_defs, no_implicit_optional, warn_return_any...
warn_unused_ignores = true
enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]

[[tool.mypy.overrides]]       # legacy packages: relax, then tighten over time
module = ["myapp.legacy.*"]
disallow_untyped_defs = false
check_untyped_defs = true     # still check bodies of unannotated functions

[[tool.mypy.overrides]]
module = ["some_untyped_lib.*"]
ignore_missing_imports = true
```
Gradual adoption order (from mypy's "Using mypy with an existing codebase"): run with
defaults, fix or `# type: ignore[code]` the errors, gate CI, then turn on strict flags one
at a time per package. Never a bare `# type: ignore`; always with the error code.

## pyright / basedpyright
```toml
[tool.pyright]
include = ["src"]
pythonVersion = "3.12"
typeCheckingMode = "strict"     # off | basic | standard | strict
reportMissingTypeStubs = false
executionEnvironments = [{ root = "src" }]
```
Per-file: `# pyright: basic` at the top relaxes one legacy file. Pyright is faster and
is what Pylance uses in VS Code; mypy has a plugin system that pyright lacks. Pick one as the CI gate to avoid fighting both.

## Untyped dependencies
1. Check for stubs: `pip install types-requests` etc. (`mypy --install-types` installs the detected missing stub packages via pip; add `--non-interactive` in CI).
2. Otherwise `ignore_missing_imports` for that module only, never globally.
3. For heavily used libs, write minimal local stubs in `stubs/` and set `mypy_path`.

## Shipping types in your own package
Add an empty `src/yourpkg/py.typed` and include it in the wheel; without it, users'
checkers treat your package as untyped.

## CI
```bash
mypy            # uses [tool.mypy] files
pyright         # or: npx pyright / basedpyright
```
Pin the checker version: new releases add errors.

## Verify
- [ ] CI fails on a deliberately wrong annotation (`x: int = "a"`).
- [ ] `warn_unused_ignores` reports no stale ignores.
- [ ] `py.typed` is present in the built wheel (`unzip -l dist/*.whl | grep py.typed`).
