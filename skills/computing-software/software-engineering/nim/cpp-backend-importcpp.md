---
id: computing-software.software-engineering.nim.cpp-backend-importcpp
name: cpp-backend-importcpp
category: computing-software
field: software-engineering
product: nim
tags: [cpp-backend-importcpp, cpp-and-js-backends, nim-cpp, importcpp, cpp-backend, constructor, cppnonpod, stl, cpp-interop, nim]
level: advanced
status: docs-checked
description: "Wrap C++ in Nim with nim cpp and importcpp patterns (#, #., @, 'N), generic templates, constructor, imported exceptions, and cppNonPod for threadvars."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/backends.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C++ backend and importcpp

Goal: call C++ from Nim.

- Compile with `nim cpp` (also required by `--cc:nvcc`).
- `importcpp` takes a pattern: `#` is the next argument, `#.` a dot/arrow call, `@` the remaining arguments comma separated, `'N` the type of the Nth argument (`'*0` the base type of the result); with no special character a method call is assumed. Examples: `proc cppMethod(this: CppObj, a, b, c: cint) {.importcpp: "#.CppMethod(@)".}`, `{.importcpp: "# + #".}`, `SystemManager::getSubsystem<'*0>()`.
- Generic imported objects map to C++ templates: `StdMap[K, V] {.importcpp: "std::map", header: "<map>".}`.
- The `constructor` pragma wraps constructors.
- Imported C++ exception types can be raised and caught (`except CStdException as e`), using `importcpp` types with `requiresInit`/`inheritable` as in the manual.
- `cppNonPod` applies to non-POD types in `threadvar` variables and needs `--tlsEmulation:off`.

Gotchas:
- No built-in `CppException` type exists; declare your own imported type.

Verify: the program links and the call returns.

## Checked

2026-11-03. Confirmed in the manual and backends guide. Real errors fixed: the skill said `cppNonPod` covers non-trivial ctors/dtors generally (manual: threadvars only) and that `except CppException` exists (it does not). Removed: g++/clang++ claims, refc fragility, `--passC:-std=c++17`.
Method: documentation only; no commands were run.
