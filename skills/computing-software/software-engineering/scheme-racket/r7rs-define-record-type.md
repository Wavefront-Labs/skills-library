---
id: computing-software.software-engineering.scheme-racket.r7rs-define-record-type
name: r7rs-define-record-type
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, r7rs-define-record-type, r7rs-small]
level: intro
status: docs-checked
description: "R7RS-small define-record-type: constructor spec, predicate, accessors and modifiers; unlisted fields start unspecified."
sources:
  - https://small.r7rs.org/attachment/r7rs.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R7RS define-record-type
**Goal:** records in portable code.
```scheme
(define-record-type point (make-point x y) point? (x point-x set-point-x!) (y point-y))
```
- The form is `(define-record-type name constructor pred field ...)`. The constructor is `(constructor-name field-name ...)`; each field is `(field-name accessor)` or `(field-name accessor modifier)`.
- Fields listed in the constructor take its arguments as initial values; the initial values of all other fields are unspecified.
- It is an error for a field name to appear in the constructor but not as a field, or for a field name, accessor or modifier name to repeat.
- The form is generative: each use creates a new record type distinct from all existing types.
- It is an error to pass an accessor or modifier a value that is not a record of that type.
## Self-check
`(point-x (make-point 1 2))` is `1`.
## Checked
2026-11-08. Confirmed in the R7RS-small report, section 5.5 (Record-type definitions): syntax, constructor and field rules, generativity and the error conditions. Removed: the claim about `srfi/9` in Racket (not covered by the cited sources) and the "uninitialised" wording (report says "unspecified").
Method: documentation only; no commands were run.
