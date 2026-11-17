---
id: computing-software.software-engineering.nim.loops-for-while
name: loops-for-while
category: computing-software
field: software-engineering
product: nim
tags: [loops-for-while, control-flow, for, while, countup, countdown, items, pairs, range, loop, nim]
level: intro
status: docs-checked
description: "Iterate in Nim with for over ranges, collections and pairs, use while, countdown, and the implicit items/pairs calls."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loops: for, while and range iteration

Goal: write correct loops.

- `for i in countup(1, 10)` runs 1 to 10; `1 .. 10` does the same and `countdown(10, 1)` counts down. `0 ..< 10` is the same as `0 .. 9`, so `..<` excludes the upper bound and `..` includes it.
- `for item in collection` is rewritten to `items(collection)` when the expression is not an iterator and there is one loop variable; with exactly two variables a `pairs` iterator is invoked implicitly.
- `items` and `mitems` give immutable and mutable elements; `pairs` and `mpairs` give the element and its index (immutable and mutable respectively).
- If an iterator yields a tuple, you can have one loop variable per tuple component.
- `while cond:` runs until the condition is false; endless loops are not an error, and `while`/`for` open an implicit block so `break` can leave them. `continue` starts the next iteration.
- The loop variable is declared by the loop and its scope ends with the loop body.

Gotcha: using `..` instead of `..<` is the classic off-by-one when indexing with `len`.

Verify: `for i in 0 ..< 3: echo i` prints 0, 1, 2.

## Checked

2026-11-08. Searched the tutorial (For statement, While statement, Scopes and the block statement) and the manual (For statements, Implicit items/pairs invocations, While statement). The bullets above match those sections.

Removed as unconfirmed: the claim that modifying a seq while iterating raises an assertion in debug builds, the claim that loop variables are immutable inside the body, the table key/value example, and the string index/char example. Dropped the lib index source (not used).

Method: documentation only; no commands were run.
