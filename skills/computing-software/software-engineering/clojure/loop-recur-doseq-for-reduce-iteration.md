---
id: computing-software.software-engineering.clojure.loop-recur-doseq-for-reduce-iteration
name: loop-recur-doseq-for-reduce-iteration
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, loop, recur, doseq, dotimes, for, list-comprehension, reduce, run, mapv, tail-recursion, loops-recur-doseq-for]
level: intro
status: docs-checked
description: "Iterate with loop/recur, reduce, doseq, dotimes, for comprehensions with :when/:let/:while and know laziness and tail-position rules."
sources: ["https://clojure.org/guides/learn/flow", "https://clojure.org/reference/special_forms"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Looping and iteration

**Goal:** pick the right construct for eager vs lazy and effects vs values.

```clojure
(loop [i 0 acc []] (if (< i 3) (recur (inc i) (conj acc i)) acc))
(reduce (fn [acc x] (+ acc x)) 0 xs)  (reduce + xs)  (reduced acc)  ; early exit
(doseq [x xs :when (odd? x)] (println x))            ; eager, side effects, returns nil
(dotimes [i 3] (println i))
(for [x (range 3) y (range 3) :when (< x y) :let [s (+ x y)]] [x y s])   ; lazy comprehension
(run! println xs)  (mapv f xs)  (doall (for ...))
```
- `recur` must be in tail position and its argument count must match the loop/fn params (a variadic fn's rest is
  one vector argument); mismatch gives "Mismatched argument count to recur".
- `recur` targets the nearest enclosing `loop` or `fn` method.
- Deep non-tail recursion overflows the stack (StackOverflowError): use `loop`/`recur`, `reduce`, or `trampoline`.
- `for` is lazy: do not use it only for side effects; use `doseq`.
- `doseq`/`for` binding order: later bindings vary fastest (inner loops).
- Prefer `reduce`/`into`/`mapv` over manual loops when they fit; loops are for multiple accumulators.

## Failure modes
- `recur` in non-tail position: "Can only recur from tail position".
- Boxed numbers in tight loops: type-hint locals or use `long`.

## Self-check
Compute factorial 20 with `loop` and with `reduce *`; confirm both agree, and 21 requires `*'`.

## Checked
2026-11-02. Confirmed: clojure.org/reference/special_forms (loop and recur: arity must match, tail position only, variadic rest passed as a single seq) and clojure.org/guides/learn/flow; clojure.core API: reduce, reduced, doseq, for, dotimes, run!, mapv, doall, trampoline. Removed: the claim that recur cannot be used inside try.
Method: documentation only; no commands were run.
