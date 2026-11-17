---
id: computing-software.software-engineering.scheme-racket.contract-blame
name: contract-blame
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, contract-blame]
level: practitioner
status: docs-checked
description: "Interpret contract violation blame (broke its own contract), positive and negative parties, and boundaries between modules."
sources:
  - https://docs.racket-lang.org/guide/contract-boundaries.html
  - https://docs.racket-lang.org/reference/attaching-contracts-to-values.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading blame messages
**Goal:** locate the offender.
- A message of the form "broke its own contract / promised: ... / produced: ..." means the party providing the value (the positive party) failed to meet the contract.
- A "contract violation / expected: ... / given: ... / in: the 1st argument of ..." message followed by `blaming: top-level` (or another context) means the value passed in did not meet a negative position of the contract. The page's own `define/contract` example shows this with a string passed to a `real?` argument.
- With `contract-out`, modules are the units of blame: the providing module meets the positive (co-variant) positions and each importing module must obey the negative (contra-variant) positions.
- With `define/contract`, the definition is responsible for the positive positions and the surrounding context for the negative ones.
- `(contract contract-expr to-protect-expr positive-blame-expr negative-blame-expr)` takes any values as the party names; they are formatted as by `display`. Optional extra arguments give a value name and a source location.
## Self-check
Run `(contract integer? #f 'pos 'neg #f #f)`: the output says it broke its own contract, promised `integer?`, produced `#f`, blaming `pos`. Then call a `define/contract` function with a bad argument and see the `expected:`/`given:` form.

## Checked
2026-11-08. Read in full: Racket Guide 7.1 Contracts and Boundaries (guide/contract-boundaries.html). Read in the Racket Reference 8.6 Attaching Contracts to Values (reference/attaching-contracts-to-values.html) the `contract-out`, `define/contract` and `contract` entries with their example error output (not the whole page). Corrected the quoted message to "broke its own contract" (the page prints that wording, not "broke its contract"), replaced the vague "client/server" reading with the page's positive/negative party definitions, and removed the unread reference/contracts index source. The `'server`/`'client` names in the old text are arbitrary blame values, not special names.
Method: documentation only; no commands were run.
