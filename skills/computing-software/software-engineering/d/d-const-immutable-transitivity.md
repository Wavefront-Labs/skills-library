---
id: computing-software.software-engineering.d.d-const-immutable-transitivity
name: d-const-immutable-transitivity
category: computing-software
field: software-engineering
product: d
tags: [d-const-immutable-transitivity, const-immutable, const, immutable, transitive-const, const-member-function, qualifiers, immutable-string, d]
level: practitioner
status: docs-checked
description: "Apply const (read-only view) and immutable (never changes) with transitive depth, immutable strings, const member functions and casting rules."
sources:
  - https://dlang.org/spec/const3.html
  - https://dlang.org/phobos/std_exception.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# const vs immutable and transitive qualifiers

Goal: use D's deep const correctly.

- `const(T)`: you cannot modify through this reference, but others may. `immutable(T)`: data never changes by anyone.
- Both are transitive: data reachable through the reference is also const/immutable; `const(char)[]` is a slice whose elements are read-only but which can be reassigned; `const char[]` applies to the whole.
- Head vs deep: `const(char)[] s` (head mutable), `const char[] s` (all const).
- Conversions: mutable -> const ok; immutable -> const ok; mutable -> immutable only if the expression is unique (spec: Unique Expressions), otherwise `std.exception.assumeUnique`.
- Member functions: `int get() const`, `immutable`, `shared`, `inout`; `const` on a function applies to `this`.
- Making copies: `.idup`, `.dup`, `std.exception.assumeUnique(arr)`.

Gotchas:
- Strings are `immutable(char)[]`; `char[]` literal needs `.dup`.

Verify: `static assert(!__traits(compiles, {const int x; x = 2;}));`

## Checked

Date 2026-11-02. Confirmed const and immutable transitivity, conversions and unique expressions (Immutable Storage Class / const spec) and assumeUnique. Removed the implicit-sharing and shared-cast claims.

Method: documentation only; no commands were run.
