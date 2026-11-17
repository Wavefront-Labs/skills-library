---
id: computing-software.software-engineering.clojure.alts-mult-pub-sub-pipeline
name: alts-mult-pub-sub-pipeline
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, core.async, alts, alt, mult, tap, pub, sub, pipeline, pipeline-blocking, merge, mix, split, core-async-alts-pipelines]
level: advanced
status: docs-checked
description: "Select among channels with alts!, fan out using mult/tap and pub/sub, and run parallel stages with pipeline, pipeline-blocking and pipeline-async."
sources: ["https://clojure.github.io/core.async/", "https://github.com/clojure/core.async/blob/master/src/main/clojure/clojure/core/async.clj"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# alts!, mult, pub/sub, pipeline

**Goal:** compose multi-channel flows.

```clojure
(a/alts!! [c1 c2 (a/timeout 500)])         ;=> [val port]; first ready wins
(go (let [[v p] (a/alts! [in (timeout 1000)])] (if (= p in) v :timed-out)))
(a/alts!! [[out :value] in])               ; put or take
(def m (a/mult src))  (a/tap m c1)  (a/tap m c2)        ; broadcast every item
(def pb (a/pub events :type))  (a/sub pb :click c3)     ; topic routing
(a/pipeline 4 out (map inc) in)            ; parallel transducer stage, order preserved
(a/pipeline-blocking 4 out (map slow-io) in)
(a/pipeline-async 4 out (fn [v ch] ... (a/close! ch)) in)
(a/merge [c1 c2])  (a/into [] c)  (a/onto-chan! c coll)  (a/to-chan! coll)
```
- `pipeline` closes `out` when `in` closes unless `close?` is false (fifth argument, default true).
- `mult` stalls on the slowest tap; give taps buffers.
- `pub` drops items that have no matching subscriber; `mult` drops items received when there are no taps.
- Use `a/<!!` carefully in REPL tests; always add timeouts to avoid hung REPLs.

## Failure modes
- Forgetting to close source channels so downstream `pipeline` never finishes.
- A slow tap blocks all other `mult` consumers.

## Self-check
Run `(a/<!! (a/into [] (let [o (chan)] (a/pipeline 2 o (map inc) (a/to-chan! [1 2 3])) o)))` and expect `[2 3 4]`.

## Checked
2026-11-02. Confirmed: core.async source (async.clj docstrings): pipeline/pipeline-blocking/pipeline-async arities, close? default true and its position (fifth argument), mult and pub semantics (slow taps hold up the mult, items with no taps or subs dropped), ordering of pipeline output. Removed: the claim that close? is the fourth argument (it is the fifth).
Method: documentation only; no commands were run.
