---
id: computing-software.software-engineering.scheme-racket.futures
name: futures
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, futures]
level: advanced
status: docs-checked
description: "Parallelise primitive-heavy code with future and touch (racket/future); blocking operations serialise to the main thread."
sources:
  - https://docs.racket-lang.org/reference/places.html
  - https://docs.racket-lang.org/reference/futures.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Futures
**Goal:** cheap parallel loops.
```racket
(require racket/future)
(define fs (for/list ([i 4]) (future (lambda () (for/sum ([j 10000000]) j)))))
(map touch fs)
```
- Future parallelism is normally enabled on all platforms in Racket CS; a future blocks or synchronises with the main thread when it hits an operation that cannot run in parallel.
- `futures-enabled?` and `processor-count` show capability.
## Self-check
Compare wall time of `(map touch fs)` versus sequential.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
