---
id: computing-software.software-engineering.scheme-racket.fold-map-filter
name: fold-map-filter
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, fold-map-filter, racket-higher-order]
level: intro
status: docs-checked
description: "Transform lists with map, filter, foldl, foldr, andmap, ormap and for-each; know foldl argument order."
sources:
  - https://docs.racket-lang.org/reference/pairs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# map, filter, foldl and foldr
**Goal:** apply functions over lists.
```racket
(map + '(1 2) '(10 20))        ; '(11 22)
(foldl cons '() '(1 2 3))      ; '(3 2 1)   fn gets (elem acc)
(foldr cons '() '(1 2 3))      ; '(1 2 3)
(filter odd? '(1 2 3))
(andmap even? '(2 4)) (ormap odd? '(2 4))
```
- `map` with several lists requires the same number of elements in every list, and `proc` must accept that many arguments.
- `foldl` calls `proc` with the element(s) first and the accumulator last (`n` lists means `n+1` arguments); it runs in constant space, whereas `foldr` uses space proportional to the list length.
- `andmap` on empty lists returns `#t`, `ormap` returns `#f`; both stop at the first deciding result.
- `for-each` is like `map` but only for effect and returns void.
## Self-check
`(foldl - 0 '(1 2 3))` is `2` (3-(2-(1-0))).

## Checked
2026-11-08. Confirmed on the Racket Reference pairs page (section 4.10.3 List Iteration): `map` same-length rule, `andmap`/`ormap` short-circuit and empty-list results, `for-each`, `foldl` argument order and constant space, `foldr` linear space, and the `foldl cons` / `foldr cons` examples. Removed the claim that `foldl` is "tail-recursive" (the page states constant space instead) and the Guide for page as a source (it does not cover these functions). `filter` is listed on the same page with signature `(filter pred lst)`.
Method: documentation only; no commands were run.
