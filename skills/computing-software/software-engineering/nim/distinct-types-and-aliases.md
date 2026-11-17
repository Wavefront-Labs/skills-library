---
id: computing-software.software-engineering.nim.distinct-types-and-aliases
name: distinct-types-and-aliases
category: computing-software
field: software-engineering
product: nim
tags: [distinct-types-and-aliases, type-system, distinct, borrow, type-alias, cast, unit-safety, nim]
level: advanced
status: docs-checked
description: "Create Nim distinct types with borrowed operations to prevent unit mix-ups, and convert explicitly to the base type."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distinct types and borrowing

Goal: encode units and IDs as types.

```nim
type
  Dollar = distinct int
  Euro = distinct int
proc `*` (x: Dollar, y: int): Dollar {.borrow.}
proc `div` (x: Dollar, y: int): Dollar {.borrow.}
```
- A distinct type is a new type derived from a base type that is incompatible with it; it does not imply a subtype relation. Explicit conversions between the distinct type and its base type are allowed in both directions, and `distinctBase` gives the reverse operation. It is an ordinal type if its base type is.
- You must define all behaviour: `echo d + 12` with `d: Dollar` is an error ("cannot add a number with no unit and a `Dollar`"), and `d + 12.Dollar` fails too because `+` is defined for `int`, not `Dollar`.
- Write the operation by hand, for example ``proc `+` (x, y: Dollar): Dollar = Dollar(int(x) + int(y))``, or use `{.borrow.}`, which makes the compiler reuse the base type's implementation so no code is generated.
- To avoid repeating the borrow boilerplate per currency, the manual wraps it in templates (`additive`, `multiplicative`, `comparable`, `defineCurrency`) and instantiates `defineCurrency(Dollar, int)` and `defineCurrency(Euro, int)`.
- Using a distinct type is the manual's recommended way to model different physical units or currencies.

Verify: adding a `Dollar` to a plain `int` fails to compile until the operation is defined or borrowed.

## Checked

2026-11-08. Read the Nim manual Distinct type section and its currency example in full, plus the tutorial's Distinct type paragraph.

Removed as unconfirmed: the claim that `type Id = int` is a pure alias that overloads cannot distinguish, the `cast[T]` description, the meters example, and the note about forgetting to borrow `==`. Dropped the lib index source (not used).

Method: documentation only; no commands were run.
