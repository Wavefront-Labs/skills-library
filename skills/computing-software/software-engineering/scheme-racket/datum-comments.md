---
id: computing-software.software-engineering.scheme-racket.datum-comments
name: datum-comments
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, datum-comments, racket-lexical]
level: intro
status: docs-checked
description: "Use line, block and datum comments in Racket source: semicolon, #"
sources:
  - https://docs.racket-lang.org/guide/syntax-overview.html
  - https://docs.racket-lang.org/reference/reader.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comments and datum comments
**Goal:** comment out code correctly.
```racket
; line comment
#| block comment, #| nests |# fine |#
(list 1 #;(expensive-call) 2)   ; => '(1 2); #; drops the next datum
```
- `#;` removes exactly one following datum (a whole parenthesised form), handy for disabling one argument or clause.
- Block comments nest in Racket; do not assume C-style non-nesting.
## Self-check
In the REPL, `(list 1 #;(/ 1 0) 2)` returns `'(1 2)` without a divide-by-zero.

## Checked

Date: 2026-11-02. Confirmed on Racket Reference Reading Comments (`#;` recursively reads one datum and discards it; `#|` block comments nest). Removed: the claim about `#;` before a closing paren.

Method: documentation only; no commands were run.
