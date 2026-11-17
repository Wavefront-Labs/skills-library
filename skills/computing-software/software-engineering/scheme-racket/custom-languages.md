---
id: computing-software.software-engineering.scheme-racket.custom-languages
name: custom-languages
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, custom-languages]
level: practitioner
status: docs-checked
description: "Make a small module language with a custom #%module-begin, use it through #lang s-exp, and build a reader layer with syntax/module-reader."
sources:
  - https://docs.racket-lang.org/guide/module-languages.html
  - https://docs.racket-lang.org/guide/syntax_module-reader.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining a module language and a #lang
**Goal:** make a small language.
```racket
;; main.rkt
#lang racket/base
(provide (rename-out [mb #%module-begin]) #%datum #%app)
(define-syntax-rule (mb body ...) (#%module-begin (displayln 'start) body ...))
```
- A module language is the initial-import module of a module; it must provide `#%module-begin`, and the other implicit forms `#%app` (function calls), `#%datum` (literals) and `#%top` (unbound identifiers) if the body uses them. Leaving `#%module-begin` out gives the error "no #%module-begin binding in the module's language".
- Redefining `#%module-begin` is the commonly useful one; the Guide's `html.rkt` example uses `(provide (except-out (all-from-out racket) #%module-begin) (rename-out [module-begin #%module-begin]))`.
- Reuse a base language's bindings with `all-from-out`, and adjust them with `except-out` and `rename-out`.
- `#lang s-exp module-name` followed by forms is the same as `(module name module-name form ...)`, with `name` derived from the source file.
- For a reader layer, write a module in `#lang s-exp syntax/module-reader` whose first form after the header is the module language; `#lang reader "that-file.rkt"` then uses it. Optional keyword specifications such as `#:read` and `#:read-syntax` come before any helper requires.
## Self-check
A file in the same directory starting `#lang s-exp "main.rkt"` (even with an empty body) prints `start` when run.

## Checked
2026-11-08. Read in full: Racket Guide 17.1 Module Languages (guide/module-languages.html) and 17.3.3 Using #lang s-exp syntax/module-reader (guide/syntax_module-reader.html); also the 17.3 section intro, which is only a list of subsections. Confirmed the implicit-form requirements and the missing-`#%module-begin` error text, the `#lang s-exp` equivalence and the `syntax/module-reader` usage. Removed the claim `(module reader syntax/module-reader mylang)` in `lang/reader.rkt` (the Guide does not show that form here) and the unsupported "all-from-out racket/base" example. The `start` self-check is a deduction from the macro, not a documented output. Replaced the guide/languages index source.
Method: documentation only; no commands were run.
