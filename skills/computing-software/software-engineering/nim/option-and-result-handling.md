---
id: computing-software.software-engineering.nim.option-and-result-handling
name: option-and-result-handling
category: computing-software
field: software-engineering
product: nim
tags: [option-and-result-handling, collections-tables-sets-options, option, some, none, results, result-type, optional, error-handling, nim]
level: practitioner
status: docs-checked
description: "Represent missing values with std/options: some, none, isSome, get, map and filter."
sources:
  - https://nim-lang.org/docs/options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Option[T] for absent values

Goal: model absence and failure without nil.

- `import std/options`; `let o = some(5)`, `none(int)`, `o.isSome`, `o.get`, `o.get(otherwise)`, `o.map(callback)` and `o.filter(callback)` from `std/options` itself, `if o.isSome: ...`.
- Use `Option[T]` for lookups: `proc find(...): Option[Item]`.
- `get` on `none` raises `UnpackDefect`; check first or use `get(otherwise)`.

Gotchas:
- Calling `get` on a `none` raises `UnpackDefect`, which is a defect, not a catchable error to rely on.

Verify: `none(int).get(7)` returns 7.

## Checked

2026-11-03. Confirmed against the options page: some, none, isSome, get, get(self, otherwise), map, filter, UnpackDefect on get of none. Removed: the `results` package section (not verifiable from official docs here), the `$`/`==` remark, the ref-nil gotcha and the exceptions-versus-Option convention.

Method: documentation only; no commands were run.
