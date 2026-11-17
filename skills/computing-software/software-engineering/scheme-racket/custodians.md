---
id: computing-software.software-engineering.scheme-racket.custodians
name: custodians
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, custodians]
level: advanced
status: docs-checked
description: "Bound resources with custodians: make-custodian, parameterize current-custodian, custodian-shutdown-all, and plumbers for flush on exit."
sources:
  - https://docs.racket-lang.org/guide/concurrency.html
  - https://docs.racket-lang.org/reference/threads.html
  - https://docs.racket-lang.org/reference/custodians.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custodians and resource management
**Goal:** clean shutdown.
```racket
(define c (make-custodian))
(parameterize ([current-custodian c]) (thread (lambda () (sleep 100))))
(custodian-shutdown-all c)
```
- `custodian-shutdown-all` closes the file-stream ports, TCP ports, TCP listeners and UDP sockets the custodian manages, and removes it as manager of threads; a thread with no managers is killed (or suspended, for `thread/suspend-to-kill`).
- A new thread is managed by the current custodian, and its allocation is accounted to its custodian managers; `custodian-limit-memory` sets a memory limit on a custodian.
## Self-check
After shutdown, the thread is `thread-dead?`.

## Checked

Date: 2026-11-02. Confirmed on Racket Reference Custodians (`custodian-shutdown-all`, `custodian-limit-memory`) and 11.1 Threads (management by the current custodian, `thread-dead?`). Removed: the platform-support hedge. Added the custodians page to sources.

Method: documentation only; no commands were run.
