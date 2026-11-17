---
id: computing-software.software-engineering.clojure.fn-arities-variadics-and-closures
name: fn-arities-variadics-and-closures
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, defn, fn, arity, multi-arity, variadic, closures, docstring, pre-post, letfn, fn-arity-closures, clojure-functions]
level: intro
status: docs-checked
description: "Define functions with multiple arities, variadic rest args, docstrings, pre/post conditions and closures; know named fn, defn- and when to use letfn."
sources: ["https://clojure.org/reference/special_forms", "https://clojure.org/guides/learn/functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functions: arities, variadics, closures

**Goal:** write idiomatic function definitions.

```clojure
(defn greet
  "Docstring goes before the params."
  ([] (greet "world"))
  ([name] (greet "Hello" name))
  ([greeting name & more]
   {:pre  [(string? name)]
    :post [(string? %)]}
   (str greeting ", " name)))

(defn- private-helper [x] x)               ; private to the namespace
(let [n 3] (fn add-n [x] (+ x n)))         ; closure; the name allows self-reference
(letfn [(ev? [n] (if (zero? n) true (od? (dec n))))
        (od? [n] (if (zero? n) false (ev? (dec n))))]
  (ev? 10))                                 ; mutually recursive local fns
```
- Multiple arities must be defined in the same `defn` (a second `defn` replaces the first), and the arities of the overloads must be distinct. One arity can call another.
- Variable parameters (`& rest`) must come at the end of the parameter list and are collected into a sequence. In `#()` literals `%&` holds the remaining args.
- `:pre`/`:post` conditions go in a map at the start of the body; `%` in `:post` is the return value. If a condition is false and `*assert*` is true, a `java.lang.AssertionError` is thrown.
- A `fn` name is bound inside the function to the function itself, allowing self-calls even in anonymous functions. `letfn` makes all of its names available in all of its function definitions and the body.

## Self-check
Call `(greet)`, `(greet "x")` and `(greet "Hi" "x" 1 2)` and confirm each works.

## Checked
2026-11-03. Confirmed against the clojure.org special forms reference, the Functions learn guide and the clojure.core docstrings for defn-, letfn: multi-arity rules, variadics, %&, :pre/:post with *assert* and AssertionError, fn self-name, letfn scoping, defn- non-public. Removed: the ArityException message, the one-variadic-arity and fixed-versus-variadic size rules, the `(set! *assert* false)` advice, the map-argument advice and the metadata examples (not on the pages read).
Method: documentation only; no commands were run.
