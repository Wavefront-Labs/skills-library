---
id: computing-software.software-engineering.scheme-racket.named-let
name: named-let
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, named-let]
level: intro
status: docs-checked
description: "Write loops with named let: (let loop ([i 0]) ...), calling loop in tail position for constant space."
sources:
  - https://docs.racket-lang.org/guide/let.html
  - https://docs.racket-lang.org/reference/let.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named let loops
**Goal:** idiomatic iteration without mutation.
```racket
(let loop ([i 0] [acc '()])
  (if (= i 5) (reverse acc) (loop (add1 i) (cons i acc))))
```
- A named `let` is equivalent to a `letrec`-bound function applied to the initial expressions; the name is visible only inside the body.
## Self-check
The loop above returns `'(0 1 2 3 4)`.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Named let (equivalence to `letrec`, binding visible only in the function body). Removed: the stack and memory claims and the 1,000,000 self-check.

Method: documentation only; no commands were run.
