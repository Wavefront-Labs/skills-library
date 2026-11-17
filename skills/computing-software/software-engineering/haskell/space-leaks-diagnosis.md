---
id: computing-software.software-engineering.haskell.space-leaks-diagnosis
name: space-leaks-diagnosis
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, space-leak, thunk, heap-profile, retainer, rts-s, max-residency, space-leaks-diagnosis]
level: advanced
status: draft
description: "Detect thunk and retention space leaks using +RTS -s, heap profiling by cost centre, retainer and biography profiles, and the usual fixes."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/", "https://hackage.haskell.org/package//deepseq"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diagnosing space leaks

**Goal:** find why memory grows, then remove the retention or thunk chain.

## Step 1: confirm
Build with `-rtsopts`, run `./app +RTS -s`. Look at "maximum residency" and "total memory in use" versus real
live data. A steadily growing residency in a loop that should be constant indicates a leak.

## Step 2: profile the heap
```bash
ghc -O1 -prof -fprof-auto-top -rtsopts App.hs
./App +RTS -hc -i0.1      # by cost centre; writes App.hp
hp2ps -c App.hp           # produces App.ps
./App +RTS -hT            # by closure type, works WITHOUT -prof
```
Other breakdowns: `-hd` closure description, `-hy` type, `-hr` retainers, `-hb` biography (requires profiling).
Cabal: `cabal build --enable-profiling --profiling-detail=toplevel-functions`.

## Typical causes and fixes
- Lazy accumulator (`foldl`, lazy `modifyIORef`, lazy state in `State`): use `foldl'`, `modifyIORef'`,
  `Control.Monad.State.Strict`, bang patterns.
- Lazy `Map` values: use `Data.Map.Strict` and `insertWith`.
- Holding a reference to a list head while traversing it: restructure so the consumer owns the list, or stream.
- `Data.Text`/`ByteString` slices retaining a huge buffer: `T.copy` or `B.copy` to detach.
- Lazy IO (`getContents`) holding the whole file: use strict read or streaming.
- Unevaluated `where` bindings captured in closures.

## Gotchas
- Profiling can change optimisation (cost centres block inlining); confirm the leak exists unprofiled via `-hT`.
- `-hT` shows closure type names like `THUNK` and `:` but not source locations.
- The generational GC means "maximum residency" is only sampled at major collections.

## Self-check
- [ ] After the fix, the `-hT` graph is flat rather than rising.
- [ ] `+RTS -s` maximum residency is a small constant factor of live data.
