---
id: computing-software.software-engineering.d.d-struct-basics-and-initialization
name: d-struct-basics-and-initialization
category: computing-software
field: software-engineering
product: d
tags: [d-struct-basics-and-initialization, structs-and-unions, struct, struct-initializer, value-semantics, default-init, d]
level: intro
status: docs-checked
description: "Define D structs: field defaults, struct literals, constructors, @disable this, = void, align, and value semantics."
sources:
  - https://dlang.org/spec/struct.html
  - https://dlang.org/spec/attribute.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct declaration, initialisers and value semantics

Goal: use structs as value types.

- `struct S { int a = 1; string n; }`; `S s;` uses defaults; the struct literal `S(2, "x")` takes positional or named arguments (`S(n: "x", a: 2)`); unassigned fields get their default initialisers. A `{ 1 }` initialiser is an error once the struct has a constructor.
- A default (no-parameter) constructor is not allowed on structs; a constructor with arguments is. A static `opCall` disables struct literal syntax, so prefer a factory function.
- Assignment copies the struct.
- `@disable this();` forbids default construction; `@disable this(this);` forbids copying (move-only types).
- `S v = void;` leaves the variable uninitialised.
- Field layout follows lexical order with padding inserted to align fields; control alignment with the `align(N)` attribute.

Gotchas:
- Returning a local struct by value can use NRVO, in which case no copy constructor is called.
- Struct member functions are not virtual; `alias this` gives implicit conversion to a member.

Verify: unittest comparing `S.init` to the literal defaults.

## Checked
Checked 2026-11-03 against the D spec Structs and Unions page and the Attributes page (`align`). Confirmed: struct literals with positional and named arguments, no default constructor, `@disable this();`, `= void`, disabled postblit, NRVO, non-virtual struct members, `alias this`. Removed: the `pragma(pack)` remark, the `ref this` remark and the slice-copy remark (not on those pages).

Method: documentation only; no commands were run.
