---
id: computing-software.software-engineering.haskell.data-map-and-set
name: data-map-and-set
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, data-map, data-set, map-strict, insertwith, unionwith, alter, foldrwithkey, balanced-tree, data-map-and-set, haskell-containers]
level: practitioner
status: docs-checked
description: "Use Data.Map.Strict and Data.Set: fromList, insertWith, alter, adjust, unionWith, lookup, foldrWithKey, toAscList, complexity and strict vs lazy."
sources: ["https://hackage.haskell.org/package//containers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data.Map and Data.Set

**Goal:** use ordered maps and sets (balanced trees, keys need `Ord`). Package: `containers`.

```haskell
import qualified Data.Map.Strict as M
import qualified Data.Set as S

m  = M.fromList [(1,"a"),(2,"b")]
M.lookup 1 m                          -- Just "a"
M.findWithDefault "?" 9 m
M.insertWith (++) 1 "z" m             -- f new old: combine on collision
M.alter (fmap (++ "!")) 2 m           -- insert/update/delete by function
M.adjust (++ "!") 2 m; M.delete 1 m; M.member 1 m
M.unionWith (+) m1 m2                 -- combine values; M.union is left-biased
M.foldrWithKey (\k v acc -> ...) z m
M.toList m                            -- ascending by key
M.fromListWith (+) [(w, 1 :: Int) | w <- words txt]    -- word count
S.fromList [3,1,2]; S.member 2 s; S.union a b; S.difference a b; S.toList s
M.keysSet m; M.restrictKeys m s; M.withoutKeys m s
```

## Facts
- Operations are O(log n); `size` is O(1); `fromList` O(n log n); `fromAscList` O(n) for sorted input.
- Import `Data.Map.Strict` for accumulators; `Data.Map.Lazy` (the plain `Data.Map`) stores unevaluated thunks as values.
- `M.!` throws on missing keys; use `M.!?` or `lookup`.
- `foldr'`/`foldl'` on maps for strict folds.

## Gotchas
- Always import qualified (`Prelude` clashes: `filter`, `map`, `lookup`, `null`).
- The `Ord` instance on keys is expected to be lawful and define a total order.
- `M.insertWith f k new` calls `f new old`, order matters for `(++)`.
- If you do not need ordering and do not handle untrusted keys, the docs suggest `Data.HashMap.Strict` from `unordered-containers`; for `Int` keys they suggest `Data.IntMap.Strict`.

## Self-check
- [ ] Counting loops use `M.insertWith (+)` from the Strict module.
- [ ] No partial `M.!` outside tests.

## Checked

2026-11-03. Confirmed against the containers Data.Map.Strict, Data.Map and Data.Set pages: function names, complexities, strict vs lazy values, Ord requirement, left-biased union, insertWith argument order. Removed: NaN corruption claim, unsourced HashMap speed claim.
Method: documentation only; no commands were run.
