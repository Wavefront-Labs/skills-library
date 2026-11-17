---
id: computing-software.software-engineering.haskell.parallel-strategies-par
name: parallel-strategies-par
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, parallel, strategies, par, pseq, parmap, rpar, rseq, eval-monad, sparks, spark-fizzled, parallel-strategies-par, haskell-parallel]
level: advanced
status: draft
description: "Express pure parallelism with the parallel package: parMap, Strategies, rdeepseq, Eval monad, sparks, and reading spark statistics."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/", "https://hackage.haskell.org/package//parallel"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parallel strategies

**Goal:** speed up pure code over multiple cores. Package: `parallel`.

```haskell
import Control.Parallel.Strategies
import Control.DeepSeq (NFData)

results = map expensive xs `using` parList rdeepseq        -- evaluate list elements in parallel
ys = parMap rdeepseq f xs
chunked = map f xs `using` parListChunk 100 rdeepseq        -- fewer, larger sparks
pair = runEval $ do
  a <- rpar (fib 30)                    -- spark: may run in parallel
  b <- rseq (fib 29)                    -- evaluate here
  _ <- rseq a
  return (a, b)
```
Build and run:
```bash
ghc -O2 -threaded -rtsopts -eventlog Par.hs
./Par +RTS -N4 -s -l          # -s prints SPARKS: n (converted, overflowed, dud, GC'd, fizzled)
```
Use ThreadScope on the `.eventlog` to see core utilisation.

## Rules
- A spark is a hint; the RTS runs it if a core is idle. `rpar`/`par` do not force anything by themselves beyond WHNF of the sparked thunk, so use `rdeepseq` for structures.
- Granularity: sparks should do enough work (microseconds of overhead each); chunk lists.
- Determinism: results never depend on parallel schedule (pure), only performance.
- `-N` sets capabilities; `-qg`/`-A64m` (larger allocation area) often help parallel GC.

## Gotchas
- Fizzled sparks (already evaluated by someone else) and dud sparks (already values) indicate wasted work.
- `-threaded` without `-N` gives one capability.
- Lazy evaluation can hide sharing: sparked work may be forced earlier by the main thread (fizzle).
- Parallel GC hurts small heaps; test `-qn2` or `-qg`.

## Self-check
- [ ] Speed-up measured against `+RTS -N1`.
- [ ] Spark summary shows mostly converted, few fizzled/GC'd.
