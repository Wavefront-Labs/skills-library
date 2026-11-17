---
id: computing-software.software-engineering.scheme-racket.class-definitions
name: class-definitions
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, class-definitions, racket-classes]
level: advanced
status: docs-checked
description: "Define classes with class%, fields, methods, init arguments, super-new, and call methods with send."
sources:
  - https://docs.racket-lang.org/guide/classes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# class, new and send
**Goal:** use the class system.
```racket
(require racket/class)   ; needed under #lang racket/base
(define counter%
  (class object%
    (init [start 0])
    (define n start)
    (super-new)
    (define/public (inc!) (set! n (add1 n)) n)))
(send (new counter%) inc!)
```
- A `class` expression is a first-class value; by convention class names end with `%` and the root class is `object%`. `new` takes initialization arguments by name, e.g. `(new counter% [start 5])`.
- An `init` argument is optional when it declares a default, as in `(init [start 0])`. Init arguments are available only during instantiation, so copy the value into a field (here `n`) for methods to use.
- A class must always invoke its superclass's initialization with `(super-new)`. The order of init, field and `(super-new)` forms sets evaluation order during instantiation: a field whose initial value calls a method must come after `super-new`.
- `define/public` introduces a public method. A method is not an independent function: call it with `(send obj method args ...)`.
- A public field is declared with `field`, e.g. `(field [size 10])`.
- A missing method on `send` is only signalled when the `send` is evaluated; declaring `(inherit m)` signals the error when the class is created and allows a direct call `(m ...)`, which the Guide prefers.
## Self-check
`(send (new counter% [start 5]) inc!)` returns `6`.

## Checked
2026-11-08. Read in full: Racket Guide chapter 13 Classes and Objects (guide/classes.html), sections 13.1 Methods through the mixins, traits and class contracts sections, with the class, init, super-new, define/public, send, inherit, field and racket/base require statements confirmed. Removed `send/apply` and `send*` (not mentioned on the page) and the over-broad "public only via define/public" claim. Added the `racket/class` require, which the page says is needed under `#lang racket/base`.
Method: documentation only; no commands were run.
