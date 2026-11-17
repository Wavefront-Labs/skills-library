---
id: computing-software.software-engineering.scheme-racket.struct-definition
name: struct-definition
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, struct-definition, racket-structs]
level: intro
status: docs-checked
description: "Define record types with struct, get constructor, predicate, accessors and mutators, and use struct-copy to update immutably."
sources:
  - https://docs.racket-lang.org/guide/define-struct.html
  - https://docs.racket-lang.org/reference/define-struct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining structs
**Goal:** declare data types.
```racket
(struct point (x y))
(define p (point 1 2))
(point-x p) (point? p)
(struct-copy point p [x 10])
```
- `struct` binds the constructor (named like the struct by default), a predicate `point?` and an accessor per field (`point-x`).
- Mutators `set-point-x!` are bound only for fields marked `#:mutable`; `#:mutable` as a struct option applies to all fields (giving it as both field option and struct option is a syntax error).
- An opaque struct instance prints like `#<point>`; add `#:transparent` to print it like a constructor call, show its fields and allow reflection (`struct?`, `struct-info`).
- `struct-copy` takes a struct id bound by `struct`, an instance and `[field-id expr]` clauses; it returns a new instance and leaves the original unchanged.
## Self-check
`(point-x (struct-copy point p [x 10]))` is `10` and `(point-x p)` is still `1`.

## Checked
2026-11-08. Confirmed against the Racket Guide "Structure Types" chapter and the Reference `struct` form: generated bindings, `#:mutable` as field and struct option and the syntax error when both are given, `#<posn>` printing, `#:transparent` printing and reflection, `struct-copy` syntax and behaviour.
Removed: "arity errors name the constructor" (not stated on the pages).
Method: documentation only; no commands were run.
