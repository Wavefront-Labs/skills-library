---
id: computing-software.software-engineering.nim.static-const-compiletime
name: static-const-compiletime
category: computing-software
field: software-engineering
product: nim
tags: [static-const-compiletime, compile-time-evaluation, static, const, compiletime, vm, static-block, nim]
level: practitioner
status: docs-checked
description: "Run code at compile time with const initialisers, static blocks, static params and the compileTime pragma."
sources:
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# static blocks, const and compileTime

Goal: move work from run time to compile time.

- A `const` section declares constants whose values are constant expressions, computed at compile time: `constEval = contains("abc", 'b')`. The value part of each declaration opens its own scope, so symbols declared inside it are not visible outside.
- `static:` runs a block at compile time and may have side effects such as `echo` (printed during compilation). `static(expr)` evaluates `expr` at compile time and uses the result at run time: `echo static(getNum(123))`.
- It is a static error if the compiler cannot execute the block at compile time; the manual's "Restrictions on Compile-Time Execution" section lists what is not allowed.
- `{.compileTime.}` marks a proc or variable for compile-time execution only; no code is generated for a proc. `compileTime` variables are also available at run time, which suits lookup tables that are filled at compile time (typically by macros) and read at run time.
- A proc using `NimNode` in its parameter types is implicitly `compileTime`.
- `when nimvm:` gives different code for compile time and run time. Requirements: the expression must be exactly `nimvm`, no `elif` branches, an `else` branch is required, and the branches must not change the semantics of the code after the statement (for example by defining symbols used later).

```nim
proc inVm(): bool =
  when nimvm: true
  else: false
const ct = inVm()   # true
let rt = inVm()     # false
```

Verify: `ct` is true and `rt` is false in the example above.

## Checked

2026-11-08. Confirmed against the Nim Manual (doc/manual.md from the Nim repository): Const section, Static statement/expression, When nimvm statement and compileTime pragma, each read in full. Not read, so removed: `static[T]` parameters, the VM limits and the `--maxLoopIterationsVM`, `--maxCallDepth` flags, `staticRead`/`staticExec`, and the binary-size and compile-time cost remarks. tut1 and lib were not read and were dropped from sources.
Method: documentation only; no commands were run.
