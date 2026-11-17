---
id: computing-software.software-engineering.nim.sugar-lambdas-collect
name: sugar-lambdas-collect
category: computing-software
field: software-engineering
product: nim
tags: [sugar-lambdas-collect, stdlib-sequtils-algorithm, sugar, lambda, collect, dup, anonymous-proc, arrow, comprehension, with, nim]
level: practitioner
status: docs-checked
description: "Write concise anonymous procs with =>, build collections with collect, copy-and-mutate with dup, and debug with dump."
sources:
  - https://nim-lang.org/docs/sugar.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sugar: => lambdas, collect and dup

Goal: use stdlib sugar for brevity.

- `import std/sugar`. Lambdas: `x => x * 2`, `(a, b) => a + b`, typed `(x: int) -> int` for proc types, e.g. `let f: int -> int = x => x + 1`.
- `collect`: `let sq = collect: (for i in 1..5: i*i)` builds seq; `collect(initHashSet())` and `collect(initTable(2))` for other targets; the last expression of the body picks the add operation: `{e}` for sets, `{k: v}` for tables, `e` for seqs.
- `dup`: `let b = a.dup(sort, reverse)` applies mutating procs to a copy.
- `dump(expr)` prints the expression and its value for quick debugging, e.g. `dump(x + y)` prints `x + y = 30`; `dumpToString` returns the text.
- `capture` copies loop variables into closures: `capture i: procs.add(() => i)`.

Gotchas:
- Semicolons cannot separate procedure arguments in `->` types.
- `capture` is for closures created in a loop, to capture the current iteration values.

Verify: collect yields @[1,4,9,16,25].

## Checked

2026-11-03. Confirmed against the sugar page: `=>`, `->`, collect (with and without init), dup, dump, dumpToString, capture and their examples. Removed: `with(...)` (it is not in sugar), `collect(newTable)` (the page uses `initTable(2)`) and the closure allocation/gcsafe claim.

Method: documentation only; no commands were run.
