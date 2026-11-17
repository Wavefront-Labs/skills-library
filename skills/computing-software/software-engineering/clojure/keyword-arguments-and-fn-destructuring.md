---
id: computing-software.software-engineering.clojure.keyword-arguments-and-fn-destructuring
name: keyword-arguments-and-fn-destructuring
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, kwargs, keyword-arguments, destructuring, defn, rest-args, apply, options-map, destructuring-kwargs]
level: practitioner
status: docs-checked
description: "Accept options as keyword arguments or an options map, destructure them in defn, and call with apply; know the Clojure 1.11 trailing-map behaviour."
sources: ["https://clojure.org/guides/destructuring", "https://clojure.org/news/2021/03/18/apis-serving-people-and-programs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyword arguments and function-argument destructuring

**Goal:** design option-taking functions that read well and call cleanly.

## Definition
```clojure
(defn connect [host & {:keys [port timeout] :or {port 80 timeout 1000}}] ...)
(connect "h" :port 8080)
(connect "h" {:port 8080})        ; Clojure 1.11+: a lone map is used outright for destructuring
(connect "h" :timeout 5 {:port 8080}) ; 1.11+: a trailing map is conj-ed onto the key/value pairs

(defn connect2 [host {:keys [port]}] ...)   ; explicit options map, simplest to compose
```
- Associative destructuring also works on the rest arg of a variadic function, treating the sequence as key/value pairs; `:or` supplies defaults for absent keys.
- Destructuring applies per argument: `(fn [[a b] {:keys [c]}] ...)`.

## Failure modes
- Passing a map where keyword arguments are expected only works from Clojure 1.11; check the version in use.
- `:or` entries should reference bindings and keys mentioned elsewhere in the same destructuring form.

## Self-check
Call your function with no options, with kwargs, and (1.11+) with a trailing map; all three should agree.

## Checked
2026-11-03. Confirmed against the clojure.org Destructuring guide (keyword-argument destructuring, :or, trailing map) and the Clojure 1.11 news post on keyword arguments (lone map used outright; trailing map conj-ed onto the pairs). Removed: the `apply` forms with `mapcat identity` and with a final map (a map spread by apply becomes entries, not a map; not documented), the odd-count error text, and the earlier-locals rule for `:or`.
Method: documentation only; no commands were run.
