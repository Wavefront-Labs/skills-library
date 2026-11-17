---
id: computing-software.software-engineering.nim.common-pragmas
name: common-pragmas
category: computing-software
field: software-engineering
product: nim
tags: [common-pragmas, effects-and-pragmas, pragma, inline, noinit, deprecated, discardable, used, push, pop, nim]
level: practitioner
status: docs-checked
description: "Use frequently needed pragmas to control inlining, initialization, warnings, deprecation, discardability and export."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common pragmas: inline, deprecated, push/pop and friends

Goal: apply pragmas correctly.

- Pragmas give the compiler extra information and are enclosed in `{.` and `.}`; they are processed during semantic checking.
- `{.deprecated.}` marks a symbol deprecated; an optional string is relayed to developers: `proc thing(x: bool) {.deprecated: "use thong instead".}`.
- `{.discardable.}` lets callers ignore a proc's or iterator's result; it does not work on templates.
- `{.used.}` suppresses the warning for a non-exported unused symbol (useful for macro-generated code); as a top-level statement it marks a module as used and avoids the "Unused import" warning.
- Compilation option pragmas: `checks`, `boundChecks`, `overflowChecks`, `nilChecks`, `assertions` (all `on|off`), `warnings`, `hints` (`on|off`), `optimization` (`none|speed|size`), `patterns`, and `callconv`. Example: `{.checks: off, optimization: speed.}`.
- `{.push checks: off.}` ... `{.pop.}` overrides settings for a region and also works for some standard pragmas: `{.push inline.}` ... `{.pop.}` makes the procs inside inlined.
- `{.compileTime.}` is for procs and variables used during compile-time execution; `{.global.}` on a variable inside a proc stores it globally, initialised once at program startup (per instantiation inside a generic proc).
- `{.error: "msg".}`, `{.warning: "msg".}`, `{.hint: "msg".}` and `{.fatal: "msg".}` emit diagnostics; `error` does not necessarily abort compilation, `fatal` is guaranteed to abort. They are often put under `when`. `{.error.}` on a proc makes any use a static error.
- Switch off one message with its identifier: `{.hint[XDeclaredButNotUsed]: off.}`.
- `{.experimental: "feature".}` enables an experimental feature for the rest of the module; inside generics or macros that cross modules put it in `push`/`pop`.
- Custom pragmas are declared with the `pragma` pragma (`{.pragma: rtl, exportc, dynlib, cdecl.}`).

Verify: a deprecated proc shows a warning at the call site.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository): Pragmas chapter intro and the deprecated, compileTime, error, fatal, warning, hint, compilation option, push/pop, global, disabling messages, used and experimental sections, plus the discardable section of the statements chapter and the pragma pragma section. Removed because those sections do not state them: `noinline` and `noinit` behaviour, and the claims on pragma placement order and misspelled pragmas. `inline` is only documented there through the `push inline` example. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
