---
id: computing-software.software-engineering.d.d-manifest-constants-and-anonymous-enums
name: d-manifest-constants-and-anonymous-enums
category: computing-software
field: software-engineering
product: d
tags: [d-manifest-constants-and-anonymous-enums, enums, manifest-constant, anonymous-enum, enum-constant, static-immutable, compile-time-constant, d]
level: practitioner
status: docs-checked
description: "Use enum for compile-time constants (enum x = 5; enum s = \"a\"), anonymous enums, and enum vs immutable vs static immutable."
sources:
  - https://dlang.org/spec/enum.html
  - https://dlang.org/spec/declaration.html
  - https://dlang.org/spec/template.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manifest constants and anonymous enums

Goal: pick the right constant kind.

- `enum pi = 3.14159;` is a manifest constant: it exists only at compile time (in the compiler's memory), is not an lvalue, and its initialiser is evaluated with CTFE. The `enum` storage class makes each declared identifier a manifest constant.
- `enum { A, B, C }` is an anonymous enum: the members are declared in the enclosing scope, no new type is created, and these are `int` constants 0, 1, 2.
- Anonymous enum members can have different types, taken from an explicit type, the base type, the initialiser or the previous member.
- In a template, `const size_t size = T.sizeof;` is located in the executable, while `enum size_t size = T.sizeof;` has no runtime location.
- Eponymous enum template: `enum bool within(alias v, T) = v <= T.max && v >= T.min;`.

Gotchas:
- Taking the address of a manifest constant is illegal.
- An initialiser for a non-local or static `immutable` must be evaluable at compile time.

Verify: a unittest that `pi` and `A, B, C` have the expected values.

## Checked
Checked 2026-11-03 against the D spec Enums (manifest constants, anonymous enums), Declarations (`enum` storage class), Type Qualifiers and Templates (eponymous templates) pages. Removed: the claim that an enum array allocates on every use, the `immutable x` remark and the `static immutable` storage claim (not stated there).

Method: documentation only; no commands were run.
