---
id: computing-software.software-engineering.v-lang.v-for-in-loops
name: v-for-in-loops
category: computing-software
field: software-engineering
product: v-lang
tags: [v-for-in-loops, loops-and-labels, for in, for loop, range, iterator, foreach, mut iteration, next method, v-lang]
level: intro
status: docs-checked
description: "Iterate arrays, maps and ranges with for in, indexed and mutable forms, reference iteration with &, and custom iterators with a next method."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for-in loops over arrays, maps, ranges and custom iterators

Goal: iterate with the right form.

- Values: `for num in numbers { }`; index and value: `for i, name in names { }`. The value is read-only; for mutation write `for mut num in numbers { num++ }` on a `mut` array.
- By default elements are taken by value; iterate `&users` to receive references (`for user in &users { }`), and the same applies to maps.
- Ranges: `for i in 0 .. 5 { }`; `low..high` is exclusive of `high`.
- Maps: `for key, value in m { }`; ignore either side with `_`.
- Custom iterators: a type with a `next` method returning an option, e.g. `fn (mut iter SquareIterator) next() ?int` (return `none` when done), works in `for squared in iter { }`.
- A single underscore identifier is ignored.
- `break` and `continue` apply to the innermost loop; label an outer loop (`outer: for ...`) and use `continue outer` / `break outer`.

Gotchas:
- V has only the `for` keyword; see v-conditional-and-c-style-loops for the other forms.

Verify: sum `0 .. 5` and assert 10.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "For loop": Array for, Custom iterators, Map for, Range for, Labelled break and continue). Removed as not found in the docs: iterating a string with `for c in s`, `for v in ch` over a channel (the docs receive with `<-ch or { break }`), descending-range and reverse-loop remarks, and the length-modification warning.

Method: documentation only; no commands were run.
