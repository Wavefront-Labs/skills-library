---
id: computing-software.software-engineering.scheme-racket.sicp-amb-nondeterminism
name: sicp-amb-nondeterminism
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-amb-nondeterminism]
level: advanced
status: draft
description: "Implement backtracking search with amb, require and success/failure continuations (SICP 4.3), or approximate with call/cc."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# amb and nondeterministic evaluation
**Goal:** declarative search.
```racket
(define fail-stack '())
(define (amb-list choices)
  (let/cc k (for ([c choices]) (let/cc next (set! fail-stack (cons next fail-stack)) (k c))) (error "no more")))
```
- A real `amb` needs a failure continuation stack; the above is only a sketch, test before relying on it.
- Alternative: `racket/control` or the `amb` packages.
## Self-check
Solve the "multiple dwelling" puzzle with `require` and `amb`.
