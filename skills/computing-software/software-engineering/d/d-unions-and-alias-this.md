---
id: computing-software.software-engineering.d.d-unions-and-alias-this
name: d-unions-and-alias-this
category: computing-software
field: software-engineering
product: d
tags: [d-unions-and-alias-this, structs-and-unions, union, sumtype, variant, alias-this, tagged-union, algebraic, d]
level: practitioner
status: docs-checked
description: "Overlay fields with union, build tagged variants (std.sumtype SumType, std.variant Algebraic), and extend structs with alias this subtyping."
sources:
  - https://dlang.org/spec/struct.html
  - https://dlang.org/spec/class.html
  - https://dlang.org/phobos/std_sumtype.html
  - https://dlang.org/phobos/std_variant.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unions, tagged unions and alias this

Goal: represent variant data safely.

- `union U { int i; float f; ubyte[4] b; }` shares storage (overlapping fields); `@safe` code cannot access union fields whose pointers or references overlap other types. Unions may not have postblits, destructors or invariants.
- Prefer `std.sumtype.SumType!(int, string)` with `match!((int i) => ..., (string s) => ...)` (exhaustive at compile time).
- `std.variant.Variant` is a dynamic any-type; `Algebraic` is its tagged variant.
- `alias this`: `struct W { Inner i; alias i this; }` converts the struct implicitly to `i` and forwards undefined lookups to it (when `i` is a class or struct).
- Anonymous unions inside structs overlay fields: `union { int a; float b; }`.

Gotchas:
- `alias this` may name a `@property` function with no parameters; conversions and lookups then go through its return value.

Verify: unittest matching all `SumType` alternatives compiles; removing one fails to compile.

## Checked

Date 2026-11-02. Confirmed unions, anonymous unions, alias this, SumType and Variant (Struct spec, std.sumtype, std.variant). Removed the multiple alias this claim and the implementation-defined union read claim; added the union restrictions on postblits, destructors and invariants.

Method: documentation only; no commands were run.
