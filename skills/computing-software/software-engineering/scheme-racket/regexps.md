---
id: computing-software.software-engineering.scheme-racket.regexps
name: regexps
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, regexps, racket-regexps]
level: practitioner
status: docs-checked
description: "Match text with #rx, #px, regexp-match, regexp-match*, regexp-match? and capture groups; #px adds the digit, word and boundary classes."
sources:
  - https://docs.racket-lang.org/guide/regexp.html
  - https://docs.racket-lang.org/reference/regexp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# regexp-match and pregexp
**Goal:** pattern matching on strings.
```racket
(regexp-match #px"(\\d+)-(\\d+)" "tel 12-34")   ; '("12-34" "12" "34")
(regexp-match* #px"\\d+" "a1b22")               ; '("1" "22")
(regexp-match? #rx"^a" "abc")
(regexp-split #rx"," "a,b")
```
- In `#rx` syntax `\d` is not a class; use `#px` or `[0-9]`.
- Backslashes need doubling in string literals.
- A failed match returns `#f`.
## Self-check
`(regexp-match #px"\\d+" "abc")` is `#f`.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
