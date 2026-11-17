---
id: computing-software.software-engineering.scheme-racket.number-conversion
name: number-conversion
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, number-conversion]
level: practitioner
status: docs-checked
description: "Convert between numbers and strings with string->number, number->string, real->decimal-string and ~r from racket/format, handling failure returns of #f."
sources:
  - https://docs.racket-lang.org/guide/numbers.html
  - https://docs.racket-lang.org/reference/generic-numbers.html
  - https://docs.racket-lang.org/reference/strings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing and formatting numbers
**Goal:** safe numeric text conversion.
```racket
(string->number "42")     ; 42
(string->number "x")      ; #f, not an error
(number->string 255 8)    ; "377"
(real->decimal-string pi 5)  ; "3.14159"
(require racket/format) (~r 3.14159 #:precision 2)  ; "3.14"
```
- `string->number` returns `#f` when the string does not parse exactly as a number datum (no whitespace allowed), so check for `#f` before arithmetic.
- `string->number` takes an optional `radix` from 2 to 16 (default 10); a `#b`, `#o`, `#d` or `#x` prefix in the string overrides it.
- `number->string` accepts radix 2, 8, 10 or 16; an inexact number requires radix 10 or `exn:fail:contract` is raised.
- `real->decimal-string n [digits]` prints exactly `digits` digits after the point (default 2) and needs a rational `n` (not `+inf.0` or `+nan.0`).
- `~r` is in `racket/format`: a numeric `#:precision` drops trailing zeroes, while `'(= n)` keeps exactly `n` digits.
## Self-check
`(string->number "abc")` returns `#f`.

## Checked
2026-11-08. Confirmed on the Racket Reference generic numerics page (section 4.3.2.9 Number-String Conversions: `string->number`, `number->string`, `real->decimal-string`) and the Reference strings page (`~r` `#:precision`). The Guide numbers page was read and confirms exact / inexact reading conventions but has no conversion detail. Replaced the `(number->string 255 16)` example with the documented radix-8 example and dropped the `"1e3"` bullet, whose result is not shown on these pages.
Method: documentation only; no commands were run.
