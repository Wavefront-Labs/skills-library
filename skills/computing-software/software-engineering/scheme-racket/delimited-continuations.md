---
id: computing-software.software-engineering.scheme-racket.delimited-continuations
name: delimited-continuations
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, delimited-continuations]
level: advanced
status: docs-checked
description: "Use call-with-continuation-prompt, abort-current-continuation and call-with-composable-continuation (racket/control: reset, shift) for generators and effects."
sources:
  - https://docs.racket-lang.org/guide/control.html
  - https://docs.racket-lang.org/reference/continuations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prompts and delimited continuations
**Goal:** compose continuations.
```racket
(require racket/control)
(+ 1 (reset (+ 10 (shift k (k (k 1))))))   ; 22
(call-with-continuation-prompt (lambda () (abort-current-continuation (default-continuation-prompt-tag) (lambda () 'out))) (default-continuation-prompt-tag) (lambda (th) (th)))
```
- `shift` and `reset` come from `racket/control` (Danvy and Filinski's operators); `reset` marks the prompt that `shift` captures up to.
- The Guide notes that `racket/control` has operators with more convenient names than the primitive prompt functions.
## Self-check
The reset example above returns `22`.

## Checked

Date: 2026-11-02. Confirmed in the Racket Guide chapter Exceptions and Control (Exceptions and Control: prompts, `call-with-continuation-prompt`, `abort-current-continuation`, `default-continuation-prompt-tag`) and the Reference for `racket/control` (`reset`, `shift`; reduction rules give 22 for the example). Removed: the advice to prefer `racket/generator`.

Method: documentation only; no commands were run.
