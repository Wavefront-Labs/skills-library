---
id: computing-software.software-engineering.clojure.macro-hygiene-gensym-and-expansion-debugging
name: macro-hygiene-gensym-and-expansion-debugging
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, macros, gensym, auto-gensym, hygiene, variable-capture, macroexpand, syntax-quote, macro-hygiene-gensym]
level: advanced
status: docs-checked
description: "Avoid variable capture in macros with auto-gensym (x#), evaluate arguments once, and inspect expansions with macroexpand-1, macroexpand and &form."
sources: ["https://clojure.org/reference/macros", "https://clojure.org/reference/reader"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macro hygiene and expansion debugging

**Goal:** make macros safe against variable capture and double evaluation.

```clojure
(defmacro with-timing [expr]
  `(let [start# (System/nanoTime)          ; auto-gensym: same start# within one syntax-quote
         result# ~expr]
     (println "ms:" (/ (- (System/nanoTime) start#) 1e6))
     result#))

(defmacro twice [x] `(let [v# ~x] [v# v#]))   ; x evaluated once
```
- Syntax-quote resolves a symbol in the current context to a fully-qualified symbol.
- A non-qualified symbol ending in `#` becomes a generated symbol (name plus `_` and a unique id), and all
  references to it within one syntax-quoted expression resolve to the same generated symbol.
- Unquote inserts one value into the template; unquote-splicing inserts a sequence of values.
- Binding `expr` once to a gensym'd local and reusing it avoids evaluating the argument twice.

## Debugging
```clojure
(macroexpand-1 '(my-macro ...))   ; one step
(macroexpand '(my-macro ...))     ; expand the head form until it is no longer a macro
```
- Inside `defmacro`, `&form` is the actual form being invoked (as data) and `&env` is a map of local
  bindings at the expansion point; printing `&form` helps trace.
- `fn`, `let` and `loop` are themselves macros (for destructuring), and `when` expands to `if` and `do`.

## Self-check
Write a macro that binds a literal local name, then use it where the caller has the same name; confirm the
`name#` version avoids the clash.

## Checked
Method: 2026-11-08 read clojure.org/reference/macros and clojure.org/reference/reader (syntax-quote section). Rewritten to what they state. Removed unsupported claims: clojure.walk/macroexpand-all, *print-meta*, spec fdef on macros, anaphoric ~'it advice, and the "bad" example's error text. The line that the same name# in two separate syntax-quotes differs and the manual gensym suggestion were dropped as not stated on the pages. Unchanged: both code examples.
