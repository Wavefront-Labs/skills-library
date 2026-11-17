---
id: computing-software.software-engineering.nim.custom-pragma-macro-and-dsl
name: custom-pragma-macro-and-dsl
category: computing-software
field: software-engineering
product: nim
tags: [custom-pragma-macro-and-dsl, macros, macro-pragma, custom-pragma, hascustompragma, dsl, annotation, getcustompragmaval, nim]
level: sme
status: docs-checked
description: "Define user pragmas and macro pragmas in Nim, detect custom annotations with hasCustomPragma and getCustomPragmaVal, and report errors from macros."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/macros.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom pragmas and macro pragmas

Goal: annotate declarations and act on them.

- User pragma alias: `{.pragma: name, ...}` bundles pragmas under a new name.
- Custom annotations: a template marked `{.pragma.}` becomes an annotation, e.g. `template dbTable(name: string, table_space: string = "") {.pragma.}`; apply it as `{.dbTable: "t".}` on a type or field, and query it with `hasCustomPragma` and `getCustomPragmaVal` from the macros module.
- Macro pragmas: a macro used as `{.name.}` receives the annotated definition and returns the replacement. Several macro pragmas are applied left to right.
- Inside macros use `getTypeImpl` / `getTypeInst` to inspect types, `error("msg", node)` to report a compile error at a node, and `expandMacros` to see the result.

Gotchas:
- A custom annotation does nothing by itself; some macro or code must read it.

Verify: the annotated definition compiles and the query returns the value.

## Checked

2026-11-03. Confirmed in the manual (user pragmas, custom annotations, macro pragmas, ordering) and macros docs (hasCustomPragma, getCustomPragmaVal, getTypeImpl, getTypeInst, error, expandMacros). Removed: `{.cache.}`-specific claims.
Method: documentation only; no commands were run.
