---
id: computing-software.software-engineering.scheme-racket.match-patterns
name: match-patterns
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, match-patterns, racket-match]
level: intro
status: docs-checked
description: "Destructure values with match using literals, identifiers, list, cons, vector and ? predicate patterns with and/or guards."
sources:
  - https://docs.racket-lang.org/guide/match.html
  - https://docs.racket-lang.org/reference/match.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# match patterns
**Goal:** replace nested conditionals.
```racket
(require racket/match)
(match v
  [(list 'add a b) (+ a b)]
  [(cons h _) h]
  [(? string? s) (string-length s)]
  [(and n (? number?) (app add1 m)) m]
  [_ 'other])
```
- Clauses are tried in order; if none matches, `exn:misc:match?` is raised. Use `_` as the catch-all: `else` is not a keyword in `match`, and using it as a pattern binds a variable named `else`, which can break `cond` and `case` in the clause body.
- A repeated identifier in one pattern must match values that are the same under `(match-equality-test)`, default `equal?`. Use `(== val)` to match against an existing variable instead of binding.
- `(list a ...)` matches any length and binds `a` to a list; `..k` means k or more.
- `(? pred pat ...)` tests a predicate then the extra patterns; `(app proc pat ...)` matches the result of applying `proc`; `#:when expr` after a pattern adds a guard.
- `racket/match` is provided by `racket` but not `racket/base`.
## Self-check
`(match '(1 2 3) [(list a ...) a])` returns `'(1 2 3)`.

## Checked
2026-11-08. Confirmed on the Racket Guide Pattern Matching page and Racket Reference section 9 (pattern grammar and descriptions of `list`, `cons`, `vector`, `?`, `app`, `and`, `or`, ellipsis and `..k`, `_`, `else`, `==`, `#:when`, `exn:misc:match?`, `match-equality-test` default `equal?`, and the racket/match provider note). Removed the exact error text `match: no matching clause`, which the pages do not give.
Method: documentation only; no commands were run.
