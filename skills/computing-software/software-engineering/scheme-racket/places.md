---
id: computing-software.software-engineering.scheme-racket.places
name: places
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, places, racket-parallelism]
level: advanced
status: docs-checked
description: "Run parallel Racket instances with dynamic-place or place forms and communicate by place-channel messages."
sources:
  - https://docs.racket-lang.org/reference/places.html
  - https://docs.racket-lang.org/reference/futures.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Places
**Goal:** multi-core parallelism.
```racket
(require racket/place)
(define p (place ch (place-channel-put ch (add1 (place-channel-get ch)))))
(place-channel-put p 1) (place-channel-get p)   ; 2
```
- Places do not share mutable state; messages are copied.
- Each place loads modules separately, so startup is costly.
## Self-check
Run the example from a module file (place forms need a module context).

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
