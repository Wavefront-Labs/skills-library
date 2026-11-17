---
id: computing-software.software-engineering.clojure.reader-conditionals-and-cljc-files
name: reader-conditionals-and-cljc-files
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, reader, cljc, reader-conditional, platform-specific, clojurescript, portable-code, reader-conditionals]
level: practitioner
status: docs-checked
description: "Write portable .cljc code using #? and #?@ reader conditionals with :clj, :cljs and :default branches, and know the splicing and feature-selection rules."
sources: ["https://clojure.org/reference/reader"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reader conditionals in .cljc files

**Goal:** share code between Clojure (JVM) and ClojureScript without forking files.

## Syntax
```clojure
(defn abs-val [x]
  #?(:clj  (Math/abs (long x))
     :cljs (js/Math.abs x)))

(defn args [] [1 #?@(:clj [2 3] :cljs [4 5])])   ; #?@ splices into the enclosing collection
```
- Allowed only in `.cljc` files, or when the reader is called with `{:read-cond :allow}`.
- Features: `:clj`, `:cljs`, `:cljr`, plus `:default` as fallback. The first matching feature wins; no match yields
  nothing (not nil).
- `#?@` must appear inside a collection, not at top level.

## Gotchas
- Every branch must be READABLE on both platforms even though only one is evaluated.
- A missing branch for a platform silently drops the form: `(defn f [] #?(:clj 1))` becomes `(defn f [])`
  in cljs, returning nil.
- `.clj` files cannot use `#?` unless the reader is configured; do not rename to `.cljc` for a single use.

## Self-check
`(read-string {:read-cond :allow :features #{:cljs}} "#?(:clj 1 :cljs 2)")` returns 2.

## Checked
2026-11-02. Confirmed: clojure.org/reference/reader: #? and #?@ syntax, platform features :clj :cljs :cljr, :default, first match wins, no match reads no form, non-selected branches are still read, splicing not allowed at top level, :read-cond :allow and :features options. Removed: the ClojureScript-only examples and the :require-macros bullet (clojurescript.org returned 403, so it is dropped from sources).
Method: documentation only; no commands were run.
