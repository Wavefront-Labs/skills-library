---
id: computing-software.software-engineering.v-lang.v-enum-methods-and-match
name: v-enum-methods-and-match
category: computing-software
field: software-engineering
product: v-lang
tags: [v-enum-methods-and-match, enums, enum methods, enum from string, enum parse, exhaustive match, comptime enum, v-lang]
level: practitioner
status: docs-checked
description: "Add methods to enums, build lookup tables, parse enums from strings and guard against invalid values."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enum methods and exhaustive match

Goal: give enums behaviour and conversions.

- Enums can have methods, just like structs: `fn (c Cycle) next() Cycle { match c { .one { return .two } .two { return .three } .three { return .one } } }`.
- From string or integer: `Cycle.from('two')!` and `Cycle.from(10) or { Cycle.three }`; `from` returns a Result and can be forwarded from a function returning `!Enum`. To string: `Cycle.one.str()`.
- Enum match must be exhaustive or have an `else` branch, which ensures a newly added field is handled everywhere. With an exhaustive match, `else` is not allowed.
- Multiple values in one arm: `.red, .blue { true }`.
- When an `if` or `match` expression compares with `==`/`!=` against an enum value, the enum operand supplies the type for shorthand values such as `.red` in the branches. A qualified value in the first branch (`Color.red`) types later `.blue` branches.
- Operations on enum values are not allowed; cast to `int` explicitly.

Gotcha: adding a variant makes every exhaustive match fail to compile, which catches places that need updating.

Verify: cover each variant in a test table.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Enums", "Match", "If expressions"). Removed as not stated there: comptime `$for v in Color.values`, the hand-written `const all` list, JSON enum serialization claims and `@[json_as_number]`, API-ordering advice.

Method: documentation only; no commands were run.
