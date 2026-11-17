---
id: computing-software.software-engineering.clojure.destructuring-vectors-and-maps
name: destructuring-vectors-and-maps
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, destructuring, let, fn, defn, keys, strs, syms, as, or, rest-args, destructuring-sequential-assoc, clojure-destructuring]
level: practitioner
status: docs-checked
description: "Destructure vectors and maps in let, fn and loop bindings using :as, :or, :keys, :strs, :syms, & rest and nested patterns, including defaults."
sources: ["https://clojure.org/guides/destructuring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destructuring vectors and maps

**Goal:** bind names directly from nested data in any binding form (`let`, `fn`, `defn`, `loop`, `doseq`, `for`).

## Sequential
```clojure
(let [[a b & more :as all] [1 2 3 4]] ...)   ; a=1 b=2 more=(3 4) all=[1 2 3 4]
(let [[_ _ third] xs] third)                  ; _ by convention for ignored
(let [[[x y] [z]] [[1 2] [3]]] ...)           ; nested
```
## Associative
```clojure
(let [{:keys [id name] :or {name "anon"} :as user} m] ...)   ; :or supplies defaults for keys not present
(let [{:strs [id]} {"id" 1}] id)                              ; string keys
(let [{:syms [x]} {'x 1}] x)
(let [{n :name, {c :city} :address} m] ...)                   ; rename and nest
(let [{:keys! [name age]} m] ...)                              ; since 1.13: throws if a key is missing
```
## Gotchas
- `:or` supplies defaults for keys that are not present in the input map; `:defaults` (since 1.13) binds the map of defaults that were applied.
- `:keys` is for keyword keys, `:strs` for string keys and `:syms` for symbol keys; the vector holds the local binding names.
- Since 1.13 the checked forms `:keys!`, `:strs!` and `:syms!` throw if a listed key is missing.

## Self-check
`(let [{:keys [a] :or {a 5}} {}] a)` returns 5, and `(let [[x & more :as all] [1 2 3]] [x more all])` returns `[1 (2 3) [1 2 3]]`.

## Checked

2026-11-02. Checked against clojure.org/guides/destructuring (& for the tail, :as, nested vectors, :or defaults for absent keys, :keys / :strs / :syms, :defaults and the checked :keys! / :strs! / :syms! forms added in 1.13, nested map destructuring). Removed (not stated on the page): namespaced :person/keys shorthand, the duplicate-local-name conflict, the `:or` behaviour with a present nil, the nth UnsupportedOperationException and the seq-as-keyword-arguments remark.

Method: documentation only; no commands were run.
