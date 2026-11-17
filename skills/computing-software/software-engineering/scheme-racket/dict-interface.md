---
id: computing-software.software-engineering.scheme-racket.dict-interface
name: dict-interface
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, dict-interface]
level: practitioner
status: docs-checked
description: "Use the racket/dict generic interface (dict-ref, dict-set, in-dict) across hash tables, association lists and vectors."
sources:
  - https://docs.racket-lang.org/reference/dicts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic dict interface
**Goal:** write code over any dictionary.
```racket
(require racket/dict)   ; also provided by racket, not racket/base
(dict-ref '((a . 1)) 'a)
(dict-set (hash) 'k 1)
(for/hash ([(k v) (in-dict '((a . 1)))]) (values k (add1 v)))
```
- Dictionaries are hash tables, vectors (exact integer keys only), lists of pairs used as association lists (keys compared with `equal?`, which must be distinct), and structures implementing `gen:dict`.
- `dict-set` and `dict-remove` take an immutable dict and return a new one. `dict-set!` requires a mutable dict and raises `exn:fail:contract` if the dict is not mutable or the key is not allowed (for example a non-integer key on a vector).
- `(dict-ref dict key [failure-result])`: if the key is missing, a procedure `failure-result` is called with no arguments, any other value is returned as is, and with no `failure-result` an exception is raised.
- With duplicate keys in a list of pairs, `dict-ref` and `dict-remove` use the first instance of the key.
- `dict?` is not a constant-time test on pairs, since it may traverse the list to check it is an association list.
- `in-dict` returns a sequence giving key and value as two values; `in-dict-pairs` gives pairs.
## Self-check
`(dict-ref '((a . 1)) 'z 0)` returns `0`.

## Checked
2026-11-08. Read: Racket Reference 4.18 Dictionaries (reference/dicts.html), the intro, the `dict?`, `dict-mutable?`, `dict-ref`, `dict-set!`, `dict-set`, `dict-remove`, `in-dict` and `in-dict-pairs` entries (the page was read at those entries, not end to end). Removed `for/dict` from the description, which does not appear on the page (the example uses `for/hash`, a standard sequence form this page does not cover). Replaced the vague "alists must be proper lists of pairs" with the page's wording on distinct keys, and dropped the guide/hash-tables and reference/sets sources, which do not document the dict interface.
Method: documentation only; no commands were run.
