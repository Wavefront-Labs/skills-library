---
id: computing-software.software-engineering.haskell.list-comprehensions
name: list-comprehensions
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, list-comprehension, ranges, enumfrom, generators, parallelcomp, list-comprehensions, haskell-lists]
level: intro
status: docs-checked
description: "Write list comprehensions with generators, guards and lets, enumeration ranges including Double pitfalls, and the ParallelListComp extension."
sources: ["https://www.haskell.org/onlinereport/haskell2010/haskellch3.html", "https://www.haskell.org/onlinereport/haskell2010/haskellch9.html", "https://downloads.haskell.org/ghc/latest/docs/users_guide/exts/parallel_list_comprehensions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List comprehensions and ranges

**Goal:** express map/filter/product concisely and avoid range surprises.

```haskell
squares = [x * x | x <- [1..10], even x]                 -- generator + guard
pairs   = [(x, y) | x <- [1..3], y <- "ab"]              -- nested: x is the outer loop
pyth n  = [(a,b,c) | c <- [1..n], b <- [1..c], a <- [1..b], a*a + b*b == c*c]
withLet = [y | x <- [1..5], let y = x * 10, y > 20]
```
The report translates comprehensions through `concatMap`; generators are evaluated as nested, depth-first loops, so the
left-most generator is the outermost loop.

## Ranges
- `[n..m]`, `[n,n'..m]` (step), `[n..]` and `[n,n'..]` are `enumFromTo`, `enumFromThenTo`, `enumFrom`, `enumFromThen`.
  A descending range needs the second element: `[10,8..0]`. `['a'..'z']` works for characters.
- `[1..]` is an infinite list; take from it lazily.
- Floating ranges: for `Double` and `Float`, `[n..m]` runs up to `m + 1/2` and `[n,n'..m]` up to `m + (n'-n)/2`, so
  `[0.1,0.2..1.0]` can include elements past the limit by up to half a step, and the repeated addition accumulates
  error; prefer integer ranges scaled by a divisor.

## ParallelListComp
`{-# LANGUAGE ParallelListComp #-}` allows `[(x, y) | x <- xs | y <- ys]`: independent branches separated by `|` that
behave like `zip`, so the result has the length of the shortest branch.

## Gotchas
- A pattern in a generator that fails (`Just x <- xs`) silently skips the element.
- Nested comprehensions over large lists are quadratic; use a better data structure for lookups.
- Strings are `[Char]`, so comprehensions work on text, but a list of characters is slow for large text.

## Self-check
- [ ] `take 5 [x | x <- [1..], x `mod` 7 == 0]` returns `[7,14,21,28,35]`.
- [ ] No Double ranges used for counting loops.

## Checked

2026-11-08. Confirmed against the Haskell 2010 Report (section 3.10 arithmetic sequences, section 3.11 list comprehensions: nested depth-first evaluation, failed matches skipped, `concatMap` translation; Prelude `numericEnumFromTo` and `numericEnumFromThenTo` limits of `m + 1/2` and `m + (n'-n)/2`) and the GHC User's Guide ParallelListComp page (independent branches, zip behaviour, shortest branch). Removed: MonadComprehensions, the `Data.Map`, `Data.Set` and `Data.Text` advice, and the claim that `[x..y]` with `x > y` is empty (not shown for Double).
Method: documentation only; no commands were run.
