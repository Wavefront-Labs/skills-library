---
id: computing-software.software-engineering.scheme-racket.list-operations
name: list-operations
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, list-operations, racket-pairs-lists]
level: intro
status: docs-checked
description: "Build and traverse lists with cons, car/cdr, first/rest, append, reverse, length, list-ref, take, drop and remove-duplicates."
sources:
  - https://docs.racket-lang.org/guide/pairs.html
  - https://docs.racket-lang.org/reference/pairs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List operations
**Goal:** everyday list work.
```racket
(require racket/list)
(first '(1 2 3)) (rest '(1 2 3)) (take '(1 2 3) 2) (drop '(1 2 3) 2)
(append '(1) '(2 3)) (remove-duplicates '(1 1 2)) (range 5)
(filter-map (lambda (x) (and (even? x) (* x x))) '(1 2 3 4))
```
- `first`/`rest` are `car`/`cdr` restricted to non-empty lists; `car`/`cdr` take any pair.
- `take` raises `exn:fail:contract` when the list has fewer than `pos` elements; `drop` is like `list-tail`.
- `remove-duplicates` keeps the first of each duplicate in the original order, using `equal?` unless you pass `same?` or `#:key`.
- `filter-map` omits elements for which `proc` returns `#f`, without building an intermediate list.
- `length` takes time proportional to the list length, `list-ref` and `take` time proportional to `pos`.
## Self-check
`(take '(1 2) 3)` raises an error rather than returning short.

## Checked
2026-11-08. Confirmed on the Racket Reference pairs page (4.10 and the racket/list section): `first`, `rest`, `car`, `cdr`, `take` error and cost, `drop`, `remove-duplicates` semantics, `filter-map`, `range`, `length` and `list-ref` cost statements, `append`, `reverse`. Removed the generic "use vectors for random access" advice, which the pages do not state.
Method: documentation only; no commands were run.
