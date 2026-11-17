---
id: computing-software.software-engineering.v-lang.v-dynamic-array-basics
name: v-dynamic-array-basics
category: computing-software
field: software-engineering
product: v-lang
tags: [v-dynamic-array-basics, arrays, array, int, append, len, cap, insert, delete, in operator, v-lang]
level: intro
status: docs-checked
description: "Create dynamic arrays with literals and []T{len, cap, init}, append with <<, index with or-blocks, check membership, and insert or delete elements."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic arrays: create, append, index

Goal: use growable arrays properly.

- Literal: `mut a := [1, 2, 3]`; the first element fixes the type (`[u8(16), 32]` forces `u8`). Elements must all share one type; braces take only named options, so `[]int{1, 2, 3}` is a syntax error.
- Sized: `[]int{len: 5, init: 0}`, `[]string{cap: 100}`, `[]int{}` for empty. `len`, `cap` and `init` are optional (`len` defaults to 0). The runtime keeps `cap` at least `len`. `init` may use `index`, e.g. `[]int{len: 6, init: index * index}`.
- Append: `a << 4`, `a << [5, 6]` appends an entire array. Also `a.insert(1, 9)`, `a.insert(1, [3, 4])`, `a.prepend(0)`, `a.delete(2)`, `a.delete_many(start, size)`, `a.pop()` (removes and returns the last), `a.trim(new_len)`, `a.clear()`.
- Access `a[i]` panics when out of range. `a[i] or { default }` handles that, and `a[i]!` propagates the error. `a.first()` and `a.last()` equal `a[0]` and `a[a.len - 1]`.
- Membership: `3 in a`, `3 !in a`.
- `a == b` compares arrays (e.g. `assert count == [0, 1, 2, 3]`). Copy with `a.clone()`; spread syntax `[...base, 3, 4]` builds a new array from an existing one.
- Pushing the elements of an array into an interface array: `<< ...array` converts each element, `<< array` appends the whole array as one value.

Gotchas:
- A value of another type will not compile: `names << 10` fails for `[]string`.
- `len` and `cap` are read-only fields.

Verify: `mut a := [1]; a << 2; assert a == [1, 2]`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Arrays", "Array Fields", "Array Initialization", "Array update syntax", "Array methods", and the "Option/Result" array index example) and vlib/builtin/array.v (method list). Removed as not stated: the claim that `a[i] or { default }` is invalid for arrays (the docs show it is valid), the `mut` requirement wording, and the vague pass-by-value note.

Method: documentation only; no commands were run.
