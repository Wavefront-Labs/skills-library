---
id: computing-software.software-engineering.scheme-racket.generic-interfaces
name: generic-interfaces
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, generic-interfaces]
level: practitioner
status: docs-checked
description: "Define polymorphic struct methods with racket/generic: define-generics, #:methods, and built-in interfaces such as gen:equal+hash and gen:custom-write."
sources:
  - https://docs.racket-lang.org/reference/struct-generics.html
  - https://docs.racket-lang.org/reference/structures.html
  - https://docs.racket-lang.org/guide/define-struct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# racket/generic interfaces
**Goal:** polymorphism for structs.
```racket
(require racket/generic)
(define-generics shape (area shape))
(struct sq (s) #:methods gen:shape [(define (area x) (* (sq-s x) (sq-s x)))])
(area (sq 3))   ; 9
```
- `racket/generic` provides `define-generics`; generic functions are defined by it, and a structure type supplies method implementations with `#:methods`.
- `define-generics id` binds `gen:id` (static information about the interface) and also an `id?` predicate and an `id/c` contract combinator.
- Optional `#:defaults`, `#:fast-defaults` and `#:fallbacks` supply implementations for non-struct values or for missing methods.
- Built-in generic interfaces named in the manuals: `gen:equal+hash`, `gen:custom-write`, `gen:dict`, `gen:stream`.
## Self-check
Implement a second struct with `#:methods gen:shape` and call `area` on both.
## Checked
2026-11-08. Confirmed on the Reference racket/generic page: `define-generics`, `#:methods`, `gen:id`/`id?`/`id/c`, and the `#:defaults`, `#:fast-defaults` and `#:fallbacks` options; `gen:equal+hash` (Equality page), `gen:custom-write` and `gen:dict` (Guide struct page), `gen:stream` (Streams page). Removed: nothing unsupported remained after rewording "generic functions are named in the form".
Method: documentation only; no commands were run.
