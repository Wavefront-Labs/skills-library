---
id: computing-software.software-engineering.scheme-racket.struct-options
name: struct-options
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, struct-options]
level: practitioner
status: docs-checked
description: "Use #:transparent, #:mutable, #:prefab, #:guard, #:auto and sub-structs; transparent structs compare with equal?."
sources:
  - https://docs.racket-lang.org/guide/define-struct.html
  - https://docs.racket-lang.org/reference/define-struct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct options and inheritance
**Goal:** configure struct behaviour.
```racket
(struct animal (name) #:transparent)
(struct dog animal (breed) #:transparent)
(equal? (dog "a" "b") (dog "a" "b"))   ; #t
(struct celsius (temp)
  #:guard (lambda (temp name)
            (unless (real? temp) (error name "bad temperature"))
            temp))
```
- `equal?` recurs on the fields of a transparent struct; for an opaque struct it defaults to instance identity. To compare without making the type transparent, implement `gen:equal+hash` via `#:methods`.
- `#:prefab` uses a pre-existing, globally shared struct type, inherently transparent; instances print as `#s(...)` and the reader can create them. Combining `#:prefab` with `#:transparent`, `#:inspector`, `#:guard`, `#:property`, `#:sealed`, `#:authentic` or `#:methods` is a syntax error, and a prefab supertype must be prefab.
- `#:guard` takes a procedure receiving the field values followed by the struct type name, and must return the field values (a sub-struct guard receives its own fields plus the type name).
- An `#:auto` field is not accepted by the constructor; it takes the `#:auto-value` (default `#f`). All fields after an `#:auto` field must also be `#:auto`. A mutator is bound only if `#:mutable` is also given.
- A sub-struct constructor takes the parent fields first, then its own.
## Self-check
`(equal? (animal "a") (animal "a"))` is `#t` only because of `#:transparent`.

## Checked
2026-11-08. Confirmed against the Racket Guide "Structure Types" chapter and the Reference `struct` form: `equal?` behaviour for transparent and opaque structs, `gen:equal+hash`, prefab rules and syntax errors, `#:guard` argument shape, `#:auto` and `#:auto-value` rules, parent-fields-first constructor.
Removed: the unconditional claim that opaque structs compare by `eq?` (the docs say instance identity by default, which is replaced above) and the bare `#:guard` example that used a non-number check.
Method: documentation only; no commands were run.
