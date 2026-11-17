---
id: computing-software.software-engineering.scheme-racket.submodules
name: submodules
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, submodules]
level: practitioner
status: docs-checked
description: "Embed submodules with module+ main and module+ test so scripts and tests live beside the code they exercise."
sources:
  - https://docs.racket-lang.org/reference/module.html
  - https://docs.racket-lang.org/reference/running-sa.html
  - https://docs.racket-lang.org/raco/test.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Submodules: module, module+, module*
**Goal:** co-locate entry points and tests.
```racket
#lang racket/base
(define (f x) (* 2 x))
(module+ main (displayln (f 21)))       ; runs with `racket file.rkt`
(module+ test (require rackunit) (check-equal? (f 2) 4))   ; runs with `raco test file.rkt`
```
- `module+ id form ...` declares and/or adds to a submodule: all `module+` pieces with the same name are combined in order into one `(module* id #f ....)` placed at the end of the enclosing module. A submodule must be made only of `module+` pieces or only of `module`/`module*`, not both.
- `module*` is for submodules that may require the enclosing module (with `#f` as the module path it sees the enclosing module's bindings, as `module+` does); `module` is expanded immediately and declared on its own, with its module path supplying the initial bindings; the scope of the enclosing module's imports and definitions does not cover a nested `module` or a `module*` with a non-`#f` module path.
- `racket file.rkt` requires the file and then its `main` submodule if available.
- `raco test file.rkt` requires and runs the `test` submodule by default (`-s name` picks another); if the file has none, it runs the top-level module unless `-x`/`--no-run-if-absent` is given.
## Self-check
`raco test file.rkt` runs the `test` submodule, not `main`.

## Checked
2026-11-08. Confirmed against the Reference module forms section (`module`, `module*`, `module+`) and the `raco test` and "Running Racket" pages.
Removed: the claim that submodules "cost nothing when the file is required" (not stated), and the wording that `module` cannot see the enclosing module's bindings (the docs say only that `module*` may require the enclosing module).
Method: documentation only; no commands were run.
