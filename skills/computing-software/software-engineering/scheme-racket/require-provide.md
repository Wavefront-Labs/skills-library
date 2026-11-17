---
id: computing-software.software-engineering.scheme-racket.require-provide
name: require-provide
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, require-provide]
level: intro
status: docs-checked
description: "Organise Racket code into modules with require, provide, struct-out and only-in; relative string paths use / on every platform."
sources:
  - https://docs.racket-lang.org/guide/module-paths.html
  - https://docs.racket-lang.org/reference/require.html
  - https://docs.racket-lang.org/reference/Module_Names_and_Loading.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# require and provide
**Goal:** organise code into modules.
```racket
;; util.rkt
#lang racket/base
(provide add2 (struct-out pt))
(struct pt (x y))
(define (add2 n) (+ n 2))
;; main.rkt
#lang racket/base
(require "util.rkt" racket/list (only-in racket/string string-join))
```
- A string module path is relative to the enclosing file and uses Unix-style conventions on every platform: `/` separates elements, `..` is the parent directory, and it must not start or end with a separator.
- An unquoted identifier like `racket/list` refers to an installed library in a collection.
- `struct-out` exports the bindings of a structure type; `only-in` imports only the listed identifiers.
- Cyclic module dependencies are an error: the default module name resolver raises `exn:fail` with a dependency-cycle message.
## Self-check
Remove `struct-out` from the `provide` and confirm the `pt` accessors are no longer available in `main.rkt`.
## Checked
2026-11-08. Confirmed on the Guide module-paths page: string path rules and identifier paths; on the Reference require page: `struct-out` and `only-in`; on the Reference "Module Names and Loading" page: the dependency-cycle `exn:fail`. Removed: the claim that a module cannot `set!` an imported variable (not stated on these pages) and the specific `pt-x` unbound wording in the self-check.
Method: documentation only; no commands were run.
