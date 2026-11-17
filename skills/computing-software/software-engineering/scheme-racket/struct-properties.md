---
id: computing-software.software-engineering.scheme-racket.struct-properties
name: struct-properties
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, struct-properties]
level: practitioner
status: docs-checked
description: "Customise Racket structs with #:property prop:procedure and #:methods gen:custom-write and gen:equal+hash."
sources:
  - https://docs.racket-lang.org/guide/define-struct.html
  - https://docs.racket-lang.org/reference/structures.html
  - https://docs.racket-lang.org/reference/Equality.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct properties and printing
**Goal:** customise struct semantics.
```racket
(struct adder (n) #:property prop:procedure (lambda (self x) (+ x (adder-n self))))
((adder 5) 1)   ; 6
(struct w (v) #:methods gen:custom-write
  [(define (write-proc s port mode) (fprintf port "<w ~a>" (w-v s)))])
```
- `#:property` associates a property and value with the structure type; `prop:procedure` lets an instance be called as a function, and the property value decides how the call is implemented.
- `#:methods` associates method definitions for a generic interface; `gen:custom-write` customises how an instance is displayed, and `gen:dict` lets instances act as dictionaries.
- `gen:equal+hash` lets `equal?` work without a transparent struct and takes three methods: the equality test (`equal-proc`), a hash code (`hash-proc`) and a secondary hash code (`hash2-proc`). The hash functions must give the same value for any two instances that `equal-proc` treats as equal.
## Self-check
`((adder 5) 1)` returns `6`.
## Checked
2026-11-08. Confirmed in the Guide "Defining Structure Types" page and the Reference Equality page: `#:property` with `prop:procedure`, `#:methods` with `gen:custom-write` and `gen:dict`, and the three `gen:equal+hash` methods and their consistency requirement. Removed: the claim that `prop:custom-write` is "the older direct property form" and any use of `prop:equal+hash`, which the cited pages do not document.
Method: documentation only; no commands were run.
