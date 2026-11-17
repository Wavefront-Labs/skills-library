---
id: computing-software.software-engineering.scheme-racket.quasiquote-unquote
name: quasiquote-unquote
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, quasiquote-unquote, racket-quoting]
level: intro
status: docs-checked
description: "Build list data with quasiquote, unquote and unquote-splicing, including nested levels and use as a match pattern."
sources:
  - https://docs.racket-lang.org/guide/qq.html
  - https://docs.racket-lang.org/reference/match.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quote and quasiquote
**Goal:** construct s-expressions.
```racket
`(1 ,(+ 1 1) ,@(list 3 4))   ; '(1 2 3 4)
`(1 2 `(,(+ 1 2) ,,(- 5 1))) ; '(1 2 `(,(+ 1 2) ,4))
```
- `` ` `` is `quasiquote`, `,` is `unquote` and `,@` is `unquote-splicing`. Each unquoted expression is evaluated and its value replaces the sub-form.
- `unquote-splicing` needs an expression that produces a list and must appear where a list or vector is built; the list is spliced in.
- A quasiquote inside a quasiquote cancels one layer of unquote and unquote-splicing, so a second `,` is needed to evaluate in the inner template.
- In `match`, a quasiquote pattern treats identifiers as symbols and unquote returns to ordinary patterns: ``(match x [`(add ,a ,b) (+ a b)])``.
## Self-check
`` `(1 2 ,@(list (+ 1 2) (- 5 1))) `` gives `'(1 2 3 4)`.

## Checked
2026-11-08. Confirmed on the Racket Guide section 4.11 (Quasiquoting) and Racket Reference section 9 (quasiquote patterns): evaluation of unquote, splicing rules, nested-level behaviour, the backquote / comma / `,@` shorthands and their printed results, and match quasi-patterns. Removed the "do not mutate quoted lists" advice, the `'(a . (b c))` example and the Guide eval page as a source, none of which the pages support.
Method: documentation only; no commands were run.
