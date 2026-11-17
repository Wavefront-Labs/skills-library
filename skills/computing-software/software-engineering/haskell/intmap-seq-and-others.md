---
id: computing-software.software-engineering.haskell.intmap-seq-and-others
name: intmap-seq-and-others
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, intmap, data-sequence, seq, data-tree, intset, dlist, queue, deque, graph, intmap-seq-and-others]
level: practitioner
status: docs-checked
description: "Pick IntMap for Int keys, Data.Sequence for deques and indexed access, and Data.Tree and Data.Graph for trees and graphs."
sources: ["https://hackage.haskell.org/package//containers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IntMap, Seq and friends

**Goal:** choose the specialised structure from `containers` that matches the access pattern.

```haskell
import qualified Data.IntMap.Strict as IM
import qualified Data.Sequence as Seq
import Data.Sequence (Seq, (|>), (<|), ViewL(..), viewl)
import Data.Tree (Tree(..), flatten, drawTree)
import Data.Graph (graphFromEdges, topSort, stronglyConnComp)

IM.fromListWith (+) [(1, 2), (1, 3)]      -- Int keys; the Map docs recommend IntMap for Int keys
q = Seq.empty |> 1 |> 2 |> 3               -- O(1) at both ends
case viewl q of x :< rest -> ...; EmptyL -> ...
Seq.index q 1; Seq.update 1 9 q; Seq.length q     -- O(log(min(i,n-i))) indexing
drawTree (fmap show (Node 1 [Node 2 [], Node 3 []]))
```
Also pattern synonyms `Empty`, `:<|`, `:|>` on `Seq` give list-like matching.

## Guide
- `[a]`: stack/stream. `Seq a`: queue, deque, sliding window, random access. `Map k v`: key lookup.
  `IntMap`: Int keys, `Set`: membership.
- `Data.Graph`: `stronglyConnComp` for SCCs and dependency orders; `topSort`.
- `Data.Map` split/lookupMin/lookupLE give ordered-range queries; `Data.Map.Merge.Strict` for custom merges.

## Gotchas
- `Seq` is always finite and strict in its length, unlike a list.

## Self-check
- [ ] Queue/deque code uses Seq, not list appends.
- [ ] Benchmarked Map Int vs IntMap before switching.

## Checked

2026-11-03. Confirmed against containers Data.Sequence, Data.IntMap.Strict, Data.Tree and Data.Graph pages: O(1) ends, index cost, pattern synonyms, fromListWith, graph functions. Removed: DList and NonEmpty advice, lazy-elements claim, IntSet claim, list-queue claim.
Method: documentation only; no commands were run.
