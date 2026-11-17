---
id: computing-software.software-engineering.scheme-racket.truthiness
name: truthiness
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, truthiness]
level: intro
status: docs-checked
description: "Only #f is false in Racket; empty list, 0, \"\" and void are all true, so use explicit predicates."
sources:
  - https://docs.racket-lang.org/guide/conditionals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Booleans and truthiness
**Goal:** avoid C-style truthiness bugs.
- `(if '() 'yes 'no)` is `'yes`; test emptiness with `null?`.
- `(if 0 ...)` takes the true branch.
- Search functions (`member`, `assoc`, `hash-ref` with `#f` default) return `#f` for miss but a list or value for hit; `(member x l)` returns a tail, not `#t`.
- Convert to strict boolean: `(and v #t)`.
## Self-check
`(if (member 0 '(0)) 'found 'no)` is `'found`.

## Checked

Date: 2026-11-02. Confirmed on Racket Guide Conditionals (every value other than `#f` counts as true; `member` returns the list tail or `#f`). Fixed sources (the equality page does not cover truthiness). Removed: the `empty?` mention.

Method: documentation only; no commands were run.
