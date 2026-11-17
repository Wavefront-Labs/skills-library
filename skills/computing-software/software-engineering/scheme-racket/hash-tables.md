---
id: computing-software.software-engineering.scheme-racket.hash-tables
name: hash-tables
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, hash-tables, racket-hash-sets]
level: intro
status: docs-checked
description: "Create and use mutable and immutable hash tables with hash, make-hash, hash-ref, hash-set, hash-set!, hash-update and iteration."
sources:
  - https://docs.racket-lang.org/guide/hash-tables.html
  - https://docs.racket-lang.org/reference/hashtables.html
  - https://docs.racket-lang.org/reference/sets.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash tables
**Goal:** key-value storage.
```racket
(define h (make-hash))               ; mutable, equal?-keyed
(hash-set! h "a" 1)
(hash-ref h "a")                     ; 1
(hash-ref h "z" #f)                  ; default value, or thunk
(define i (hash 'a 1))               ; immutable
(hash-set i 'b 2)                    ; returns new table
(hash-update i 'a add1 0)
(for ([(k v) (in-hash i)]) (displayln (cons k v)))
```
- `hash-ref` without default raises on a missing key.
- `hash-set` is for immutable tables, `hash-set!` for mutable.
- Each mutable-table operation is guarded by the table's semaphore, but `hash-update!` and `hash-ref!` are not atomic as a whole; use your own lock for compound updates.
## Self-check
`(hash-ref (hash) 'x)` raises; `(hash-ref (hash) 'x 0)` is `0`.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
