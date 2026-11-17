---
id: computing-software.software-engineering.scheme-racket.association-lists
name: association-lists
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, association-lists]
level: intro
status: docs-checked
description: "Look up key-value pairs in lists with assoc, assq, assv and remove or update immutably; prefer hashes for large data."
sources:
  - https://docs.racket-lang.org/guide/pairs.html
  - https://docs.racket-lang.org/reference/pairs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Association lists
**Goal:** use alists safely.
```racket
(define al '((a . 1) (b . 2)))
(assq 'b al)           ; '(b . 2)
(cdr (assq 'b al))     ; 2
(assoc "b" '(("b" . 1)) string=?)  ; custom equality in 3rd arg
```
- A miss returns `#f` rather than a pair, so check the result before taking `cdr`.
- `assoc` compares with `equal?` unless given an `is-equal?` procedure as its third argument.
## Self-check
`(assq 'z al)` returns `#f`.

## Checked

Date: 2026-11-02. Confirmed on Racket Reference Pairs and Lists (`assq`, `assoc v lst [is-equal?]` default `equal?`, result is the pair or `#f`). Removed: the O(n) claim and the statement that `(cdr #f)` errors, which that page does not state.

Method: documentation only; no commands were run.
