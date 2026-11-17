---
id: computing-software.software-engineering.scheme-racket.match-struct-list
name: match-struct-list
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, match-struct-list]
level: practitioner
status: docs-checked
description: "Match struct instances with (struct-name field ...) patterns, hash and regexp patterns, and nested lists."
sources:
  - https://docs.racket-lang.org/guide/match.html
  - https://docs.racket-lang.org/reference/match.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching structs and nested data
**Goal:** deconstruct records.
```racket
(require racket/match)
(struct pt (x y))
(match (pt 1 2) [(pt x y) (+ x y)])
(match (hash 'a 1) [(hash 'a v) v])
(match "x12" [(regexp #rx"x([0-9]+)" (list _ n)) n])
(match '((1 . a) (2 . b)) [(list (cons k v) ...) k])
```
- `(struct-id pat ...)` or `(struct struct-id (pat ...))` matches an instance with one pattern per field; `(struct struct-id _)` matches any instance. The id must be bound to struct type information, as `struct` provides.
- `(hash key-expr pat ... ...)` matches a hash table; by default every key in the table must be matched, `#:open` allows extra keys, and `hash*` is open by default and supports `#:default`. The `hash` and `hash*` patterns were added in Racket 8.11.1.10; `hash-table` is deprecated.
- `(regexp rx pat)` matches a string against the regexp and then matches the `regexp-match` result against `pat`; a string `rx` is converted with `regexp`.
- Quasi-patterns use `` ` `` with `,pat` for sub-patterns, for example `` `(,a . ,b) ``.
## Self-check
`(match '((1 . a) (2 . b)) [(list (cons k v) ...) k])` returns `'(1 2)`.

## Checked
2026-11-08. Confirmed on the Racket Reference section 9 pattern grammar: struct patterns, `(struct struct-id _)`, `hash` / `hash*` modes and the 8.11.1.10 change note, deprecated `hash-table`, `regexp` with a result pattern, `cons` and `list` with ellipsis, and quasi-patterns. Replaced the deprecated `hash-table` example with `hash`. Removed the `struct-out` export claim and the arity-error self-check, which the pages do not state.
Method: documentation only; no commands were run.
