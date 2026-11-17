---
id: computing-software.software-engineering.clojure.clojure-core-reducers-fold-and-parallelism
name: clojure-core-reducers-fold-and-parallelism
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, reducers, fold, fork-join, parallelism, pmap, claypoole, executors, data-parallel, performance, performance-concurrency-reducers]
level: advanced
status: docs-checked
description: "Use clojure.core.reducers/fold for parallel reduce-combine over vectors and maps, pmap/pcalls caveats, and bounded thread pools for CPU- or IO-bound work."
sources: ["https://clojure.org/reference/reducers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parallel processing

**Goal:** use all cores safely.

```clojure
(require '[clojure.core.reducers :as r])
(r/fold + (r/map inc (vec (range 1e6))))               ; parallel over vectors/maps via fork/join
(r/fold 512 + (fn [acc x] (+ acc x)) coll)             ; batch size, combinef, reducef
(into [] (r/filter even? v))                           ; reducers are eager and non-lazy
(pmap f coll)                                          ; lazy, window of cores+2, per-element overhead
(pcalls f1 f2)  (pvalues expr1 expr2)
```
- `fold` needs an associative combine function with an identity (calling `(f)` with no args returns identity).
  Works in parallel only on vectors and hash maps; other collections fall back to sequential reduce.
- Reducers are not lazy; use them for large CPU-bound reductions.
- `pmap` is only worthwhile when each task takes much longer than the thread handoff; chunk the input first.
- For IO-bound parallelism use an explicit bounded JDK thread pool (see the java.util.concurrent documentation), or core.async `pipeline-blocking`.
- Libraries: claypoole offers prioritised bounded pools and `pmap` variants (unconfirmed API details).
- Beware shared mutable state; keep tasks pure.

## Failure modes
- Non-associative combine functions give different results run to run.
- Unbounded thread creation via `future` in a loop.

## Self-check
Compare `reduce` and `fold` on a 10M-element vector with `time`.

## Checked
2026-11-02. Confirmed: clojure.org/reference/reducers and the clojure.core API page: fold semantics (default batch size 512, combinef with identity, parallel only on vectors and maps with sequential fallback), r/map, r/filter, into with reducers, pmap, pcalls, pvalues. Removed: the order-guarantee claim and the ExecutorService code detail (not in the pages read).
Method: documentation only; no commands were run.
