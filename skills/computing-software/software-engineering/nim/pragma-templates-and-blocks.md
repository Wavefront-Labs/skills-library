---
id: computing-software.software-engineering.nim.pragma-templates-and-blocks
name: pragma-templates-and-blocks
category: computing-software
field: software-engineering
product: nim
tags: [pragma-templates-and-blocks, templates, pragma-template, custom-pragma, block-template, do-notation, template-pragma, nim]
level: advanced
status: docs-checked
description: "Use templates as custom pragmas, as statement blocks with trailing blocks, and to define reusable pragma sets."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pragma templates and block-style templates

Goal: bundle pragmas and block syntax with templates.

- The `pragma` pragma declares a user-defined pragma that bundles others: `{.pragma: rtl, exportc, dynlib, cdecl.}`, then apply it as `{.rtl.}` on a proc. User-defined pragmas live in a different module-wide scope than other symbols and cannot be imported from a module.
- Custom annotations are templates carrying the `pragma` pragma: `template dbTable(name: string, table_space: string = "") {.pragma.}`. They do not affect code generation; macros can detect them (the macros module has helpers).
- Pass a block to a template as the last argument with the colon syntax: `withFile(txt, "f.txt", fmWrite):` followed by the indented statements, which bind to the `actions` parameter.
- The block parameter normally has to be `untyped`: a `typed` body is type-checked before it is passed, so a proc declared by the template is not visible to it (`undeclared identifier`), whereas with `untyped` it compiles.
- A template where every parameter is `untyped` is an immediate template; the explicit `immediate` pragma is obsolete and deprecated, so use `untyped` parameters.
- Templates may be redefined with the same signature; the `redefine` pragma makes it explicit and silences the implicit-redefinition warning.

Verify: the colon-block call to your template compiles, and the custom pragma is detected by the macro that reads it.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository): Templates chapter through Varargs of untyped, immediate and redefine pragmas, and the User-defined pragmas chapter (pragma pragma and custom annotations). Removed because not found there: `repeat 3: echo "x"` style non-parenthesised calls, `do:`/`of`/`else` multi-block advice, `getAst`, the "template that expands to a proc declaration must return untyped" rule, and `--expandMacro`. The pragma set `inline, noSideEffect` was replaced by the manual's own example. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
