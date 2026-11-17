---
id: computing-software.software-engineering.clojure.seqs-and-lazy-sequences
name: seqs-and-lazy-sequences
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, seq, lazy-seq, map, filter, take, doall, dorun, realized, chunked-seq, iterate, lazy, seq-abstraction-lazy]
level: practitioner
status: docs-checked
description: "Use the seq abstraction and lazy sequences correctly: first/rest/next, laziness, doall/dorun/run!, infinite seqs, and the doall memory trade-off."
sources: ["https://clojure.org/reference/sequences", "https://clojure.org/reference/lazy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sequences and laziness

**Goal:** treat collections uniformly through `seq` and control when lazy work happens.

## Core
```clojure
(seq [])        ;=> nil (so (when (seq xs) ...) is the idiom for "non-empty")
(first xs) (rest xs) (next xs)   ; rest returns a logical seq for which seq is nil at the end; next is (seq (rest xs))
(take 5 (iterate #(* 2 %) 1))    ; infinite seq, only 5 realised
(lazy-seq (cons x (my-seq ...))) ; build your own
(doall (map f xs))  (dorun (map f xs))   ; force realisation (doall keeps results, dorun discards)
```
- Most sequence library functions are lazy: they return seqs incrementally as consumed. `seq` on an Iterable or Java array is a single pass that can see later mutation, so do not mutate sources that have seqs on them.
- `doall` walks the seq, retains the head and returns it (whole seq in memory); `dorun` does not retain the head and returns nil; `run!` applies a procedure to each item for side effects and returns nil (since 1.7); `realized?` checks whether a lazy seq has been forced.

## Failure modes
- Side effects in a lazy `map` never happen if nothing consumes it; use `run!`, `doseq` or `mapv`.
- Effects other than those needed for the first element do not occur until the seq is consumed.
- Using `doall` on a huge seq keeps all of it in memory at once; use `dorun` or `run!` when you only want effects.

## Self-check
`(def r (map #(do (println %) %) [1 2 3]))` prints nothing until `(first r)` or `(doall r)`.

## Checked
2026-11-03. Confirmed against the clojure.org Sequences reference and the clojure.core API docstrings for doall, dorun, run!, rest/next, iterate, lazy-seq and realized?. Removed: the chunking (32 element) claim, the named eager/lazy function lists, the "Stream closed" and binding claims, the head-holding of def'd ranges, and the StackOverflowError claim (not on the pages read).
Method: documentation only; no commands were run.
