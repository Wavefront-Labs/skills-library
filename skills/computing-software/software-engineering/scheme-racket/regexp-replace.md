---
id: computing-software.software-engineering.scheme-racket.regexp-replace
name: regexp-replace
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, regexp-replace]
level: practitioner
status: docs-checked
description: "Substitute text with regexp-replace and regexp-replace*, using numbered backreferences or a procedure for the replacement."
sources:
  - https://docs.racket-lang.org/guide/regexp.html
  - https://docs.racket-lang.org/reference/regexp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# regexp-replace and replace-star
**Goal:** rewrite text.
```racket
(regexp-replace* #px"(\\w+)@(\\w+)" "a@b c@d" "\\2:\\1")   ; "b:a d:c"
(regexp-replace* #px"\\d+" "a1b22" (lambda (m) (number->string (* 2 (string->number m)))))
```
- `&` and `\\0` mean the whole match in the insert string; escape a literal `&` as `\\&`.
- `regexp-replace` replaces only the first match.
## Self-check
Double every integer in `"a1b22"` to get `"a2b44"`.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
