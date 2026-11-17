---
id: computing-software.software-engineering.clojure.transducers-map-filter-into-sequence
name: transducers-map-filter-into-sequence
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, transducers, transduce, into, sequence, eduction, completing, reduced, map, filter, comp]
level: advanced
status: docs-checked
description: "Compose map/filter/take pipelines as transducers with comp, run them via into, transduce, sequence or eduction, and write stateful or early-terminating ones."
sources: ["https://clojure.org/reference/transducers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transducers

**Goal:** build reusable, intermediate-collection-free processing pipelines.

```clojure
(def xf (comp (filter odd?) (map inc) (take 5)))   ; composes left-to-right in data flow order
(into [] xf (range))                    ;=> [2 4 6 8 10]
(transduce xf + 0 (range 100))          ; reduce with xf: init 0
(sequence xf coll)                      ; lazy output
(eduction xf coll)                      ; reducible/iterable, re-run on each reduce
(run! println (eduction (map inc) [1 2]))
```
- Transducer-returning arities exist for `map`, `filter`, `take`, `drop`, `mapcat`, `partition-all`, `dedupe`,
  `distinct`, `keep`, `take-while` and more: call them without the collection. `cat` is itself a transducer.
- A transducer is `(fn [rf] (fn ([] (rf)) ([acc] (rf acc)) ([acc x] ...)))`: init, completion, step arities.
- Stateful: use `volatile!` inside the closure; create state per transducer application, never at `def` time.
- Early exit: return `(reduced acc)`; call `unreduced` to unwrap; `completing` adapts
  a 2-arity reducing fn for `transduce`.
- `comp` order reads as the order data flows through the steps (opposite of ordinary function composition).

## Failure modes
- Missing completion arity breaks `transduce`/`into` for stateful transducers (must call `(rf acc)`).
- Sharing mutable state across runs by creating the volatile outside the `(fn [rf] ...)`.

## Self-check
`(transduce (comp (map inc) (filter even?)) conj [] (range 6))` gives `[2 4 6]`.

## Checked
2026-11-02. Confirmed: clojure.org/reference/transducers: list of functions with transducer arities, cat as a transducer, three-arity shape (init, completion, step), stateful transducers with volatile! created per application, reduced for early exit, completing, completion arity called exactly once; clojure.core API: transduce, sequence, eduction, into. Removed: ensure-reduced (not on the page) and cat from the call-without-collection list.
Method: documentation only; no commands were run.
