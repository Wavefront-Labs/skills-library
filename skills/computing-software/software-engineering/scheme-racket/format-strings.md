---
id: computing-software.software-engineering.scheme-racket.format-strings
name: format-strings
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, format-strings]
level: practitioner
status: docs-checked
description: "Format output with printf/format directives ~a ~s ~v ~e and the racket/format helpers ~a ~r with padding and precision."
sources:
  - https://docs.racket-lang.org/reference/Writing.html
  - https://docs.racket-lang.org/reference/strings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# format, printf and racket/format
**Goal:** produce formatted text.
```racket
(format "~a has ~s items~n" "list" 3)
(require racket/format)
(~a 5 #:width 4 #:align 'right #:pad-string "0")  ; "0005"
(~r 3.14159 #:precision 2)  ; "3.14"
```
- `~a` displays, `~s` writes (strings keep their quotes), `~v` prints, `~e` uses the error value conversion handler, `~n` or `~%` is a newline, `~~` is a tilde.
- A `~` that is not one of the documented escapes raises `exn:fail:contract`, as does supplying fewer or more arguments than the format string uses.
- `racket/format` (also provided by `racket`, not `racket/base`) has `~a`, `~v`, `~s`, `~e` and `~r`, which return strings. `~a` pads or truncates with `#:min-width`, `#:max-width` or `#:width`; `#:align` is `'left` (default), `'center` or `'right`; `#:pad-string` sets the padding.
- `~r` `#:precision` is the number of digits after the decimal point (default 6); a plain number drops trailing zeroes, while `'(= n)` keeps exactly `n` digits.
## Self-check
`(format "~s ~a" "x" "x")` is `"\"x\" x"`.

## Checked
2026-11-08. Confirmed on the Racket Reference Writing page (`fprintf` / `printf` / `format` escapes and error conditions) and the Reference strings page, section 4.4.7 (`racket/format`: `~a` keywords, defaults and padding rules, `~v`, `~s`, `~e`, `~r` precision semantics). The `"0005"` and `"3.14"` examples follow from those rules. Replaced the Guide strings and symbols pages as sources, since the directives and options are documented in the Reference pages.
Method: documentation only; no commands were run.
