---
id: computing-software.software-engineering.scheme-racket.sequences-generators
name: sequences-generators
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sequences-generators]
level: practitioner
status: docs-checked
description: "Lazy and custom sequences in Racket: racket/generator (generator, yield) and racket/stream (stream-cons, stream-map, in-stream)."
sources:
  - https://docs.racket-lang.org/guide/for.html
  - https://docs.racket-lang.org/reference/sequences.html
  - https://docs.racket-lang.org/reference/streams.html
  - https://docs.racket-lang.org/reference/Generators.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sequences, streams and generators
**Goal:** lazy and custom sequences.
```racket
(require racket/generator racket/stream)
(define g (generator () (for ([i 3]) (yield i)) 'done))
(g) (g) (g) (g)   ; 0 1 2 done
(stream-first (stream-map add1 (in-naturals)))
(for ([x (in-stream (stream-take (in-naturals) 3))]) x)
```
- A generator is a procedure that returns the next value each time it is called; `yield` returns a value from inside the body, and a later call resumes at the `yield`. The body's eventual result is the final yield; calling again afterwards returns the same values, with 0 arguments. `generator` formals do not support keyword or optional arguments.
- A stream is a kind of sequence with `stream-first` and `stream-rest`. `stream-cons` builds a lazy stream: unless `#:eager` is given, neither the first expression nor the rest is evaluated immediately.
- Plain lists can be used as streams, and `in-range` and `in-naturals` also produce streams. `racket/stream` is provided by `racket` but not `racket/base`.
- `in-stream` can improve performance when it appears directly in a `for` clause.
## Self-check
Take the first five even squares from `in-naturals` with a stream.
## Checked
2026-11-08. Confirmed on the Reference Generators and Streams pages: generator and `yield` semantics, final-value behaviour, `stream-cons` laziness and `#:eager`, lists as streams, `in-stream`, and the `racket/stream` library note. Removed: "generator is built on continuations" and "lists are not streams" (the latter is wrong: the page says plain lists can be used as streams).
Method: documentation only; no commands were run.
