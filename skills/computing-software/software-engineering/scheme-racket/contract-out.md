---
id: computing-software.software-engineering.scheme-racket.contract-out
name: contract-out
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, contract-out]
level: practitioner
status: docs-checked
description: "Choose between contract-out at module boundaries and define/contract for nested boundaries, including struct exports and where checking happens."
sources:
  - https://docs.racket-lang.org/guide/contract-boundaries.html
  - https://docs.racket-lang.org/reference/attaching-contracts-to-values.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# contract-out versus define/contract
**Goal:** put contracts where they belong.
- `contract-out` goes in a `provide` and treats modules as units of blame. Only uses of the contracted variable outside the providing module are checked; inside the providing module no contract checking occurs.
- `define/contract` treats the single definition as a contract region: references to the id from outside the definition must meet the negative positions, but references inside the definition are not checked (a recursive function's contract is not rechecked on each recursive call).
- The Guide encourages contracts mainly at module boundaries; nested boundaries from `define/contract` can have unexpected performance implications or blame a party that seems unintuitive.
- Under `#lang racket/base`, `(require racket/contract)` first.
- Struct export: `(contract-out (struct pt ([x real?] [y real?])))`. All fields and their contracts must be listed, and the exported struct name also acts as a constructor unless `#:omit-constructor` is given.
- `(rename internal-id external-id contract-expr)` exports under another name; `contract-expr`s are evaluated at the end of the module, so they can refer to later definitions.
## Self-check
Call the function from inside its module with a bad argument; no violation under `contract-out`. Call it from a client module and get a violation.

## Checked
2026-11-08. Read in full: Racket Guide 7.1 Contracts and Boundaries (guide/contract-boundaries.html). Read in the Racket Reference 8.6 Attaching Contracts to Values (reference/attaching-contracts-to-values.html) the `contract-out`, `define/contract` and `contract` entries (not the whole page): module-as-unit-of-blame wording, the "no contract checking inside the providing module" sentence, the struct and rename forms, and the define/contract region wording with its recursive `fact` example. Corrected the old claim that `define/contract` "checks every internal call too": the page says references inside the definition are not checked. Replaced the unread reference/contracts index source.
Method: documentation only; no commands were run.
