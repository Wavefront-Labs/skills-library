---
id: computing-software.software-engineering.scheme-racket.data-contracts
name: data-contracts
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, data-contracts]
level: practitioner
status: docs-checked
description: "Describe data shapes with contracts: and/c, or/c, listof, struct/c, and plain predicates, and how contracts on mutable data wrap values."
sources:
  - https://docs.racket-lang.org/reference/contracts.html
  - https://docs.racket-lang.org/reference/data-structure-contracts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data contracts: listof, struct/c, flat predicates
**Goal:** describe data shapes.
```racket
(require racket/contract)   ; not provided by racket/base
(define pos-int/c (and/c exact-integer? positive?))
(define/contract xs (listof pos-int/c) '(1 2 3))
(struct point (x y))
(struct/c point real? real?)
(or/c string? #f)
```
- Any arity-1 procedure is a contract (a predicate); symbols, booleans, strings, numbers, regexps and similar values also act as contracts that recognize themselves.
- `(and/c contract ...)` accepts values that satisfy all contracts, checked left to right. `(or/c contract ...)` accepts values accepted by any one; it checks flat contracts first and moves non-flat ones to the end.
- `(listof c)` recognizes a list whose every element matches `c`. When applied to a value the result is not necessarily `eq?` to the input.
- `(struct/c struct-id contract-expr ...)` recognizes instances of the struct type whose field values match; immutable fields need flat or chaperone contracts, and it is flat only if all fields are immutable with flat contracts.
- Higher-order contracts on mutable data (vectors, boxes, hash tables) return a chaperone or impersonator of the input, so the result is not `eq?` to it.
## Self-check
`(contract (listof integer?) '(1 a) 'pos 'neg)` raises a violation blaming `pos`, because `pos` supplied the bad value.

## Checked
2026-11-08. Read in full: Racket Reference 8.1 Data-structure Contracts entries for `or/c`, `and/c`, `listof` and `struct/c`, plus the Contracts overview page (reference/contracts.html, whole page). The data-structure page was read at those entries and the vector/box/hash not-`eq?` sentences, not end to end. Removed the unsupported advice that `listof` "checks the whole list on each crossing; prefer checking once at the boundary" (the page only says the result is not necessarily `eq?`). Added the `racket/contract` requirement and a missing `struct` definition for the `struct/c` example. The self-check follows the page's documented `contract` example (the value-supplying party, `pos`, is blamed).
Method: documentation only; no commands were run.
