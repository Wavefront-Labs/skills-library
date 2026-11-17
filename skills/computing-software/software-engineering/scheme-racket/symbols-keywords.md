---
id: computing-software.software-engineering.scheme-racket.symbols-keywords
name: symbols-keywords
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, symbols-keywords]
level: intro
status: docs-checked
description: "Use symbols for identifiers and enum values (eq?-comparable) and keywords for named arguments; convert with symbol->string and string->symbol."
sources:
  - https://docs.racket-lang.org/guide/symbols.html
  - https://docs.racket-lang.org/reference/symbols.html
  - https://docs.racket-lang.org/reference/keywords.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Symbols and keywords
**Goal:** pick symbol or string.
- `(eq? 'abc 'abc)` is `#t`; symbols read by the reader or made with `string->symbol` are interned (one symbol per character sequence), so `eq?` is a cheap comparison for tags and enumerations. Case matters: `(eq? 'a 'A)` is `#f`.
- `gensym` and `string->uninterned-symbol` return fresh uninterned symbols, not `eq?` to any other symbol even if they print the same; useful as fresh tags. Two calls of `string->uninterned-symbol` with the same string give distinct symbols.
- `symbol-interned?` tests whether a symbol is interned.
- Keywords `#:k` are a separate type: `(keyword? '#:apple)` is `#t`, `(keyword? 'define)` is `#f`. Convert with `keyword->string` and `string->keyword`.
## Self-check
`(symbol->string 'abc)` is `"abc"`; `(eq? (string->symbol "a") 'a)` is `#t`; `(eq? 'a (string->uninterned-symbol "a"))` is `#f`.

## Checked
2026-11-08. Confirmed against the Guide "Symbols" section and the Reference symbols and keywords pages: interning, `eq?` examples, `gensym`, `string->uninterned-symbol`, `symbol-interned?`, `keyword?`, `keyword->string`, `string->keyword`.
Removed: the claim about how `(string->symbol "has space")` prints (not on the pages) and the strings pages as sources.
Method: documentation only; no commands were run.
