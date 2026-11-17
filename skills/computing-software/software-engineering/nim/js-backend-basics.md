---
id: computing-software.software-engineering.nim.js-backend-basics
name: js-backend-basics
category: computing-software
field: software-engineering
product: nim
tags: [js-backend-basics, cpp-and-js-backends, nim-js, javascript-backend, dom, browser, node, karax, importjs, nim]
level: practitioner
status: docs-checked
description: "Compile Nim to JavaScript with nim js, target browser or Node, interact with the DOM and ship the generated script."
sources:
  - https://nim-lang.org/docs/backends.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JavaScript backend: nim js, DOM and output

Goal: write front-end or Node code in Nim.

- `nim js -o:calculator.js calculator.nim` generates a `.js` file. Nim targets JavaScript 1.5 and, since JS has no portable module include, generates one long `.js` file.
- By default the file is meant to be referenced from an `.html` file (`<script type="text/javascript" src="calculator.js"></script>`). `echo` output then appears in the browser console.
- To run under Node.js use `nim js -r examples/hallo.nim`. If you see errors that `globalThis` is not defined, use a recent Node.js (at least 12.0).
- Browser DOM access: the `dom` module has DOM querying and modification procs; Karax is the referenced framework for browser applications.
- Not available on the JS target: manual memory management (`alloc`), `cast` and other unsafe operations (`zeroMem`), file management, OS-specific operations, threading and coroutines, and some standard library modules. The stdlib has modules catered to the JS backend.
- Call page JS from Nim with `importc` (the generic way, works on JS too): `proc addTwoIntegers(a, b: int): int {.importc.}`, with the JS function defined in the host HTML.
- Nim symbols are mangled; `exportc` keeps the Nim name for the backend. The JS target needs no `NimMain` initialisation (C targets do).

Verify: open the host HTML in a browser; the console shows `10` for the `addTwoIntegers(3, 7)` example.

## Checked

2026-11-08. Confirmed against the Nim Backend integration document (doc/backends.md from the Nim repository), read in full. Removed because it does not state them: `-d:release` and `-d:nodejs` flags, `import std/dom` usage and `innerHTML` example, 64-bit integer emulation, and source map flags. The manual, tut1 and lib sources were not read for this skill and were dropped.
Method: documentation only; no commands were run.
