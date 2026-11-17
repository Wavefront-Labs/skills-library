---
id: computing-software.software-engineering.haskell.semigroup-and-monoid
name: semigroup-and-monoid
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, semigroup, monoid, mappend, mconcat, sum-product, semigroup-and-monoid]
level: practitioner
status: docs-checked
description: "Use Semigroup and Monoid instances, newtype wrappers like Sum and Any, foldMap and mconcat, and write lawful instances for your own types."
sources: ["https://hackage.haskell.org/package/base", "https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semigroup and Monoid

**Goal:** combine values associatively and fold structures with `foldMap`.

```haskell
import Data.Monoid
import Data.Semigroup

[1,2] <> [3]                          -- [1,2,3]
getSum (foldMap Sum [1..10])          -- 55
getAll (foldMap (All . even) [2,4])   -- True
mconcat ["a","b","c"]                 -- "abc"
Max 3 <> Max 5                        -- Max {getMax = 5}
Just [1] <> Nothing <> Just [2]       -- Just [1,2] (Maybe lifts a Semigroup)

newtype MaxLen = MaxLen Int deriving Show
instance Semigroup MaxLen where MaxLen a <> MaxLen b = MaxLen (max a b)
instance Monoid MaxLen where mempty = MaxLen 0
```

## Laws
- Semigroup: `(a <> b) <> c == a <> (b <> c)`.
- Monoid: `mempty <> x == x == x <> mempty`.
- `foldMap f` maps then combines with `<>`; the container decides association, so laws matter.

## Useful instances
`Ordering` (so `comparing fst <> comparing snd` sorts by two keys), functions `a -> b` when `b` is a
Semigroup, `Map` (`<>` is `union`, left-biased), `Endo` (function composition).

## Gotchas
- `Sum` and `Product` are newtypes; unwrap with `getSum`.
- `Map`'s `<>` is `union`, so values are not combined; use `Map.unionWith (<>)`.
- Semigroup became a superclass of Monoid in base-4.11.

## Self-check
- [ ] QuickCheck properties for associativity and identity on your instances.
- [ ] `sortBy (comparing a <> comparing b)` used for multi-key sorting.

## Checked

2026-11-03. Confirmed against base Data.Semigroup and Data.Monoid pages and the containers Data.Map page: Ordering and function instances, Map (<>) = union, Semigroup superclass of Monoid in base-4.11. Removed: tuple, Ap, Alt, First/Last, list-append and mappend-default claims.
Method: documentation only; no commands were run.
