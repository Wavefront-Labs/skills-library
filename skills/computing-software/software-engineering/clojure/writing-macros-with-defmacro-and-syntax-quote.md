---
id: computing-software.software-engineering.clojure.writing-macros-with-defmacro-and-syntax-quote
name: writing-macros-with-defmacro-and-syntax-quote
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, macros, defmacro, syntax-quote, unquote, unquote-splicing, macroexpand, quasiquote, defmacro-syntax-quote, clojure-macros]
level: advanced
status: docs-checked
description: "Write macros with defmacro using syntax-quote, unquote and unquote-splicing, and verify them with macroexpand-1; know when a function is the better choice."
sources: ["https://clojure.org/reference/macros"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# defmacro and syntax-quote

**Goal:** write a correct macro and inspect what it generates.

```clojure
(defmacro unless [test & body]
  `(if (not ~test) (do ~@body)))      ; ` syntax-quote, ~ unquote, ~@ unquote-splicing

(macroexpand-1 '(unless x (f) (g)))
;=> (if (clojure.core/not x) (do (f) (g)))
```
- Syntax-quote namespace-qualifies symbols (`clojure.core/not`) so the expansion is not captured by call-site
  names; use `~'name` to deliberately emit an unqualified symbol.
- A macro receives unevaluated forms (data) and returns a form; it runs at compile time.
- `&form` and `&env` are implicit args inside `defmacro` (the whole call form and local bindings).
- Macros are not first-class: they cannot be passed to `map` or `apply`. Wrap in a function if needed.

## Rules of thumb
1. If a function can do it, write a function. Macros are for new syntax, delaying evaluation or compile-time work.
2. Evaluate each argument at most once: bind it with a gensym local (see the hygiene skill).
3. Keep the macro thin: expand to a call of a regular function that holds the logic, so it is testable.

## Failure modes
- Using a macro as a value (passing it to `map` or `apply`) fails at compile time.
- Argument evaluated twice, producing double side effects.
- Using `'` instead of syntax-quote and capturing user symbols or leaving unresolved names.
- Macro definition after use: the earlier call site was compiled as a function call.

## Self-check
Call `macroexpand-1` and `macroexpand-all` (`clojure.walk/macroexpand-all`) on your macro with a side-effecting argument.

## Checked
2026-11-02. Confirmed: clojure.org/reference/macros (&form, &env, macros receive unevaluated forms and run at compile time) and clojure.org/reference/reader (syntax-quote qualification, unquote, unquote-splicing, ~'name); clojure.walk API (macroexpand-all); clojure.core macroexpand-1. Softened: the error-message bullet.
Method: documentation only; no commands were run.
