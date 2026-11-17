---
id: computing-software.software-engineering.scheme-racket.sicp-environment-model
name: sicp-environment-model
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-environment-model]
level: practitioner
status: draft
description: "Evaluate with frames and pointers: lambda captures its defining environment; applying a procedure creates a new frame (SICP 3.2)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The environment model
**Goal:** explain closure behaviour.
- Each frame maps names to values with an enclosing-frame link; `define` adds to the current frame, `set!` modifies the nearest existing binding.
- A procedure object is code plus the environment where `lambda` was evaluated.
- Use DrRacket's Check Syntax arrows to see binding structure.
## Self-check
Draw frames for `(define (make-counter) (let ([n 0]) (lambda () (set! n (add1 n)) n)))` called twice.
