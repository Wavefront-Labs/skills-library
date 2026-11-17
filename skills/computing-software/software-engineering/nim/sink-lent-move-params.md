---
id: computing-software.software-engineering.nim.sink-lent-move-params
name: sink-lent-move-params
category: computing-software
field: software-engineering
product: nim
tags: [sink-lent-move-params, destructors-move-semantics, sink, lent, move, ensuremove, ownership, borrowing, owned, nim]
level: sme
status: docs-checked
description: "Use sink parameters to take ownership, lent results to borrow, and move/ensureMove to avoid copies in hot code."
sources:
  - https://nim-lang.org/docs/destructors.html
  - https://nim-lang.org/docs/mm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sink, lent and move parameters

Goal: avoid hidden copies.

- `proc add(s: var Q, x: sink T)` means the proc takes ownership of `x`. A location passed to a `sink` parameter should not be used afterwards; the compiler proves it is the last use (static control flow analysis over local variables) and otherwise passes a copy.
- A `sink` parameter may be consumed once in the body but need not be consumed at all (affine, not linear), so `put(t: var Table; k: sink Key, v: sink Value)` works without extra overloads.
- Object and tuple fields are tracked separately: consuming `tup[0]` leaves `tup[1]` usable.
- `lent T` as a return type is a hidden pointer, like `var T` but unable to mutate; the compiler proves it does not outlive its origin. Use it for getters such as ``proc `[]`(x: Tree; i: int): lent Tree`` and for iterators yielding `lent`. No destructor call is injected for `lent` or `var` expressions.
- `move(x)` forces a move and calls `=wasMoved`; `ensureMove(x)` has no runtime effect but is a static error if the compiler cannot prove the move is safe (valid for a local or a `sink` parameter, invalid for a normal parameter).
- Move elements explicitly when needed: `dest[i] = move(src[i])`.
- `--sinkInference:on` (or `{.push sinkInference: on.}` ... `{.pop.}`) enables limited sink parameter inference; `{.nosinks.}` disables it for one routine.
- Inspect what the compiler injected with `--expandArc:functionName` (or a file name for the whole module).

Verify: `--expandArc:myProc` shows a `=sink` rather than `=copy` after your change.

## Checked

2026-11-08. Confirmed against the Nim Destructors and Move Semantics document (doc/destructors.md, read in full) for sink semantics, field tracking, `lent`, `move`, `ensureMove`, sink inference and `.nosinks`, and against Nim's Memory Management document (doc/mm.md, read in full) for `--expandArc:functionName`. Removed: the "const ref" comparison for `lent`, the `var T` return claim, "the compiler may warn" on use after move, and "sink on a type without moves is just a copy". The old sources (manual, tut1, lib) were not read for this skill and were dropped.
Method: documentation only; no commands were run.
