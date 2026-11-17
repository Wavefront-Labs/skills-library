---
id: computing-software.software-engineering.scheme-racket.semaphores
name: semaphores
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, semaphores]
level: advanced
status: docs-checked
description: "Protect shared state with make-semaphore, semaphore-wait/post, call-with-semaphore, and mutable hash caution."
sources:
  - https://docs.racket-lang.org/guide/concurrency.html
  - https://docs.racket-lang.org/reference/threads.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Semaphores and locks
**Goal:** mutual exclusion.
```racket
(define lock (make-semaphore 1))
(call-with-semaphore lock (lambda () (set! n (add1 n))))
```
- `call-with-semaphore` releases on exception.
- `hash-update!` and `hash-ref!` use the table's semaphore separately for their lookup and store parts, so the update as a whole is not atomic; compound updates need your own lock.
## Self-check
Increment a counter from 100 threads with and without the lock.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
