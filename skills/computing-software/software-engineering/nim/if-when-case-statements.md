---
id: computing-software.software-engineering.nim.if-when-case-statements
name: if-when-case-statements
category: computing-software
field: software-engineering
product: nim
tags: [if-when-case-statements, control-flow, if, elif, when, case, of, branching, expression, nim]
level: intro
status: docs-checked
description: "Branch in Nim with if/elif/else, compile-time when, and case over ordinals and strings, also as expressions."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# if, when and case statements

Goal: choose the correct branching construct.

- `if cond: ... elif ...: ... else: ...`; zero or more `elif` parts and the `else` part is optional. An `if` expression is like a ternary operator and always yields a value, so its `else` part is required.
- `when` is almost identical to `if` but each condition must be a constant expression evaluated by the compiler, its branches do not open a new scope, and the compiler checks semantics and produces code only for the first branch whose condition is true. Use it for platform-specific code, for example `when system.hostOS == "linux":`. `when` also has an expression form.
- `case x` with `of 1, 2:` and `of 3..8:` (ranges for ordinals) and `of "a":`. The tutorial says you must cover every value of an integer, so add `else: discard` when you do not; string cases always need an `else` because all strings cannot be listed. For enumerations and subranges the compiler checks that every value is covered.
- `case` works as an expression too; a branch with several statements uses the last expression as its value.
- The manual lists the allowed `case` value types as ordinal types, floats, strings and cstrings.

Gotchas:
- Indentation, not braces, groups statements, and it must use spaces; tabs are not allowed.
- A `when` branch that is not selected is not code-generated, so use `if` where you want everything type-checked.

Verify: removing an enum branch and the `else` makes the compiler report a missing case.

## Checked

2026-11-08. Searched the tutorial (If statement, Case statement, When statement, Statements and indentation, first-program indentation note) and the manual (Indentation, Case statement, If expression, When expression, Case expression). The bullets above match those sections.

Corrected: the old note that `case` on floats is not allowed contradicts the manual, which lists floats among the allowed case value types. Removed the `defined(windows)` example and the claim that `when` hides errors in the dead branch as phrased; the tutorial only says semantics are checked for the selected branch. Dropped the lib index source (not used).

Method: documentation only; no commands were run.
