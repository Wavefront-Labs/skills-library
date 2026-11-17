---
id: computing-software.software-engineering.clojure.special-forms-def-if-do-let-fn
name: special-forms-def-if-do-let-fn
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, special-forms, def, if, do, let, quote, var, fn, loop, recur, try, throw, monitor-enter, clojure-evaluation]
level: practitioner
status: docs-checked
description: "Know the fixed set of Clojure special forms (def, if, do, let*, quote, var, fn*, loop*, recur, throw, try, set!, new, dot) and how macros build on them."
sources: ["https://clojure.org/reference/special_forms"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Special forms

**Goal:** know what is built into the compiler versus what is a macro or function.

## The set
`def` `if` `do` `let` `quote` `var` `fn` `loop` `recur` `throw` `try` (with `catch` / `finally` clauses)
`monitor-enter` `monitor-exit`, plus dot (`.`), `new` and `set!` documented under Java interop and Vars. Macros
such as `cond`, `when`, `defn`, `and`, `or` and `->` build on these.

## Behaviour to remember
- `(if test then else?)`: only `nil` and `false` are logically false; everything else is true. A missing else yields nil.
- `(do a b c)` evaluates in order and returns the last.
- `(def x 1)` creates and interns (or locates) a global var in the current namespace; with an init it sets the root binding.
- `(recur ...)` rebinds the params of the enclosing `fn` or the bindings of the enclosing `loop` in parallel; it is the only non-stack-consuming looping construct (no tail-call optimization), and `recur` in other than tail position is an error checked by the compiler.
- `(do)` with no expressions returns nil.
- `set!` of fields is described in the Java interop section and `set!` of vars in the Vars section of the reference.

## Self-check
Write a factorial with `loop` / `recur` and confirm that moving `recur` out of tail position fails to compile.

## Checked

2026-11-02. Checked against clojure.org/reference/special_forms (list of special forms: def, if, do, let, quote, var, fn, loop, recur, throw, try with catch and finally, monitor-enter, monitor-exit, with dot, new and set! documented elsewhere; if semantics; do; def interns a var; recur semantics and tail-position check). Fixed: the list previously named let*, fn* and loop* instead of the documented let, fn, loop. Removed: the macroexpand examples, the dot-form expansion claims, the thread-local set! detail and the quoted error messages (not on that page).

Method: documentation only; no commands were run.
