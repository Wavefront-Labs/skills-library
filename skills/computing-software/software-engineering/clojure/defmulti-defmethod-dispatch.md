---
id: computing-software.software-engineering.clojure.defmulti-defmethod-dispatch
name: defmulti-defmethod-dispatch
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, multimethods, defmulti, defmethod, dispatch-fn, prefer-method, default, remove-method, multimethods-dispatch, clojure-multimethods]
level: practitioner
status: docs-checked
description: "Dispatch on any function of the arguments with defmulti/defmethod, add a :default method, resolve ambiguity with prefer-method and extend open-ended behaviour."
sources: ["https://clojure.org/reference/multimethods"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defmulti and defmethod

**Goal:** open polymorphism on arbitrary data (value, type, multiple args).

```clojure
(defmulti area :shape)                       ; dispatch fn: keyword lookup
(defmethod area :circle [{:keys [r]}] (* Math/PI r r))
(defmethod area :square [{:keys [s]}] (* s s))
(defmethod area :default [x] (throw (ex-info "unknown shape" {:x x})))

(defmulti combine (fn [a b] [(type a) (type b)]))   ; multi-argument dispatch
(methods area)  (get-method area :circle)  (remove-method area :square)
```
- Dispatch values are compared with `isa?`, so hierarchies and class inheritance apply.
- `defmulti` does NOT redefine on reload when the var already exists; use `(def area nil)` or
  `(ns-unmap *ns* 'area)` before re-evaluating, or `defonce` semantics will surprise you.
- Ambiguity: two methods match via `isa?` with no preference: `(prefer-method f :a :b)`.
- Multimethods dispatch on arbitrary functions of the arguments; protocols dispatch on the type of the first argument only (see the protocols skill).

## Failure modes
- `No method in multimethod 'area' for dispatch value: :triangle` (add `:default`).
- `Multiple methods in multimethod 'f' match dispatch value`: add `prefer-method`.
- Changing the dispatch function at the REPL has no effect until the var is unmapped.

## Self-check
Add a `:default` method that throws `ex-info` with the offending value and trigger it.

## Checked
2026-11-02. Confirmed: clojure.org/reference/multimethods: defmulti/defmethod, isa?-based dispatch, :default, prefer-method and the ambiguity error text, methods/get-method/remove-method; clojure.core API: defmulti only defines the var if it does not already hold a multimethod. Removed: the dispatch-cost comparison.
Method: documentation only; no commands were run.
