---
id: computing-software.software-engineering.scheme-racket.sicp-streams
name: sicp-streams
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sicp-streams]
level: advanced
status: draft
description: "Implement lazy sequences with delay/force and stream-cons, or use racket/stream (stream-cons, stream-first, stream-rest) (SICP 3.5)."
sources:
  - https://sarabander.github.io/sicp/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Streams and delayed evaluation
**Goal:** infinite sequences.
```racket
(require racket/stream)
(define (ints n) (stream-cons n (ints (add1 n))))
(stream->list (stream-take (ints 1) 5))
```
- SICP's `cons-stream` is a special form; in Racket use `stream-cons` (lazy in both fields) or `racket/promise` `delay`/`force`.
- Memoisation matters: `delay` memoises, avoiding exponential recomputation.
## Self-check
Build `integers`, then a stream of primes via sieve and take 10.
