---
id: computing-software.software-engineering.nim.enums-subranges-ordinals
name: enums-subranges-ordinals
category: computing-software
field: software-engineering
product: nim
tags: [enums-subranges-ordinals, type-system, enum, subrange, ordinal, set, ord, succ, pred, nim]
level: practitioner
status: docs-checked
description: "Define Nim enums with explicit values and string names, restrict ints with subranges, and use ordinal operations and sets."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums, subranges and ordinal types

Goal: model closed domains with types.

- `type Direction = enum north, east, south, west` gives ordered symbols mapped to 0, 1, 2, 3; qualify with `Direction.south` to avoid ambiguity. `$` converts a value to its name and `ord` to its integer.
- Explicit values must be ascending, and a field without one gets the previous value plus 1. String values are set with `valueB = "value B"` or a tuple `valueA = (0, "my value A")`, and control the result of `$`.
- An enum with holes (for example `a = 2, b = 4, c = 89`) is not ordinal anymore: it cannot index arrays and `inc`, `dec`, `succ` and `pred` are not available for it.
- `{.pure.}` enums add their fields to a hidden module-specific scope that is queried last, so ambiguous names such as `amb` need qualification like `MyEnum.amb`.
- Ordinal types are enums, integer types, `char` and `bool`, plus subranges. Operations: `ord`, `inc(x)`, `inc(x, n)`, `dec`, `succ`, `pred` (the n-th variants take a count). `inc`, `dec`, `succ` and `pred` can raise `RangeDefect` or `OverflowDefect` when the matching runtime checks are on.
- Subrange: `type MySubrange = range[0..5]` holds only 0 to 5; assigning another value is a compile-time or runtime error, and assignments to and from the base type are allowed. `Natural` is `range[0..high(int)]`, which the tutorial prefers to unsigned types for non-negative numbers.
- Sets: `set[T]` for an ordinal base type such as `char`, enums, `int8`-`int16`, `uint8`-`uint16`, or ordinal subranges. `{}` is the empty set; `A + B` is union, `A * B` intersection, `A - B` difference, `A == B` equality, `A <= B` subset, `A < B` proper subset.

Gotcha: a set base type is limited by `MaxSetElements` (2^16); `set[int64]` is an error. The tutorial points to `std/sets` hash sets for larger types.

Verify: assigning 6 to a `range[0..5]` variable is reported as an error.

## Checked

2026-11-08. Read the Nim manual Enumeration types section in full and the tutorial sections Enumerations, Ordinal types, Subranges and Sets.

Removed as unconfirmed: the `Color(x)` unchecked conversion note, the `incl`, `excl` and `in` set operators, and the claim that sets of enums with holes are disallowed (the manual says only that such enums are not ordinal and cannot index arrays). Dropped the lib index source (not used).

Method: documentation only; no commands were run.
