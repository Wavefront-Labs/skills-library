---
id: computing-software.software-engineering.scheme-racket.call-cc
name: call-cc
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, call-cc, racket-continuations]
level: advanced
status: docs-checked
description: "Capture continuations with call/cc (call-with-current-continuation) for early exit; prefer let/ec or call/ec for escapes in Racket."
sources:
  - https://docs.racket-lang.org/guide/control.html
  - https://docs.racket-lang.org/reference/continuations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# call/cc escape and re-entry
**Goal:** early exit and backtracking.
```racket
(let/ec return (for ([x '(1 2 3)]) (when (> x 1) (return x))) #f)   ; 2
(define k #f)
(+ 1 (call/cc (lambda (c) (set! k c) 1)))
(k 10)   ; re-enters at top level: 11
```
- A captured continuation runs up to the nearest enclosing prompt; each REPL interaction is implicitly wrapped in a prompt.
- Applying a continuation from `call/cc` first aborts to the current prompt, then restores the saved continuation.
- `let/ec` (escape continuations, `call/ec`) is implemented more efficiently than `call/cc` and fits early exits.
## Self-check
Use `let/ec` to stop a loop at the first match.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Continuations and Racket Reference Continuations (`call/cc` is `call-with-current-continuation`; REPL interactions are wrapped in a prompt; `let/ec` and `call/ec` are more efficient escape-only forms). Removed: the per-top-level-form prompt wording.

Method: documentation only; no commands were run.
