---
id: computing-software.software-engineering.nim.macro-debugging-treerepr
name: macro-debugging-treerepr
category: computing-software
field: software-engineering
product: nim
tags: [macro-debugging-treerepr, macros, treerepr, lisprepr, expandmacros, dumptree, debug, macro-debugging, nim]
level: practitioner
status: docs-checked
description: "Debug Nim macros with dumpTree, dumpLisp, dumpAstGen, treeRepr, lispRepr, astGenRepr, repr, expandMacros, error, and the --expandMacro compiler option."
sources:
  - https://nim-lang.org/docs/macros.html
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/system.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging macros

Goal: see the AST a macro receives and produces.

- `dumpTree: <stmts>`, `dumpLisp: <stmts>` and `dumpAstGen: <stmts>` print the AST of untyped statements at compile time (tree, Lisp form, and Nim code that rebuilds it).
- On a NimNode value use `treeRepr`, `lispRepr`, `astGenRepr` (strings) and `repr` (source-like text, from system).
- `expandMacros: body` (typed) shows the code after macro expansion.
- Compiler option `--expandMacro:MACRO` dumps every AST generated from the named macro.
- `error("message", node)` stops compilation with a message located at the node.

Gotchas:
- Output appears at compile time, not when the program runs.

Verify: compile once and read the printed tree.

## Checked

2026-11-03. Confirmed in the macros module docs, system docs (`repr`) and compiler guide (`--expandMacro`). Removed: `static: echo`, `{.error: "msg".}` and "repr omits hidden conversions" claims (not shown in the pages).
Method: documentation only; no commands were run.
