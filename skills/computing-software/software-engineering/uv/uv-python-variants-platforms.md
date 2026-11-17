---
id: computing-software.software-engineering.uv.uv-python-variants-platforms
name: uv-python-variants-platforms
category: computing-software
field: software-engineering
product: uv
tags: [uv, free-threaded, debug-build, pypy, pyodide, windows-registry, python-versions, rosetta]
level: practitioner
status: docs-checked
description: "Request free-threaded, debug, PyPy, GraalPy and Pyodide interpreters in uv, force x86_64 emulation, and use the Windows registry and py launcher."
sources: [https://docs.astral.sh/uv/concepts/python-versions/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv Python variants, implementations and platforms

Goal: select non-default builds and implementations deliberately.

## Method

Free-threaded (CPython 3.13+):

- 3.13: never selected by default; request `3.13t` or `3.13+freethreaded`.
- 3.14+: allowed without explicit selection, but the GIL build is still preferred (for example `uv python install 3.14`). A free-threaded interpreter that comes first on PATH will be used.
- To require the GIL build when both exist: the `+gil` specifier, e.g. `3.14+gil`.

Debug builds (assertions on, slower, not for general use): request `3.13d` or `3.13+debug`. They are used when nothing else matches or you give the executable path. Unlike usual uv CPython installs, their debug symbols are not stripped, which helps C-level debugging.

Implementations: CPython (`cpython`, `cp`), PyPy (`pypy`, `pp`), GraalPy (`graalpy`, `gp`), Pyodide (`pyodide`); names are not case-sensitive. Unsupported implementations are not discovered. Examples: `uv python install pypy`. Upgrades are not supported for PyPy, GraalPy or Pyodide. PyPy comes from the PyPy project and lags CPython (up to 3.11 per the page). Pyodide, from the Pyodide project, is CPython for WebAssembly / Emscripten.

x86_64 on aarch64 (Rosetta 2 on macOS, Windows on ARM emulation): x86_64 uv can use either interpreter, but an interpreter needs packages of its own architecture (all x86_64 or all aarch64). Force emulated Python with `UV_PYTHON_ARCH=x86_64` or an explicit request such as `cpython-3.14-windows-x86_64`.

Windows registry: managed installs register per PEP 514, then the `py` launcher works:

```console
$ uv python install 3.13.1
$ py -V:Astral/CPython3.13.1
```

Uninstalling removes that registry entry and any broken ones.

## Verify

The page's example: after `uv python install 3.13.1` on Windows, `py -V:Astral/CPython3.13.1` launches that interpreter.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/python-versions). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
