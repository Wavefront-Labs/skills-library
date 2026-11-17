---
id: computing-software.software-engineering.haskell.vector-package
name: vector-package
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, vector, unboxed-vector, mutable-vector, fusion, generate, modify-vector, primitive, vector-package, haskell-arrays]
level: practitioner
status: docs-checked
description: "Use Data.Vector and Data.Vector.Unboxed, construction (fromList, generate), mutable vectors in ST, and indexing costs."
sources: ["https://hackage.haskell.org/package//vector", "https://hackage.haskell.org/package//array"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vector

**Goal:** fast arrays with a list-like API. Package: `vector`.

```haskell
import qualified Data.Vector as V                 -- boxed, any element type
import qualified Data.Vector.Unboxed as U         -- unboxed, elements need an Unbox instance
import qualified Data.Vector.Unboxed.Mutable as UM
import Control.Monad.ST

v = U.fromList [1..10 :: Int]
U.sum (U.map (* 2) (U.filter even v))      -- sum of the doubled even elements
v U.! 3; v U.!? 99; U.length v
U.generate 5 (\i -> i * i)
U.accumulate (+) (U.replicate 3 0) (U.fromList [(0,1),(2,5)])
sieve n = runST $ do
  a <- UM.replicate (n + 1) True
  forM_ [2 .. n] $ \i -> do
    p <- UM.read a i
    when p $ forM_ [i*i, i*i+i .. n] $ \j -> UM.write a j False
  U.freeze a
```

## Facts
- `modify` applies a destructive operation, in place if safe and on a copy otherwise. `thaw`/`freeze` are O(n) copies; `unsafeThaw`/`unsafeFreeze` are O(1) and the original must not be used afterwards.
- `generate` and `unfoldrN` construct vectors from an index function or a seed.

## Gotchas
- `!` and `!?` (safe, returns `Maybe`) are O(1); `unsafeIndex` skips bounds checking.
- `snoc` is O(n); build with `generate` or `unfoldrN`.

## Self-check
- [ ] Numeric hot paths use Unboxed.
- [ ] Mutation confined to `runST` with the vector frozen at the boundary.

## Checked

2026-11-03. Confirmed against the vector Data.Vector.Unboxed page: indexing costs, modify, thaw/freeze/unsafe variants, generate, unfoldrN, snoc cost. Removed: slice, fusion, vector-algorithms and thunk claims.
Method: documentation only; no commands were run.
