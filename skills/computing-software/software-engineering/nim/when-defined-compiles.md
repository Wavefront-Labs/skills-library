---
id: computing-software.software-engineering.nim.when-defined-compiles
name: when-defined-compiles
category: computing-software
field: software-engineering
product: nim
tags: [when-defined-compiles, compile-time-evaluation, when-defined, define, compiles, declared, hostos, hostcpu, conditional-compilation, nim]
level: practitioner
status: docs-checked
description: "Select code at compile time with when defined(...), -d: flags, system constants and the compiles/declared checks."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# when, defined and compiles

Goal: write portable and feature-flagged code.

- `when` is `if` for conditional compilation: every condition must be a constant `bool` expression, the branches open no new scope, only the branch that evaluates true is translated and the others are not checked for semantics (each condition is still checked). Example: `when sizeof(int) == 8:`. `when` is also allowed inside `object` definitions.
- Build-time values: the pragmas `intdefine`, `strdefine` and `booldefine` read a define as an integer, string or bool: `const FooBar {.intdefine.}: int = 5`, then `nim c -d:FooBar=42 foobar.nim` prints 42 (default 5 without the flag).
- `-d:flag` is a shortcut for `-d:flag=true`. `defined(FooBar)` tells you whether a value was provided.
- The pragmas accept a string for a qualified define name: `{.intdefine: "package.FooBar".}` with `-d:package.FooBar=42`.
- To branch on compile time versus run time use `when nimvm` (see the compile-time skill).

Gotchas:
- `when` branches that are false are not semantically checked, so typos hide there.

Verify: `nim c -d:FooBar=5` changes the const read with `{.intdefine.}`.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository): When statement (read in full) and the section on `intdefine`/`strdefine`/`booldefine` (read in full). Removed because the pages read do not describe them: `hostOS`/`hostCPU` and the `defined(linux)`, `defined(js)`, `defined(cpp)`, `defined(release)`, `defined(danger)` symbol list, the semantics of `compiles(...)` and `declared(...)`, `isMainModule`, and the `static: doAssert` advice. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
