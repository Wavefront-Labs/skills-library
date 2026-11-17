---
id: computing-software.software-engineering.scheme-racket.parameters
name: parameters
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, parameters, racket-parameters]
level: practitioner
status: docs-checked
description: "Create dynamically scoped settings with make-parameter, read by calling it, and rebind with parameterize within a thread."
sources:
  - https://docs.racket-lang.org/reference/parameters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# make-parameter and parameterize
**Goal:** dynamic scope without globals.
```racket
(define depth (make-parameter 0))
(define (show) (displayln (depth)))
(parameterize ([depth 5]) (show))   ; 5
(show)                              ; 0
```
- New threads inherit the creating thread's parameterization at creation.
- `(depth 3)` mutates the current value (avoid except at startup).
## Self-check
After `parameterize` exits, `(depth)` returns the original value.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
