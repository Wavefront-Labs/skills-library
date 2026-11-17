---
id: computing-software.software-engineering.clojure.type-hints-and-reflection-warnings
name: type-hints-and-reflection-warnings
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, type-hints, reflection, warn-on-reflection, primitive, long, double, performance, hint, type-hints-reflection]
level: advanced
status: docs-checked
description: "Remove reflection with type hints, enable *warn-on-reflection*, use primitive hints for fns and locals, and read the compiler's warning output."
sources: ["https://clojure.org/reference/java_interop", "https://clojure.org/reference/compilation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type hints and reflection

**Goal:** make interop calls fast and find the slow ones.

```clojure
(set! *warn-on-reflection* true)           ; per file, at the top (after ns)
(defn len [^String s] (.length s))         ; hint arg
(defn parse ^long [^String s] (Long/parseLong s))   ; primitive return hint (placed before params)
(let [^java.io.File f (io/file p)] (.getName f))
(defn sum ^double [^doubles xs] ...)       ; array hints: ^longs ^doubles ^objects ^bytes
```
- A reflection warning reports a call that cannot be resolved at compile time (for example "call to charAt can't be resolved"). Fix by hinting the target, not the result.
- Put the `set!` in each namespace you want checked.
- Hints go on the binding/arg (`^String s`) or the form (`^String (f x)`); a return hint goes before the arg vector
  (`(defn f ^String [x] ...)`) or on the name.
- Functions taking or returning primitives are limited to `long` and `double` params (and up to 4 args).
- Hinting a wrong class throws ClassCastException at runtime.

## Failure modes
- Hint placed on the wrong form silently ignored.
- Boxed math in loops: use `(loop [i 0] ...)` with long and `unchecked-*` or `*unchecked-math*` consciously.

## Self-check
Turn on warnings, load your namespace, count warnings, hint until zero.

## Checked
2026-11-02. Confirmed: clojure.org/reference/java_interop (type hints, reflection warnings, primitive fn hints limited to long and double with arity up to 4) and the compilation reference. Removed: the Leiningen :global-vars setting (not on the pages read) and the exact warning text.
Method: documentation only; no commands were run.
