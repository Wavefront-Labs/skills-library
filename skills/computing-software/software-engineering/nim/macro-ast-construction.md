---
id: computing-software.software-engineering.nim.macro-ast-construction
name: macro-ast-construction
category: computing-software
field: software-engineering
product: nim
tags: [macro-ast-construction, macros, macro, nimnode, ast, quote-do, newtree, nnk, metaprogramming, nim]
level: advanced
status: docs-checked
description: "Build Nim ASTs in macros with quote do, newTree, newStmtList, newLit, ident, genSym and newCall, and inspect nodes with kind, len, strVal and intVal."
sources:
  - https://nim-lang.org/docs/macros.html
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Constructing ASTs in macros

Goal: generate code with the least hand-built tree.

- Start with `quote do:`; backticks interpolate NimNodes: `macro hello(name: untyped): untyped = result = quote do: echo "hello ", `name``.
- Build nodes explicitly with `newTree(kind, children...)`, `newStmtList(...)`, `newCall("name", args...)` (accepts a string name), `ident("x")` for identifiers, and `newLit(value)` to turn a compile-time value (ints, strings, sequences, and more via many overloads) into a literal node. Append with `add`.
- Fresh names: `genSym` makes a unique symbol so generated variables do not collide with user code.
- Read nodes: `node.kind` (an `NimNodeKind` such as `nnkCall`), `node.len`, `node[i]`, `node.strVal` for identifiers/strings, `node.intVal` for integer literals.
- Typed macros can look inside types with `getTypeImpl` and `getTypeInst`.
- Prefer `quote do` unless the shape depends on the input; use `newTree` for variable-length structure.

Gotchas:
- `untyped` parameters are not type-checked before the macro runs; `typed` ones are.

Verify: print the result with `echo result.repr` or `treeRepr` (see the macro-debugging skill).

## Checked

2026-11-03. Confirmed in the macros module docs (quote, newTree, newStmtList, newLit, ident, genSym, kind, len, strVal, intVal, newCall, add, getTypeImpl, getTypeInst) and the manual. Removed: the unverified "macros cannot do I/O" claim and a long hand-built tree example not shown in the pages.
Method: documentation only; no commands were run.
