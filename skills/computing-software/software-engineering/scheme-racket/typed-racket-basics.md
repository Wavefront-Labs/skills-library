---
id: computing-software.software-engineering.scheme-racket.typed-racket-basics
name: typed-racket-basics
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, typed-racket-basics, racket-typed-lazy]
level: advanced
status: docs-checked
description: "Annotate with #lang typed/racket, : declarations, U unions and All polymorphism; require/typed at the typed-untyped boundary installs contracts by default."
sources:
  - https://docs.racket-lang.org/ts-guide/quick.html
  - https://docs.racket-lang.org/ts-guide/beginning.html
  - https://docs.racket-lang.org/ts-guide/types.html
  - https://docs.racket-lang.org/ts-guide/occurrence-typing.html
  - https://docs.racket-lang.org/ts-guide/typed-untyped-interaction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typed Racket basics
**Goal:** add static types to a Racket module.
```racket
#lang typed/racket
(struct pt ([x : Real] [y : Real]))
(: distance (-> pt pt Real))
(define (distance p1 p2)
  (sqrt (+ (sqr (- (pt-x p2) (pt-x p1)))
           (sqr (- (pt-y p2) (pt-y p1))))))
(: list-length (All (A) (-> (Listof A) Integer)))
(define (list-length l) (length l))
(define-type Tree (U leaf node))
```
- Porting steps: change the language to `typed/racket`, change `(require mod)` to `(require typed/mod)`, annotate structure definitions and top-level definitions. The program is type-checked before it runs; a type error stops it running.
- `typed/racket/base` corresponds to `racket/base`. The older `define:`-style forms with a `:` suffix are legacy only; use plain `struct`, `define` and `let` with annotations.
- Unions are `(U t1 t2 ...)`; `All` binds type variables for polymorphic functions; `define-type` names a type.
- Occurrence typing: after `(string? x)` succeeds, `x` has type `String` in the then branch, and the other union members in the else branch. Predicates carry propositions, e.g. `string?` has type `(-> Any Boolean : String)`.
- REPL: `racket -I typed/racket`; evaluating a name prints its type, and `:print-type` prints only the type.
- Untyped module used from typed code: `(require/typed "file.rkt" [#:struct pt ([x : Real] [y : Real])] [distance (-> pt pt Real)])`. Do not use `require/typed` between two typed modules; plain `require` works. Untyped code can require typed modules freely, except it may not use macros defined in typed modules.
- Boundary protection: Deep types (default `typed/racket`) use contracts; Shallow (`typed/racket/shallow`) use cheaper shape checks; Optional (`typed/racket/optional`) enforce nothing at run time. Contract cost is highest for higher-order values such as `Vectorof`, `->` and `Object`.
## Self-check
`(add1 "not a number")` is rejected with a "Type Checker: type mismatch" error.

## Checked
2026-11-08. Confirmed against the Typed Racket Guide pages Quick Start, Beginning Typed Racket, Types in Typed Racket, Occurrence Typing and Typed-Untyped Interaction: language names, porting steps, U/All/define-type, the legacy colon-suffix forms, string? proposition type, require/typed rules, Deep/Shallow/Optional behaviour, `racket -I typed/racket` and `:print-type`. Removed: `define:` as a current form (the guide calls it legacy); the lazy docs source (unrelated).
Method: documentation only; no commands were run.
