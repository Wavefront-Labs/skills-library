---
id: computing-software.software-engineering.scheme-racket.and-or
name: and-or
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, and-or]
level: intro
status: docs-checked
description: "Use and/or as value-returning short-circuit operators; and returns the last value, or returns the first truthy value."
sources:
  - https://docs.racket-lang.org/guide/conditionals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# and, or and short-circuit values
**Goal:** exploit truthy-value results.
```racket
(or (hash-ref h k #f) (compute k))
(and (pair? l) (car l))
```
- `(and)` is `#t`, `(or)` is `#f`.
- Only `#f` is false; `0`, `'()` and `""` are true.
## Self-check
`(or #f 0)` returns `0`.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Conditionals (only `#f` is false; `(and)` is `#t`; `(or)` is `#f`; `or` returns the first non-`#f` value). Removed: nothing.

Method: documentation only; no commands were run.
