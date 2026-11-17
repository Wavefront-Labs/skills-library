---
id: computing-software.software-engineering.scheme-racket.dynamic-wind
name: dynamic-wind
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, dynamic-wind]
level: practitioner
status: docs-checked
description: "Guarantee cleanup with dynamic-wind pre/value/post thunks, or call-with-output-file style resource helpers; understand re-entry by continuations."
sources:
  - https://docs.racket-lang.org/guide/control.html
  - https://docs.racket-lang.org/reference/exns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dynamic-wind and cleanup
**Goal:** run cleanup on exit.
```racket
(dynamic-wind
  (lambda () (displayln "enter"))
  (lambda () (error "fail"))
  (lambda () (displayln "cleanup")))
```
- The post thunk runs after the value thunk returns and every time control jumps out of it; the pre thunk runs every time control jumps into it, including re-entry by a continuation.
- No special handling applies to jumps into or out of the pre and post thunks themselves.
- The value of `dynamic-wind` is the value returned by the value thunk.
## Self-check
"cleanup" prints when control jumps out of the value thunk.

## Checked

Date: 2026-11-02. Confirmed on Racket Reference Continuations (`dynamic-wind` pre, value and post thunks and jump behaviour). Removed: the advice about `call-with-output-file` and custodians, and the ordering claim against the REPL error message.

Method: documentation only; no commands were run.
