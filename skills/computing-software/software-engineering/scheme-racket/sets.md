---
id: computing-software.software-engineering.scheme-racket.sets
name: sets
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sets]
level: practitioner
status: docs-checked
description: "Use racket/set sets: set, set-add, set-member?, set-union, subset?, and choose list-based or mutable variants."
sources:
  - https://docs.racket-lang.org/guide/hash-tables.html
  - https://docs.racket-lang.org/reference/sets.html
  - https://docs.racket-lang.org/reference/sets.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sets
**Goal:** membership collections.
```racket
(require racket/set)
(define s (set 1 2 3))
(set-member? s 2) (set-add s 4) (set-union s (set 9)) (subset? (set 1) s)
(for ([x (in-set s)]) (displayln x))
(list->set '(1 1 2))
```
- `set` is immutable and `equal?`-based; `mutable-set` and `seteq` exist.
## Self-check
`(set-count (list->set '(1 1 2)))` is `2`.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
