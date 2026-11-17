---
id: computing-software.software-engineering.clojure.dynamic-vars-binding-and-metadata
name: dynamic-vars-binding-and-metadata
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, dynamic-vars, binding, earmuffs, thread-local, with-meta, metadata, set-bang, ^:dynamic, private, ns-dynamic-binding-meta]
level: practitioner
status: docs-checked
description: "Use ^:dynamic vars with binding for thread-local overrides, understand conveyance across threads, and attach metadata with ^ and with-meta/vary-meta."
sources: ["https://clojure.org/reference/vars", "https://clojure.org/reference/metadata"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic vars, binding and metadata

**Goal:** use thread-local bindings and metadata deliberately.

```clojure
(def ^:dynamic *db* nil)                 ; earmuffs by convention
(defn q [] (:conn *db*))
(binding [*db* {:conn 1}] (q))           ;=> 1  (thread-local, visible to callees in this thread)

(def v (with-meta [1 2] {:src "file"}))  (meta v)    ; metadata does not affect equality
(vary-meta v assoc :seen true)
(defn ^{:added "1.0"} f [])              ; metadata on the var
(def ^:private ^:const limit 10)
```
- `binding` only works on vars declared `^:dynamic`; otherwise "Can't dynamically bind non-dynamic var".
- Bindings are conveyed into `future`, `send` and `pmap` bound-fn threads, but NOT into plain `Thread`s or
  lazy seqs realised after the `binding` exits.
- `bound-fn` and `bound-fn*` capture current bindings for callbacks.
- `with-redefs` changes the root and affects all threads; `binding` is per-thread.
- Metadata is carried by collections, symbols and vars, not numbers or strings; `with-meta` returns a new value.

## Gotchas
Lazy results read dynamic vars at realisation time; force them within the `binding` form.

## Self-check
`(binding [*print-length* 2] (pr-str (range 10)))` prints `(0 1 ...)`.

## Checked
2026-11-02. Confirmed: clojure.org/reference/vars (^:dynamic, binding, thread-local bindings, binding conveyance via future, send, send-off and pmap, alter-var-root, with-redefs) and clojure.org/reference/metadata (with-meta, vary-meta, metadata does not affect equality). No removals.
Method: documentation only; no commands were run.
