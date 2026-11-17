---
id: computing-software.software-engineering.clojure.reader-macros-and-tagged-literals
name: reader-macros-and-tagged-literals
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, reader, tagged-literals, inst, uuid, data_readers, quote, deref, var-quote, anonymous-fn, reader-macros-tagged-literals]
level: practitioner
status: docs-checked
description: "Use quote, deref, var-quote, #() anonymous functions, #_ discard and tagged literals such as #inst and #uuid, including custom data_readers.clj tags."
sources: ["https://clojure.org/reference/reader"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reader macros and tagged literals

**Goal:** read dispatch syntax correctly and add your own tagged literals safely.

## Built-in dispatch forms
```clojure
'x            ; (quote x)
@a            ; (deref a)
#'f           ; (var f)
#(+ % %2 %&)  ; anonymous fn: % = %1, %2 ..., %& = rest args; #() cannot nest
#_(ignored)   ; discard the next form at read time (stackable: #_#_ a b)
^:private     ; metadata shorthand for ^{:private true}
#inst "2026-01-01T00:00:00.000-00:00"   ; java.util.Date
#uuid "5fe5ab5e-0000-4000-8000-000000000000"
```
- `(comment ...)` is a macro returning nil: its body is read but never evaluated. `#_` drops the form at read time,
  so the form must still be readable.

## Custom tagged literals
1. Create `data_readers.clj` (or `.cljc`) at the classpath root containing a map from namespace-qualified tag
   symbols to var symbols: `{my/point my.app.readers/->point}`.
2. Tags must be namespace-qualified; unqualified tags are reserved for Clojure.
3. Without the file, bind `*data-readers*` or pass `:readers` to `clojure.edn/read-string`.
4. Use `*default-data-reader-fn*` (or the `:default` option for EDN) to handle unknown tags, e.g. with `tagged-literal`.

## Gotchas
- `#()` cannot contain nested `#()`; use `fn` for nesting.
- `clojure.core/read-string` can evaluate code via `#=` when `*read-eval*` is true; use `clojure.edn/read-string`
  for untrusted data.

## Self-check
`(read-string "#(inc %)")` returns a `(fn* [p1__N#] ...)` form; evaluating that form and calling it with 1 returns 2.

## Checked
2026-11-02. Confirmed: clojure.org/reference/reader: quote, deref, var, #() with % %1 %& and no nesting, #_ (stackable), ^ metadata, #inst, #uuid, data_readers.clj/.cljc, qualified tags, *data-readers*, *default-data-reader-fn*, :readers option of clojure.edn. Removed: the claim about requiring the reader function namespace manually.
Method: documentation only; no commands were run.
