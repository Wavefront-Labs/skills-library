---
id: computing-software.software-engineering.haskell.foldable-and-traversable
name: foldable-and-traversable
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, foldable, traversable, traverse, sequencea, mapm, foldmap, foldable-and-traversable]
level: practitioner
status: docs-checked
description: "Use Foldable (toList, null, length, foldMap) and Traversable (traverse, sequenceA, mapM) over Maybe, lists, Map and trees."
sources: ["https://hackage.haskell.org/package/base", "https://www.haskell.org/onlinereport/haskell2010/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Foldable and Traversable

**Goal:** write functions over any container and run effectful maps.

```haskell
import Data.Foldable (for_, traverse_, toList, foldl', foldrM)
import Data.Traversable (for)

length (Just 3)                 -- 1
sum (Map.fromList [(1,10),(2,20)])    -- 30: folds over values
traverse (\x -> if x > 0 then Just x else Nothing) [1,2,3]   -- Just [1,2,3]
traverse (\x -> if x > 0 then Just x else Nothing) [1,0]     -- Nothing
sequenceA [Just 1, Just 2]      -- Just [1,2]
for_ [1,2,3] print              -- run an action per element, discard results
mapM_ print xs                  -- same, older name
r <- for items $ \i -> fetch i  -- keep results
```

## Core methods
- `Foldable`: `foldMap` or `foldr` (MINIMAL), plus `toList`, `null`, `length`, `elem`, `sum`, `maximum`, `foldl'`.
- `Traversable`: `traverse` or `sequenceA` (MINIMAL), requires `Functor` and `Foldable`.
- `traverse` with `Either e` stops at the first `Left`; with `Maybe` at the first `Nothing`.

## Gotchas
- For effects only, use `traverse_`/`for_`/`mapM_` rather than `traverse`/`mapM`, which also build a result structure.

## Self-check
- [ ] Functions over containers take `Foldable t => t a`, not `[a]`, unless lists are required.
- [ ] `traverse_`/`for_` used when results are discarded.

## Checked

2026-11-03. Confirmed against base Data.Foldable and Data.Traversable pages: minimal definitions, for_, traverse_, foldrM, sequenceA. Removed: deriving section, tuple-fold, tail-recursion, State and Map-order claims, validation claim.
Method: documentation only; no commands were run.
