---
id: computing-software.software-engineering.scheme-racket.parameter-guards
name: parameter-guards
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, parameter-guards]
level: advanced
status: docs-checked
description: "Add a guard procedure to make-parameter to validate or convert, and use built-ins like current-output-port, current-directory and current-command-line-arguments."
sources:
  - https://docs.racket-lang.org/reference/parameters.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guards and built-in parameters
**Goal:** validated parameters.
```racket
(define n (make-parameter 1 (lambda (v) (if (exact-integer? v) v (error 'n "int")))))
(parameterize ([current-output-port (open-output-string)]) (display "hi"))
```
- Guard result becomes the stored value, so it can normalise input.
- The guard is not applied to the initial value; it runs when the parameter is later set (`parameterize` or direct call).
## Self-check
`(parameterize ([n 'x]) (n))` raises the guard's error.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
