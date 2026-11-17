---
id: computing-software.software-engineering.clojure.clojure-set-union-difference-join-index
name: clojure-set-union-difference-join-index
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clojure.set, union, intersection, difference, join, project, rename, index, map-invert, subset, clojure-set-relational, clojure-core-library]
level: practitioner
status: docs-checked
description: "Use clojure.set union, intersection, difference, subset?, rename-keys, map-invert and relational join/project/index operations on sets of maps."
sources: ["https://clojure.github.io/clojure/clojure.set-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# clojure.set

**Goal:** set algebra and simple relational operations.

```clojure
(require '[clojure.set :as set])
(set/union #{1 2} #{2 3})  (set/intersection a b)  (set/difference a b)
(set/subset? a b)  (set/superset? a b)
(set/rename-keys {:a 1} {:a :b})    ;=> {:b 1}
(set/map-invert {:a 1 :b 2})        ;=> {1 :a, 2 :b}  (duplicate values: one wins)
(set/select even? #{1 2 3 4})
(set/project #{{:a 1 :b 2}} [:a])
(set/join users orders)             ; natural join on common keys of sets of maps
(set/join users orders {:id :user-id})
(set/index users [:dept])           ; map from {:dept x} to the set of matching rows
(set/rename #{{:a 1}} {:a :x})
```
- The set operations expect sets; convert other collections with `(set coll)`.
- Relational functions treat each map as a row; `join` without a key map joins on the keys the relations share.
- `(contains? #{nil} nil)` is true; `(get #{nil} nil)` returns nil, ambiguous: use `contains?`.

## Failure modes
- `map-invert` of non-unique values drops entries.

## Self-check
Join two small sets of maps by `:id` and compare to a manual `group-by` implementation.

## Checked
2026-11-02. Confirmed: clojure.set API page: union, intersection, difference, subset?, superset?, select, project, rename, rename-keys, map-invert, join (with and without key map), index; clojure.core API: contains? and get on sets. Removed: the performance remark about argument order and the vector-input claims (not stated).
Method: documentation only; no commands were run.
