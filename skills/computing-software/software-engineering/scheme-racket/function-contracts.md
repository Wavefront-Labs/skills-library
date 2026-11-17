---
id: computing-software.software-engineering.scheme-racket.function-contracts
name: function-contracts
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, function-contracts, racket-contracts]
level: practitioner
status: docs-checked
description: "Specify procedure behaviour with ->, ->*, ->i and case-> contracts guarding arguments and results."
sources:
  - https://docs.racket-lang.org/guide/contracts-general-functions.html
  - https://docs.racket-lang.org/reference/function-contracts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function contracts: -> and ->*
**Goal:** guard function boundaries.
```racket
(require racket/contract)
(define/contract (maybe-invert i b)
  (-> integer? boolean? integer?)
  (if b (- i) i))
(provide
 (contract-out
  [string-pad-center (->* (string? natural-number/c) (char?) string?)]
  [max-abs (-> real? real? ... real?)]))
```
- `(-> dom ... range)` is for a fixed number of arguments with a result contract independent of the inputs; a domain `...` allows arbitrarily many more arguments matching the contract before it. Keywords go in the domain (`(-> integer? #:invert? boolean? integer?)`).
- `->*` syntax is `(->* (mandatory ...) (optional ...) rest pre range post)`: first group mandatory, second group optional, last the result. Rest arguments use `#:rest`, e.g. `(->* (real?) () #:rest (listof real?) real?)`. Keywords are allowed in both groups.
- `->i` names each argument and result so later contracts can depend on earlier ones, and supports pre- and post-conditions; `case->` matches `case-lambda` functions.
- Cost ordering from the reference: `->` is the cheapest, `->*` needs packaging arguments as lists, `->i` is the most expensive.
- A default value for an optional argument is not checked by the contract at that interface.

## Self-check
`(maybe-invert #f 1)` raises a contract violation naming the 1st argument and `integer?`; the docs' REPL example shows `blaming: top-level`, the caller.

## Checked
2026-11-08. Confirmed against the Racket Guide section "Contracts on Functions in General" and Reference section 8.2 Function Contracts: `->`, `->*` group structure, `#:rest`, keyword domains, `->i` dependent contracts, `case->`, the cost ordering, `define/contract` violation output and blame.
Removed: `and/c`, `not/c` and `#:n` keyword-in-`contract-out` example (not on the fetched pages) and the claim that `->*` is written `(->* (mandatory) (optional) result)` only; the full syntax is stated above.
Method: documentation only; no commands were run.
