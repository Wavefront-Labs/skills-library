---
id: computing-software.software-engineering.v-lang.v-enum-basics
name: v-enum-basics
category: computing-software
field: software-engineering
product: v-lang
tags: [v-enum-basics, enums, enum, enum values, red, int cast, match enum, variants, v-lang]
level: intro
status: docs-checked
description: "Declare enums with optional explicit values, use the .name shorthand, convert to int, iterate and match exhaustively."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring and using enums

Goal: model a closed set of named values.

- An enum is a group of constant integer values, each with its own name; values start at 0 and increase by 1: `enum Color { red green blue }`. Explicit values are allowed and numbering continues after them: `enum Grocery { apple orange = 5 pear }` gives 0, 5, 6.
- The underlying type can be any integer type, omitted if `int`: `enum Color as u8 { red green blue }`.
- Where the type is known, use the leading dot: `mut color := Color.red`, then `color = .green`; `println(color)` prints `green`. Struct fields expecting an enum accept `.field` too.
- To int: `int(color)`. Operations on enum variables are not allowed; cast to `int` first.
- Name and conversion helpers: `Color.one.str()`; `Cycle.from('two')!` and `Cycle.from(10) or { Cycle.three }` build an enum from a string or integer and return a Result.
- `match` on an enum must be exhaustive or have an `else` branch; with an exhaustive match, `else` is not allowed.
- Enum fields can reuse reserved keywords with the `@` escape (`@struct`).
- `$if` blocks are allowed in enum bodies to include fields conditionally.

Verify: `assert int(Color.blue) == 2`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, section "Enums", "Match"): declaration, numbering, `as u8`, shorthand, `int()` cast, `from`/`str`, exhaustive match, keyword escape, `$if`. Removed as not stated there: `unsafe { Color(2) }` cast, `'${c}'` interpolation, passing `.blue` as a plain function argument, naming-convention and invalid-cast gotchas.

Method: documentation only; no commands were run.
