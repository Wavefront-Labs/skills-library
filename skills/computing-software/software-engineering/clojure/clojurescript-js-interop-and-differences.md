---
id: computing-software.software-engineering.clojure.clojurescript-js-interop-and-differences
name: clojurescript-js-interop-and-differences
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clojurescript, js-interop, goog, differences, macros, namespaces, cljs-differences-js-interop]
level: practitioner
status: docs-checked
description: "Key documented differences between ClojureScript and JVM Clojure (numbers, characters, namespaces, macros, vars, concurrency) and the js/ host-interop basics."
sources: ["https://clojurescript.org/about/differences", "https://clojurescript.org/reference/javascript-api"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ClojureScript JS interop and differences

**Goal:** avoid porting JVM assumptions into ClojureScript.

```clojure
goog/LOCALE                          ; interop works with new, /, . where possible
(.-NEGATIVE_INFINITY js/Number)      ; => -Infinity
js/Infinity                          ; js namespace reaches global properties
(.indexOf [1 2 3 5 7] 5)             ; => 3   (stable, public per the JS API page)
(.lastIndexOf [1 2 3 5 2 7] 2)       ; => 4
```

## Reader and data
- Only integer and floating-point literals mapping to JS primitives; no ratio, BigDecimal or BigInteger
  literals. Equality follows JS: `(= 0.0 0)` is true.
- No character literals; characters are single-character strings.
- `read` and `read-string` are in `cljs.reader`. `*out*` and `*err*` are not implemented. Regex follows JS.
- `nil` is both JS `null` and `undefined`. Keywords are not guaranteed `identical?`; use `keyword-identical?`.
- Persistent collections exist, with transients for vectors, hash maps and hash sets; not every collection
  function is implemented. StructMaps (`defstruct` etc.) are not implemented.

## Interop and hints
- `Foo/bar` always means `Foo` is a namespace; no Java-style static field access.
- `^long`/`^double` are hints only; `^boolean` matters because it avoids a checked `if`.

## Namespaces and macros
- `:use` needs `:only`; `:require` supports `:as`, `:refer`, `:rename` but not `:refer :all` or prefix lists;
  `:import` works only for Google Closure classes.
- Macros must be defined in a different compilation stage (typically another namespace) and referenced with
  `:require-macros` (or `:include-macros`/`:refer-macros`). A macro and function may share a name; macro
  expansion runs first.

## Vars and concurrency
- `def` yields ordinary JS variables; vars are not reified at runtime; `intern` is not implemented; `:private`
  is not enforced (an analysis warning); `fn` does not enforce arity at runtime.
- Atoms work as in Clojure; refs/STM and agents are not supported; `locking` is not implemented.

## Self-check
Confirm `(= 1 1.0)` is true in a cljs REPL, and that `(.indexOf [1 2 3] 3)` returns 2.

## Checked
Method: 2026-11-08 read clojurescript.org/about/differences and clojurescript.org/reference/javascript-api. The API page only documents indexOf and lastIndexOf. Removed unsupported claims: clj->js/js->clj/#js/set!/aget usage, `^js` externs hints, exception forms, js/Promise and core.async advice, deftype mutable fields, failure modes. Self-check not run.
