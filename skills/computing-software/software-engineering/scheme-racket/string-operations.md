---
id: computing-software.software-engineering.scheme-racket.string-operations
name: string-operations
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, string-operations]
level: intro
status: docs-checked
description: "Common Racket string tasks with racket/string: string-split, string-join, string-replace, string-trim, substring; literals are immutable."
sources:
  - https://docs.racket-lang.org/guide/strings.html
  - https://docs.racket-lang.org/guide/symbols.html
  - https://docs.racket-lang.org/reference/strings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String operations
**Goal:** common string tasks.
```racket
(require racket/string)
(string-split " foo bar baz \r\n\t")  ; '("foo" "bar" "baz")
(string-join '("a" "b") ", ")         ; "a, b"
(string-replace "foo bar baz" "bar" "blah") ; "foo blah baz"
(string-trim " foo bar baz \r\n\t")   ; "foo bar baz"
(substring "Apple" 1 3)               ; "pp"
```
- `racket/string` is not provided by `racket/base`.
- Strings from the default reader (literals) are immutable; `make-string` and `string-copy` give mutable strings. `string-set!` on an immutable string raises `exn:fail:contract`.
- `string-split` with no separator splits on whitespace (`#px"\\s+"`) and trims first; `(string-split " ")` is `'()`.
- `string-join` defaults to a single space separator; `string-replace` replaces all occurrences by default and matches a string `from` literally.
## Self-check
`(string-join (string-split "a b  c") "_")` gives `"a_b_c"`.
## Checked
2026-11-08. Confirmed on the Reference strings page: the `racket/string` section note, signatures, defaults and examples for `string-split`, `string-join`, `string-replace` and `string-trim`, the immutability rules, `make-string`, `string-copy` and `substring`. Removed: the unexemplified `(string-split "a,b,,c" ",")` result comment and the original `"a_b"`/`"el"` example outputs, replaced by the manual's own examples.
Method: documentation only; no commands were run.
