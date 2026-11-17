---
id: computing-software.software-engineering.clojure.debugging-with-tap-and-repl-inspection
name: debugging-with-tap-and-repl-inspection
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, debugging, tap, add-tap, clojure-repl, doc, source, pst, debugging-tap-repl-tools, clojure-debugging-profiling]
level: practitioner
status: docs-checked
description: "Inspect values in running Clojure code with tap>, add-tap and remove-tap, clojure.repl doc/source/apropos/dir/pst, REPL last-value vars and print limits."
sources: ["https://clojure.github.io/clojure/clojure.core-api.html", "https://clojure.github.io/clojure/clojure.repl-api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging with tap> and clojure.repl

**Goal:** see intermediate values without littering code with println.

```clojure
(add-tap #(prn :tap %))              ; f, a fn of one argument, is called with anything sent via tap>
(tap> {:user u :step :validate})     ; will not block; true if there was room in the queue, false if dropped
(remove-tap f)                       ; remove f from the tap set

(require '[clojure.repl :refer [doc source apropos dir find-doc pst]])
(doc map)  (source map)  (dir clojure.string)  (apropos "sort")
```
- `doc` prints documentation for a var or special form (or a spec given a keyword); `find-doc` searches docs
  and names by regex or string; `source` prints source if it can find it; `dir` prints a sorted directory of a
  namespace's public vars; `apropos` returns public definitions in loaded namespaces matching a string or regex.
- `pst` prints a stack trace to a requested depth, defaulting to the root cause; `root-cause` peels off an
  exception's wrappers.
- `*1`, `*2`, `*3` hold the most recent, second and third most recent printed values; `*e` the most recent
  exception caught by the REPL.
- `*print-length*` limits items printed per collection and `*print-level*` nesting depth; the root binding of
  both is nil (no limit).
- Poor man's spy: `(defn spy [x] (println x) x)` then thread `(-> x f spy g)`.

## Self-check
Register a tap, `tap>` a map inside a function, call it and see the map printed.

## Checked
Method: 2026-11-08 read clojure.repl-api and the tap/REPL var/print var docstrings in clojure.core-api (only the first 100k and 200k-300k chars of the long page were read, covering these entries). Removed unsupported claims: Portal/Reveal usage, scope-capture, JDWP/Cursive debugging, the 1.10 version claim, "silently drops with no tap" failure mode, and the dev-only macro advice. Unchanged: spy helper (plain code, not from the docs) and the self-check.
