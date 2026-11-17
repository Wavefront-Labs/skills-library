---
id: computing-software.software-engineering.haskell.data-list-functions
name: data-list-functions
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, data-list, sortby, sorton, groupby, nub, partition, isprefixof, zip, transpose, data-list-functions]
level: intro
status: docs-checked
description: "Use the Data.List API: sort, sortOn, group, nub, partition, isPrefixOf, intercalate, transpose, zip3 and unfoldr, and know the O(n^2) traps."
sources: ["https://www.haskell.org/onlinereport/haskell2010/", "https://hackage.haskell.org/package/base"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data.List essentials

**Goal:** reach for the right function in `Data.List` (module in `base`) instead of hand loops.

```haskell
import Data.List
import Data.Ord (comparing, Down(..))

sort [3,1,2]                         -- [1,2,3]; stable sort
sortOn snd [(1,'b'),(2,'a')]         -- sort by a key computed once per element
sortBy (comparing Down) [1,3,2]      -- descending
group (sort "mississippi")           -- ["iiii","m","pp","ssss"]; groups ADJACENT equals only
nub [1,2,1,3]                        -- [1,2,3]; O(n^2), needs Eq
partition even [1..6]                -- ([2,4,6],[1,3,5])
intercalate ", " ["a","b"]           -- "a, b"
transpose ["abc","de"]               -- ["ad","be","c"]
isPrefixOf "ab" "abc"; isInfixOf; isSuffixOf
splitAt 2 [1..5]; span even [2,4,5,6]; dropWhileEnd (== ' ') "hi  "
zip3, zipWith3, unzip3; lookup 2 [(1,"a"),(2,"b")]
unfoldr (\n -> if n > 5 then Nothing else Just (n, n + 1)) 1   -- [1..5]
```

## Traps
- `head`, `tail`, `last`, `init`, `!!`, `maximum`, `foldr1` are partial and the docs carry a WARNING on them; `head` and `tail`
  trigger the partiality warning that `-Wno-x-partial` silences. Use pattern matching, `!?` or `unsnoc`.
- `nub` is O(n^2); with an `Ord` instance the docs suggest `nubOrd` from the containers package.
- `group` does not merge non-adjacent equal elements; sort first.
- `(++)` takes time linear in its first list: associate it to the right; `foldl (++) []` is prone to quadratic slowdown.
- `sortOn f` is equivalent to `sortBy (comparing f)` but evaluates `f` once per element.

## Self-check
- [ ] Hoogle (hoogle.haskell.org) lookup of the type you need was tried before writing a helper.
- [ ] Partial functions replaced or guarded; `-Wall` is clean.

## Checked

2026-11-03. Confirmed against the base Data.List page: stable sort, sortOn evaluates the key once, nub is O(n^2) with the nubOrd pointer, partial-function warnings and -Wno-x-partial, (++) cost. Removed: version hedge and NonEmpty advice.
Method: documentation only; no commands were run.
