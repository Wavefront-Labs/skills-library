---
id: computing-software.software-engineering.nim.importjs-and-js-interop
name: importjs-and-js-interop
category: computing-software
field: software-engineering
product: nim
tags: [importjs-and-js-interop, cpp-and-js-backends, importjs, emit-js, js-interop, importc-js, npm, binding, nim]
level: advanced
status: docs-checked
description: "Call JS functions and objects from Nim with importjs, emit raw JS, and bind to npm libraries."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/backends.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# importjs and interoperating with JavaScript libraries

Goal: call existing JS code.

- `importc` is the generic way to make backend symbols available in Nim and works on the JS target. Bind a host function: `proc addTwoIntegers(a, b: int): int {.importc.}`; the JS function is defined by the HTML page that hosts the generated script.
- `importjs` is like `importcpp` for C++: it imports JavaScript methods or symbols in general, and the generated code uses the JS method calling syntax `obj.method(arg)`.
- Nim symbols are mangled by default; `exportc` keeps the Nim name (or an alternative name) so JS can call Nim code. The JS target needs no `NimMain` call.
- The JS target has no manual memory management, `cast`, file or OS access, or threading.

Verify: compile with `nim js -o:calculator.js calculator.nim`, open the host HTML, and the browser console shows the call result.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md, ImportJs pragma section) and the Backend integration document (doc/backends.md, Nim code calling the backend, JavaScript invocation example, Backend code calling Nim). Removed because neither document states them: `#` placeholder patterns for `importjs`, `{.emit.}` and `asm` for JS, `importjs` on object types and `new Chart(#)` constructors, `cstring` as the JS string type, `require` for Node and npm usage, and `std/asyncjs`. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
