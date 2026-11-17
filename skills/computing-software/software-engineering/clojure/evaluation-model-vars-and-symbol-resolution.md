---
id: computing-software.software-engineering.clojure.evaluation-model-vars-and-symbol-resolution
name: evaluation-model-vars-and-symbol-resolution
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, evaluation, vars, symbols, resolve, intern, var-root, def, alter-var-root, with-redefs, evaluation-vars-symbols]
level: practitioner
status: docs-checked
description: "Understand how Clojure resolves symbols to vars and locals, the read-eval-compile cycle, var roots, and tools like resolve, alter-var-root and with-redefs."
sources: ["https://clojure.org/reference/evaluation", "https://clojure.org/reference/vars"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluation model, symbols and vars

**Goal:** predict what a symbol means at a given place and how redefinition behaves.

## Model
The reader produces data; each top-level form is compiled to JVM bytecode and evaluated immediately, one at a
time. A symbol resolves to (in order): special form, local binding, class (if it names an imported class or
contains a dot), then a var in the current namespace or its refers/aliases.

## Vars
```clojure
(def ^:private limit 10)
(resolve 'limit)            ; the var, or nil
#'limit                     ; (var limit)
@#'limit                    ; deref the var, same as limit
(alter-var-root #'limit inc)  ; change the root binding, visible to all threads
(with-redefs [limit 99] (f))   ; temporarily swap root, for tests; not thread-isolated
(meta #'limit)              ; :name :ns :line :file :private ...
```
- Calls through a var look it up at each call unless direct linking is on (see the compilation reference), so
  redefining a function at the REPL affects callers.
- `def` inside a function creates a global var at runtime; avoid it.

## Failure modes
- `Unable to resolve symbol: x in this context`: missing `require`, typo, or use before `def` (use `declare`).
- A function value captured earlier (stored in a map, passed as an argument) does not see a REPL redefinition;
  pass `#'f` to keep a live reference.

## Self-check
Define `f`, store `(def g {:f f})`, redefine `f`, and confirm `((:f g))` still calls the old one.

## Checked
2026-11-02. Confirmed: clojure.org/reference/evaluation (forms compiled and evaluated one at a time, symbol resolution order beginning with special forms), clojure.org/reference/vars (def, var, alter-var-root, with-redefs, var metadata) and the compilation reference (direct linking).
Method: documentation only; no commands were run.
