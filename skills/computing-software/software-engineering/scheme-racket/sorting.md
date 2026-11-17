---
id: computing-software.software-engineering.scheme-racket.sorting
name: sorting
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sorting]
level: intro
status: docs-checked
description: "Sort with sort and #:key, #:cache-keys?, using strict comparison; sort is stable."
sources:
  - https://docs.racket-lang.org/reference/pairs.html
  - https://docs.racket-lang.org/reference/vectors.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorting
**Goal:** order lists predictably.
```racket
(sort '(3 1 2) <)
(sort '(("b" 1) ("a" 2)) string<? #:key car)
```
- Use `<`/`string<?`, not `<=`, to keep stability meaningful.
- `#:cache-keys? #t` when the key function is expensive.
- Sort vectors with `vector-sort` from `racket/vector`.
## Self-check
Sort `'("b" "A" "a")` with `string<?` and with `string-ci<?`, compare.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
