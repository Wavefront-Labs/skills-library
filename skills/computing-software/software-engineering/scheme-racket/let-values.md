---
id: computing-software.software-engineering.scheme-racket.let-values
name: let-values
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, let-values]
level: practitioner
status: docs-checked
description: "Bind multiple values with let-values and let*-values; splicing-let from racket/splicing exposes bindings to module scope."
sources:
  - https://docs.racket-lang.org/guide/let.html
  - https://docs.racket-lang.org/reference/let.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# let-values and splicing forms
**Goal:** destructure multiple returns locally.
```racket
(let-values ([(q r) (quotient/remainder 17 5)]) (list q r))
```
- `(require racket/splicing)` provides `splicing-let` and `splicing-let-values`, which are like `let` and `let-values`.
## Self-check
`(let-values ([(q r) (quotient/remainder 17 5)]) (list q r))` gives `'(3 2)`.

## Checked

Date: 2026-11-02. Confirmed on the Racket Reference (`let-values`, `racket/splicing` forms `splicing-let` and `splicing-let-values`) and the Guide's use of `quotient/remainder` to produce two values. Removed: the claim about helpers staying private while public names are defined.

Method: documentation only; no commands were run.
