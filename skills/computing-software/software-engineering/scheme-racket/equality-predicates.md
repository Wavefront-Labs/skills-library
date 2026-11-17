---
id: computing-software.software-engineering.scheme-racket.equality-predicates
name: equality-predicates
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, equality-predicates]
level: practitioner
status: docs-checked
description: "Choose between eq?, eqv?, equal? and = in Racket, and which comparison each hash table constructor uses."
sources:
  - https://docs.racket-lang.org/reference/Equality.html
  - https://docs.racket-lang.org/reference/generic-numbers.html
  - https://docs.racket-lang.org/reference/hashtables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# eq?, eqv?, equal? and =
**Goal:** compare values correctly.
- `eq?` is true when two values refer to the same object. As a special case among numbers, two fixnums that are `=` are `eq?`. Examples from the Reference: `(eq? 'yes 'yes)` and `(eq? (* 6 7) 42)` are `#t`; `(eq? (expt 2 100) (expt 2 100))`, `(eq? 2 2.0)` and `(eq? (make-string 3 #\z) (make-string 3 #\z))` are `#f`.
- `eqv?` differs from `eq?` only for numbers: they must have the same exactness and precision and be equal (`(eqv? 2 2.0)` is `#f`, `(eqv? (expt 2 100) (expt 2 100))` is `#t`). The Reference lightly discourages `eqv?` in favour of `equal?`.
- `equal?` is eqv? unless specified otherwise for a datatype; it recurses into strings, byte strings, pairs, mutable pairs, vectors, boxes, hash tables and inspectable structures. The Reference says `equal?` is preferred for most uses.
- `=` takes `number?` arguments and is numeric: `(= 1 1.0)` is `#t`, and `+nan.0` is not `=` to itself.
- Hash tables: `make-hash` compares keys with `equal?`, `make-hasheq` with `eq?`, `make-hasheqv` with `eqv?` (and `make-hashalw` with `equal-always?`).
## Self-check
Compare `(eq? (make-string 3 #\z) (make-string 3 #\z))` (`#f`), `(equal? (make-string 3 #\z) (make-string 3 #\z))` (`#t`) and `(eqv? 2 2.0)` (`#f`).

## Checked
2026-11-08. Read: Racket Reference 4.1 Equality (reference/Equality.html) from the `equal?` entry through the `eq?` examples (about lines 80-195 of the stripped page); the rest of the page (hash codes) was searched, not read. From reference/generic-numbers.html read the `=` entry only; from reference/hashtables.html read the `make-hash`, `make-hasheq`, `make-hasheqv`, `make-hashalw` entries. Replaced the self-check `(eq? "a" "a")`, whose result the pages do not state, with a `make-string` example that they do. Replaced "transparent structs" with the page's term "inspectable structures". Removed the unsourced claim that `eq?` is "fine for small ints" in favour of the page's fixnum sentence, and swapped the unavailable reference/equality.html and reference/hashes.html URLs for the real pages.
Method: documentation only; no commands were run.
