---
id: computing-software.software-engineering.clojure.clojure-walk-zip-and-data-diff
name: clojure-walk-zip-and-data-diff
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clojure.walk, postwalk, prewalk, keywordize-keys, clojure.zip, zipper, clojure.data, diff, tree-traversal, walk-zip-data-diff]
level: advanced
status: docs-checked
description: "Transform nested data with clojure.walk postwalk/prewalk/keywordize-keys, navigate trees with clojure.zip zippers, and compare values with clojure.data/diff."
sources: ["https://clojure.github.io/clojure/clojure.walk-api.html", "https://clojure.github.io/clojure/clojure.zip-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# clojure.walk, clojure.zip, clojure.data

**Goal:** transform and compare nested structures.

```clojure
(require '[clojure.walk :as walk] '[clojure.zip :as zip] '[clojure.data :as data])
(walk/postwalk #(if (number? %) (inc %) %) {:a [1 2] :b 3})   ;=> {:a [2 3] :b 4}
(walk/prewalk-replace {:a :x} form)   (walk/postwalk-replace ...)
(walk/keywordize-keys {"a" 1})        (walk/stringify-keys m)
(walk/macroexpand-all form)

(def z (zip/vector-zip [1 [2 3] 4]))
(-> z zip/down zip/right zip/down zip/node)   ;=> 2
(zip/edit (zip/down z) inc)  (zip/replace z x)  (zip/insert-right z x)  (zip/root z)
(zip/seq-zip '(1 (2)))  (zip/xml-zip xml)  (zip/next z) (zip/end? z)

(data/diff {:a 1 :b 2} {:a 1 :b 3})   ;=> [{:b 2} {:b 3} {:a 1}]   [only-in-a only-in-b in-both]
```
- `postwalk` does a depth-first, post-order traversal (children first); `prewalk` is pre-order. `walk` supports all Clojure data structures except maps created with `sorted-map-by`.
- `zip/zipper` builds a custom zipper from `branch?`, `children`, `make-node` and a root; `zip/next` moves depth-first and returns a loc detectable with `zip/end?` at the end.
- `zip/edit` replaces the node with `(f node args)`; `zip/root` zips all the way up and returns the root node reflecting any changes.
- `clojure.data/diff` returns `[only-in-a only-in-b in-both]`; for equal inputs that is `[nil nil a]`. Maps are subdiffed where keys match and values differ, sets are never subdiffed, and sequential things are compared by index with results returned as vectors.

## Failure modes
- Forgetting `zip/root` after edits and returning only the sub-location.
- Using `walk` on a `sorted-map-by` map, which it does not support.

## Self-check
Walk `{:a {:b 1}}` and double every number; then diff the result against the original.

## Checked
2026-11-03. Confirmed against the clojure.walk, clojure.zip and clojure.data API pages: postwalk, prewalk, the -replace variants, keywordize-keys, stringify-keys, macroexpand-all, the sorted-map-by limitation, vector-zip, seq-zip, xml-zip, down, right, node, edit, replace, insert-right, root, next, end?, zipper, and diff's return tuple and comparison rules. Removed: the map-entry shape remark, the persistent-cursor remark and the expensive-walk failure mode (not on the pages).
Method: documentation only; no commands were run.
