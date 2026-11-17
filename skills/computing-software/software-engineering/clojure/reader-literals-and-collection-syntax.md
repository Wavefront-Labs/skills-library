---
id: computing-software.software-engineering.clojure.reader-literals-and-collection-syntax
name: reader-literals-and-collection-syntax
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, reader, literals, keywords, symbols, vectors, maps, sets, syntax, literals-collections, clojure-reader]
level: intro
status: docs-checked
description: "Read and write Clojure literals: numbers, strings, keywords, symbols, lists, vectors, maps, sets, regex and character forms, and what the reader returns."
sources: ["https://clojure.org/reference/reader", "https://clojure.org/guides/learn/syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reader literals and collection syntax

**Goal:** know exactly what each piece of source text becomes before evaluation.

## Forms
```clojure
42  3.14  1/3  42N  1.5M  0xFF  2r1010   ; long, double, ratio, BigInt, BigDecimal, hex, radix
"str"  \a  \newline  #"re.*"             ; string, char, regex pattern
:kw  :ns/kw  ::local-kw  ::alias/kw      ; keywords; :: resolves in the current ns
'sym  'ns/sym  nil  true  false
'(1 2 3)  [1 2 3]  {:a 1 :b 2}  #{1 2 3} ; list, vector, map, set
```
- Commas are whitespace. `{:a 1, :b 2}` equals `{:a 1 :b 2}`.
- A map literal needs an even number of forms; a set literal with duplicate elements throws at read time
  (`#{1 1}` reports a duplicate key).
- A list in code is a call; quote it (`'(1 2 3)`) or use `(list 1 2 3)` to get data.
- `::kw` expands at read time using `*ns*`; `#:person{:name "A" :age 3}` is the namespaced-map shorthand
  for `{:person/name "A" :person/age 3}`.

## Symbols vs keywords
Keywords evaluate to themselves and are functions of maps (`(:a {:a 1})` returns 1). Symbols are resolved
to vars or locals.

## Failure modes
- Unbalanced brackets cause reader errors; use a structural editor (paredit, parinfer).
- A map literal with an odd number of forms is a reader error.
- `(1 2 3)` evaluated as code throws a ClassCastException (a Long is not a function).

## Self-check
At a REPL: `(map type [1 1.5 1/2 1N 1M \a "s" :k 's #"r" '() [] {} #{}])` and predict each class before running.

## Checked
2026-11-02. Confirmed: clojure.org/reference/reader and clojure.org/guides/learn/syntax: numeric literal forms (ratio, N, M, hex, radix), strings, characters, regex literals, keywords and :: resolution, lists vectors maps sets, commas as whitespace, namespaced-map shorthand, keywords as functions. Softened: reader error messages.
Method: documentation only; no commands were run.
