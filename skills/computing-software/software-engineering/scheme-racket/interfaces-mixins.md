---
id: computing-software.software-engineering.scheme-racket.interfaces-mixins
name: interfaces-mixins
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, interfaces-mixins]
level: advanced
status: docs-checked
description: "Declare interfaces with interface, override or augment methods, and compose behaviour with mixins as functions from class to class."
sources:
  - https://docs.racket-lang.org/guide/classes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interfaces, inheritance and mixins
**Goal:** reusable object behaviour.
```racket
(define printable<%> (interface () show))
(define (loud-mixin %) (class % (super-new) (define/override (show) (string-upcase (super show)))))
```
- `(interface (superinterface-expr ...) id ...)` declares an interface (for example `(interface () get-size grow eat)` in the Guide).
- Mixin: a `class` expression nested in a function of its superclass, e.g. `(define picky-fish% (picky-mixin fish%))`. Composition is function application: `(hungry-mixin (picky-mixin fish%))`.
- `define/override` makes the mixin require that the base class already has the method (an error is signaled when the mixin is applied if not); `(inherit eat)` likewise enforces a method-existence requirement and is preferred over `send this`.
- A method declared `pubment` can only be augmented (`augment`, with `inner` in the superclass); `augride` and `overment` switch between override and augment modes.
- `is-a?` takes an object and a class or interface (instance of the class or a derived class, or class implements the interface); `implementation?` checks a class against an interface, so a mixin can test `(implementation? % grower-interface)` on its argument.
## Self-check
`(is-a? obj printable<%>)` is `#t` for an object whose class implements the interface.

## Checked
2026-11-08. Confirmed against the Racket Guide "Classes and Objects" chapter (interfaces, mixins, `define/override`, `inherit`, `super-new`, augmentation forms, `is-a?`, `implementation?`).
Removed: nothing substantive; claims were tightened to what the chapter states and the unsupported implication that `inherit` is only needed "as needed" was replaced by the documented method-existence behaviour.
Method: documentation only; no commands were run.
