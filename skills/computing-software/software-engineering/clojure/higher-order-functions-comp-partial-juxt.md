---
id: computing-software.software-engineering.clojure.higher-order-functions-comp-partial-juxt
name: higher-order-functions-comp-partial-juxt
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, comp, partial, juxt, complement, constantly, identity, fnil, memoize, some-fn, every-pred, threading-macros, higher-order-comp-partial]
level: practitioner
status: docs-checked
description: "Compose behaviour with comp, partial, juxt, complement, fnil, memoize, every-pred, some-fn and the -> ->> as-> some-> cond-> threading macros."
sources: ["https://clojure.org/guides/threading_macros", "https://clojure.github.io/clojure/clojure.core-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Higher-order functions and threading

**Goal:** compose small functions rather than writing nested lambdas.

```clojure
((comp inc *) 2 3)                  ;=> 7   (right to left; the rightmost may take many args)
((partial + 10) 5)                  ;=> 15
((juxt first last count) [1 2 3])   ;=> [1 3 3]
(filter (complement even?) xs)
(update m :n (fnil inc 0))          ; substitute a default for nil input
(def slow (memoize f))              ; caches results by args; trades memory for speed
((every-pred pos? even?) 4)  ((some-fn :a :b) m)

(-> m (assoc :a 1) (update :b inc))             ; thread first
(->> xs (map inc) (filter even?) (reduce +))    ; thread last
(as-> x $ (f 1 $) (g $ 2))                      ; arbitrary position
(some-> m :a :b inc)                            ; stops at nil
(cond-> m flag? (assoc :a 1) other? (dissoc :b)) ; conditional steps
```
## Gotchas
- `memoize` keeps a cache, so memory use grows with the distinct arguments seen.
- `->` inserts the threaded value between the function name and the first argument; `->>` inserts it as the last argument. A bare symbol or keyword without parentheses is called with the value as its single argument, so `(-> x f)` is `(f x)`.
- `some->` evaluates to nil as soon as a step yields nil instead of raising; `cond->` threads through only the steps whose test is true; `cond->>` is the thread-last variant.

## Self-check
Rewrite `(f (g (h x)))` as `(-> x h g f)` and confirm identical output.

## Checked
2026-11-03. Confirmed against the clojure.core API docstrings (comp, partial, juxt, complement, fnil, memoize, every-pred, some-fn, as->, some->, cond->, ->, ->>) and the Threading Macros guide. Removed: the "no eviction" claim, the bounded-cache-library advice, the wrapping advice for `#()` steps and the prefer-`->`-for-maps style advice (not on the pages read).
Method: documentation only; no commands were run.
