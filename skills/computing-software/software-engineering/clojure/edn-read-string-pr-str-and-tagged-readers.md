---
id: computing-software.software-engineering.clojure.edn-read-string-pr-str-and-tagged-readers
name: edn-read-string-pr-str-and-tagged-readers
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, edn, read-string, pr-str, print-method, tagged-readers, print-dup, serialization, data-readers, edn-read-print, clojure-data-formats]
level: practitioner
status: docs-checked
description: "Read and write EDN with clojure.edn/read-string and pr-str, handle custom types via tagged literals and print-method, and avoid core read-string on untrusted input."
sources: ["https://github.com/edn-format/edn", "https://clojure.org/reference/reader"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EDN

**Goal:** use Clojure's native data notation for config and interchange.

```clojure
(require '[clojure.edn :as edn])
(edn/read-string "{:a 1 :b #{1 2}}")
(edn/read-string {:readers {'my/point ->Point} :default tagged-literal} s)
(with-open [r (java.io.PushbackReader. (io/reader "config.edn"))] (edn/read r))
(pr-str {:a 1 "s" \c})    (prn x)   (binding [*print-length* 10] (pr-str xs))
(defmethod print-method Point [p ^java.io.Writer w] (.write w (str "#my/point " (pr-str [(:x p) (:y p)]))))
```
- EDN reader has no `#=`, `#()` or reader conditionals: it is safe for data. `clojure.core/read-string`
  with `*read-eval*` true can execute code.
- Built-ins: `#inst`, `#uuid`; everything else needs `:readers` or `:default`.
- `pr-str` output is readable (strings quoted, keywords with colon); `print`/`str` are for humans.
- Records print as `#ns.Rec{...}`; reading them back via the EDN reader needs a tag reader.
- `NaN` and infinity print as `##NaN`, `##Inf`, `##-Inf`; these symbolic values are a Clojure reader feature.
- Use `*print-namespace-maps*` (default true in REPL) to control `#:ns{...}` output, set to false for interchange.

## Failure modes
- `No reader function for tag foo/bar`: add `:readers` or `:default`.
- Atoms, functions and Java objects are not printable as data.

## Self-check
Round-trip `(edn/read-string (pr-str x))` for a nested map with a keyword set and `#inst`.

## Checked
2026-11-02. Confirmed: clojure.org/reference/reader and the EDN spec repository: #inst and #uuid built-ins, tagged literals and :readers/:default, no #= or reader conditionals in EDN, symbolic values ##Inf ##-Inf ##NaN, *print-namespace-maps*, *read-eval*. Removed: the float round-trip claim and the print-dup line.
Method: documentation only; no commands were run.
