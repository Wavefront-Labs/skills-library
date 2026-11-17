---
id: computing-software.software-engineering.nim.func-and-side-effects
name: func-and-side-effects
category: computing-software
field: software-engineering
product: nim
tags: [func-and-side-effects, funcs-iterators-converters, func, nosideeffect, purity, side-effects, strictfuncs, nim]
level: practitioner
status: docs-checked
description: "Declare side-effect free Nim funcs, how noSideEffect is checked, and the cast and debugEcho escape hatches."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# func and side-effect tracking

Goal: write verifiably pure code.

- `func` is a shortcut for a `noSideEffect` proc: `func binarySearch[T](a: openArray[T]; elem: T): int` is short for the proc with `{.noSideEffect.}`.
- A routine has no side effects if it does not access a threadlocal or global variable and does not call a routine that has a side effect. It may only change locations reachable from its parameters, and its return value only depends on the parameters. It is a static error to mark a routine `noSideEffect` when the compiler cannot verify it.
- The tutorial adds that funcs cannot access global state (except `const`) but can still change their mutable arguments, those marked `var`, and any `ref` objects.
- Side effects are usually inferred, analogous to exception tracking. For imported functions the compiler cannot infer, annotate with the `sideEffect` pragma.
- To override the analysis use a cast block: `{.cast(noSideEffect).}:` followed by an indented body, for example around `echo "test"`.
- `noSideEffect` implies `gcsafe`.

Gotcha: `debugEcho` is the built-in that pretends to be free of side effects, so use it (not `echo`) to debug routines marked `noSideEffect`.

Verify: putting a plain `echo` in a func is rejected by the compiler.

## Checked

2026-11-08. Read the Nim manual Func and Side effects sections, and the tutorial Funcs and methods section.

Removed as unconfirmed: the `strictFuncs` experimental switch, the exact compiler message text, and the claim about proc variables losing purity information. Dropped the lib index source (not used).

Method: documentation only; no commands were run.
