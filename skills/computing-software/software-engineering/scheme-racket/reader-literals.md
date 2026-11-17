---
id: computing-software.software-engineering.scheme-racket.reader-literals
name: reader-literals
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, reader-literals]
level: intro
status: docs-checked
description: "Recognise Racket reader syntax: booleans, characters, byte strings, #rx/#px regexps, #:keywords, #hash, vectors #(...) and quote shorthands."
sources:
  - https://docs.racket-lang.org/guide/syntax-overview.html
  - https://docs.racket-lang.org/reference/reader.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reader literals and quote shorthands
**Goal:** read literal data without guessing.
| Written | Means |
|---|---|
| `#t #true #f #false` | booleans |
| `#\a #\space #\λ #\u3BB` | characters (`#\λ` and `#\u3BB` are the same character) |
| `#"abc"` | byte string |
| `#rx"a+"` `#px"\\d+"` | regexp, pregexp |
| `#:key` | keyword (for `#:key` arguments) |
| `#(1 2 3)` | literal vector |
| `#hash((a . 1))` | immutable hash table with `equal?` key matching (`#hasheq` for `eq?`) |
| `'x` `` `x `` `,x` `,@x` | quote, quasiquote, unquote, unquote-splicing |
| `#'x` `` #`x `` `#,x` `#,@x` | syntax, quasisyntax, unsyntax, unsyntax-splicing |
- `[ ]` and `{ }` read as lists exactly like `( )` when matched; a mismatched closer raises `exn:fail:read`. Setting `read-square-bracket-as-paren` (and the tag variant) to `#f` turns square brackets into read errors.
- A delimited `.` between two data makes a pair: `(1 . 3)` reads as `(cons 1 3)`. Three or more data with `.` around a middle element reads as infix: `(1 . 2 . 3)` reads as `(list 2 1 3)`.
- `#true` and `#false` are the long forms of `#t` and `#f`.
## Self-check
`'apple` reads as `(list 'quote 'apple)`; `'(1 . 3)` equals `(cons 1 3)`; `'(1 . (3))` equals `(list 1 3)`.

## Checked
2026-11-08. Confirmed against the Reference "The Reader" chapter: the dispatch table (`#t`/`#f`, `#(`, `#"`, `#:`, `#rx`, `#px`, `#hash`, square and curly brackets), boolean syntax including `#true`/`#false`, `#\space` and `#\λ` character examples, immutable `equal?`-based `#hash`, quote prefixes, pair and infix-dot rules.
Removed: `#λ` as a character literal (the syntax is `#\λ`), the "convention uses brackets in let and cond" remark (style advice not in the reference), and vector and `hash-ref` self-check results that the page does not state.
Method: documentation only; no commands were run.
