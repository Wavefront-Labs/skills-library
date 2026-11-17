---
id: computing-software.software-engineering.nim.iterators-inline-closure
name: iterators-inline-closure
category: computing-software
field: software-engineering
product: nim
tags: [iterators-inline-closure, funcs-iterators-converters, iterator, yield, closure-iterator, inline-iterator, generator, items, nim]
level: practitioner
status: docs-checked
description: "Write inline and closure iterators with yield in Nim, and know the restrictions that differ from procs."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterators: inline and closure

Goal: produce sequences lazily.

- Replace `proc` by `iterator` and use `yield` to return and continue: `iterator countup(a, b: int): int` loops with `yield res`.
- Iterators differ from procs: they can only be called from `for` loops, cannot contain `return` (and procs cannot contain `yield`), have no implicit `result`, do not support recursion, and cannot be forward declared because the compiler must inline them. The tutorial flags the last restriction as expected to go away in future.
- There are two kinds. An inline iterator is always inlined, with zero overhead but possibly a heavy increase in code size; ideally refactor it to contain a single `yield`. Iterators not marked `{.closure.}` or `{.inline.}` default to inline.
- Inline iterators are second class: they can be passed as parameters only to inlining facilities such as templates, macros and other inline iterators.
- `iterator count0(): int {.closure.}` is a closure iterator that can be passed around freely, for example to `proc invoke(iter: iterator(): int {.closure.})`. `finished(it)` tests whether it has completed.
- In a closure iterator `return` is allowed and ends the iteration; a closure iterator cannot be executed at compile time for now. Closure iterator invocation typically costs more than an inline iterator.
- A `for x in obj` loop with one variable is rewritten to `items(obj)`, and with two variables to `pairs(obj)`, so custom containers define those iterators.
- Iterators have their own namespace, so wrapping one in a proc of the same name that accumulates a seq is common (the tutorial cites `split` from strutils).

Verify: `for x in evens(6): echo x` prints 0, 2, 4.

## Checked

2026-11-08. Read the Nim tutorial Iterators section and the manual First-class iterators and Implicit items/pairs invocations sections.

Removed as unconfirmed: the claim that closure iterators capture variables and allocate, and the `toSeq` from sequtils remark. Dropped the lib index source (not used).

Method: documentation only; no commands were run.
