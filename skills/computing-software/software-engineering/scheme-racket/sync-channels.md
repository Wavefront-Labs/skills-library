---
id: computing-software.software-engineering.scheme-racket.sync-channels
name: sync-channels
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, sync-channels]
level: advanced
status: docs-checked
description: "Coordinate threads with make-channel, channel-put, channel-get and sync/timeout on events."
sources:
  - https://docs.racket-lang.org/guide/concurrency.html
  - https://docs.racket-lang.org/reference/threads.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Channels and sync
**Goal:** message passing.
```racket
(define ch (make-channel))
(thread (lambda () (channel-put ch 42)))
(channel-get ch)                       ; 42
(sync/timeout 1 ch)
```
- `channel-put` blocks until received.
- `sync` picks among events: channels, threads, timers (`alarm-evt`), ports.
## Self-check
`(sync/timeout 0.1 (make-channel))` returns `#f`.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
