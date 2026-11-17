---
id: computing-software.software-engineering.scheme-racket.units-signatures
name: units-signatures
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, units-signatures]
level: advanced
status: docs-checked
description: "Use define-signature, define-unit, define-compound-unit/infer and define-values/invoke-unit/infer for late-linked components; prefer modules unless units are needed."
sources:
  - https://docs.racket-lang.org/guide/units.html
  - https://docs.racket-lang.org/guide/Signatures_and_Units.html
  - https://docs.racket-lang.org/guide/Invoking_Units.html
  - https://docs.racket-lang.org/guide/Linking_Units.html
  - https://docs.racket-lang.org/guide/unit_versus_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Units and signatures
**Goal:** know when units apply and how to link them.
```racket
#lang racket
(define-signature toy-factory^ (build-toys repaint toy? toy-color))
(define-unit simple-factory@
  (import) (export toy-factory^)
  (struct toy (color) #:transparent)
  (define (build-toys n) (for/list ([i (in-range n)]) (toy 'blue)))
  (define (repaint t col) (toy col)))
(define-values/invoke-unit/infer simple-factory@)
```
- `#lang racket/base` needs `(require racket/unit)`.
- Convention: signature names end with `^`, unit names end with `@`. A signature is normally defined in a module and provided; a unit names it in an `export` clause (what it implements) or `import` clause (what it needs).
- A unit importing only a signature depends on the specification, not on one implementation.
- `invoke-unit` runs a unit with no imports but does not bind its body definitions. `define-values/invoke-unit/infer` binds the identifiers of the exported signature; `/infer` means the signatures are inferred from the unit.
- Mutually dependent units are linked: `(define-compound-unit/infer both@ (import) (export toy-factory^ toy-store^) (link store-specific-factory@ toy-store@))`, then invoke `both@`. Connections are inferred from the signatures each unit imports and exports.
- The Guide's advice: use `unit` when `module` almost works but separately compiled pieces must refer to each other, or when you want a stronger interface/implementation split. A module is for managing a namespace, and module boundaries are separate-compilation boundaries that forbid mutual dependencies. Otherwise prefer modules.
## Self-check
Define two units that import each other's signature, link them with `define-compound-unit/infer`, invoke the result.

## Checked
2026-11-08. Confirmed against the Racket Guide chapter 14 pages (Units; Signatures and Units; Invoking Units; Linking Units; unit versus module): racket/unit requirement, naming conventions, form names, invoke-unit versus define-values/invoke-unit/infer, compound-unit linking, module versus unit guidance. Removed: the `(invoke-unit u (import s))` form and a bare `link` form, which are not shown in the Guide; the reference/structures source (unrelated).
Method: documentation only; no commands were run.
