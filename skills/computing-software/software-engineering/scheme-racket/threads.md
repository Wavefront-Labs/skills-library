---
id: computing-software.software-engineering.scheme-racket.threads
name: threads
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, threads, racket-concurrency]
level: practitioner
status: docs-checked
description: "Start preemptive green threads with thread, wait with thread-wait, and kill with kill-thread; by default they do not run in parallel."
sources:
  - https://docs.racket-lang.org/guide/concurrency.html
  - https://docs.racket-lang.org/reference/threads.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Green threads
**Goal:** concurrent tasks.
```racket
(define t (thread (lambda () (sleep 0.1) (displayln "done"))))
(thread-wait t)
(thread-send t 'msg) (thread-receive)
```
- By default `thread`s are coroutine threads and do not run in parallel (`#:pool` creates parallel threads); use places or futures for parallelism.
- Main thread exit ends the program; wait for workers.
## Self-check
Start 3 threads printing, join all, verify output order is nondeterministic.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
