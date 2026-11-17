---
id: computing-software.software-engineering.clojure.transient-collections-for-batch-updates
name: transient-collections-for-batch-updates
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, transients, transient, persistent-bang, assoc-bang, conj-bang, performance, batch-updates, clojure-transients-transducers]
level: advanced
status: docs-checked
description: "Speed up local batch construction with transient, conj!/assoc!, and persistent!; use the returned value, never the original, and keep transients thread-confined."
sources: ["https://clojure.org/reference/transients"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transients

**Goal:** build large collections faster by temporarily allowing in-place mutation.

```clojure
(persistent!
  (reduce (fn [acc x] (conj! acc x)) (transient []) (range 1e6)))

(persistent! (reduce (fn [m [k v]] (assoc! m k v)) (transient {}) pairs))
```
- Supported: vectors, hash-maps, hash-sets (not lists or sorted collections).
- Always use the RETURN value of `conj!`/`assoc!` (they may return a different object); never rely on
  mutation of the original reference.
- After `persistent!` the transient is dead; further use throws an exception.
- Do not share a transient between threads concurrently.
- `(get t k)` and `count` work on transients; `dissoc!`, `disj!`, `pop!` exist.

## When to use
Only after profiling shows collection building matters. `into` and `reduce` with persistent collections are
usually fast enough.

## Failure modes
- Treating the transient like a mutable collection: `(def t (transient {})) (assoc! t :a 1) (persistent! t)` may
  lose updates.
- Returning a transient from a function to callers.

## Self-check
Benchmark `(into [] (range 1e6))` versus a loop of `conj` with a criterium run; confirm gap.

## Checked
2026-11-02. Confirmed: clojure.org/reference/transients: vectors, hash-maps and hash-sets only; use the return value of conj!/assoc!, do not bash in place; read-only interface (get, count, nth) works; persistent! ends the transient. Removed: the exact exception text and the claims about into using transients internally.
Method: documentation only; no commands were run.
