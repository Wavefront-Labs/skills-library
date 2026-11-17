---
id: computing-software.software-engineering.haskell.folds-and-higher-order-functions
name: folds-and-higher-order-functions
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, foldr, foldl-prime, foldl, map, filter, zipwith, scanl, higher-order, folds-and-higher-order-functions]
level: intro
status: draft
description: "Use map, filter, foldr, foldl', scanl and zipWith correctly, and choose between foldr and foldl' for laziness and stack safety."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Folds, map and filter

**Goal:** pick the right fold and avoid stack and thunk blowups.

```haskell
import Data.List (foldl')

sum' :: [Int] -> Int
sum' = foldl' (+) 0                         -- strict left fold: constant space

anyBig :: [Int] -> Bool
anyBig = foldr (\x acc -> x > 100 || acc) False   -- foldr short-circuits, works on infinite lists

running = scanl (+) 0 [1,2,3]               -- [0,1,3,6]
pairsUp = zipWith (+) [1,2,3] [10,20,30]    -- [11,22,33]
```

## Choosing
- `foldr f z`: right-nested; lazy when `f` is lazy in its second argument. Good for building lists
  (`foldr (:) []`) and short-circuiting.
- `foldl' f z` from `Data.List`: forces the accumulator to WHNF at each step. Use for sums, counts, maps.
  Recent base versions also export it from Prelude (unconfirmed which); import it explicitly to be safe.
- `foldl` (lazy) builds a chain of thunks; GHC `-O` often repairs it via strictness analysis, but do not rely on it.
- `foldr1`, `foldl1`, `maximum`, `minimum` are partial on empty lists.
- `Foldable` generalises these to `Maybe`, `Map`, `Set`, `Seq`.

## Gotchas
- WHNF only: `foldl' (\(a,b) x -> (a+x,b+1)) (0,0)` still builds thunks inside the tuple; use bang patterns or a strict data type.
- A strict-combining `foldr` over a huge list uses stack proportional to the length; the stack is limited by the RTS `-K` option.

## Self-check
- [ ] `./prog +RTS -s` shows low maximum residency for the fold.
- [ ] Empty-list case explicitly handled for partial folds.
