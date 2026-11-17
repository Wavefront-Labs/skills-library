---
id: computing-software.software-engineering.haskell.array-and-st-arrays
name: array-and-st-arrays
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, data-array, stuarray, iouarray, runstarray, runstuarray, ix, accumarray, ioref, stref, mutable-state, array-and-st-arrays]
level: advanced
status: docs-checked
description: "Use immutable Data.Array with accumArray, mutable STUArray/IOArray in ST, IORef/STRef with strict modify, and runST's rank-2 rule."
sources: ["https://hackage.haskell.org/package//vector", "https://hackage.haskell.org/package//array"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrays and mutable state

**Goal:** mutate safely and quickly inside pure code. Packages: `array`, base (`Data.IORef`, `Data.STRef`, `Control.Monad.ST`).

```haskell
import Data.Array
import Data.Array.ST (runSTUArray, newArray, readArray, writeArray)
import Data.Array.Unboxed (UArray)
import Data.STRef
import Control.Monad.ST
import Data.IORef

a = listArray (0, 4) [10,20,30,40,50] :: Array Int Int
a ! 2;  bounds a;  a // [(1, 99)]         -- (//) returns an updated array
accumArray (+) 0 (0, 2) [(0,1),(2,5),(0,3)] :: Array Int Int
grid = listArray ((0,0),(2,2)) [1..9] :: Array (Int,Int) Int     -- Ix gives tuple indices

counts :: Int -> UArray Int Int
counts n = runSTUArray $ do
  arr <- newArray (0, n) 0
  mapM_ (\i -> readArray arr i >>= writeArray arr i . (+1)) [0 .. n]
  pure arr

sumST xs = runST $ do { r <- newSTRef 0; mapM_ (\x -> modifySTRef' r (+ x)) xs; readSTRef r }
ref <- newIORef 0; modifyIORef' ref (+ 1); readIORef ref
atomicModifyIORef' ref (\n -> (n + 1, ()))
```

## Facts
- `Array` is immutable, non-strict and boxed; `UArray` has unboxed elements. `accumArray` is strict in each accumulation result, so accumulated arrays should not in general be recursive.
- `runST :: (forall s. ST s a) -> a`: the rank-2 type prevents the mutable reference escaping.
- Use `modifyIORef'` and `modifySTRef'`, the strict ones.

## Gotchas
- Use `atomicModifyIORef'` for atomic updates of an `IORef` from several threads.
- Indices missing from an association list have undefined (bottom) values.
- Repeated indices in an association list are undefined per Haskell 2010; GHC's implementation uses the last association.

## Self-check
- [ ] `runST` code type checks without annotation tricks (no `$` problems: use `runST $ do`).
- [ ] No `//` in a loop.

## Checked

2026-11-03. Confirmed against the array Data.Array and base Data.IORef, Data.STRef pages: non-strict boxed Array, accumArray strictness, undefined missing indices, repeated-index behaviour, strict modify functions, atomicModifyIORef'. Removed: bounds-check, unsafeRead and library-preference claims.
Method: documentation only; no commands were run.
