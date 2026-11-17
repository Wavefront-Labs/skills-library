---
id: computing-software.software-engineering.scheme-racket.datum-to-syntax
name: datum-to-syntax
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, datum-to-syntax]
level: advanced
status: docs-checked
description: "Use datum->syntax to give a new identifier the lexical context of existing syntax, for intentional capture, and know the syntax-parameter alternative."
sources:
  - https://docs.racket-lang.org/guide/stx-obj.html
  - https://docs.racket-lang.org/reference/stxops.html
  - https://docs.racket-lang.org/guide/with-syntax.html
  - https://docs.racket-lang.org/reference/stxparam.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# datum->syntax and intentional capture
**Goal:** introduce bindings visible to user code.
```racket
(define-syntax (aif stx)
  (syntax-case stx ()
    [(k c t e) (with-syntax ([it (datum->syntax #'k 'it)])
                 #'(let ([it c]) (if it t e)))]))
```
- `(datum->syntax ctxt v [srcloc prop ignored])` converts the datum `v` to syntax; converted objects get the lexical context of `ctxt` (a syntax object or `#f`) and the source location of `srcloc`. If `v` is already a syntax object it is returned unmodified. Here `#'k`, the macro keyword at the use site, donates its context so `it` is visible to the user's `t` and `e`.
- `with-syntax` binds pattern variables (the left-hand side is a pattern, as in `syntax-case`), which is how the computed `it` identifier is spliced into the template.
- Alternative: syntax parameters from `racket/stxparam` (not `racket/base`): `define-syntax-parameter` plus `syntax-parameterize` binds `it` only inside the macro's expansion; the reference's own `aif` example uses `(syntax-parameterize ([it (syntax-id-rules () [_ t])]) ...)`.
- Advice: document any identifiers a macro captures.
## Self-check
`(aif (assq 'a '((a . 1))) (cdr it) 0)` returns `1`.

## Checked
2026-11-08. Read in full: Racket Guide 16.2.1 Syntax Objects (guide/stx-obj.html), 16.2.4 with-syntax and generate-temporaries (guide/with-syntax.html), and Racket Reference 12.5 Syntax Parameters (reference/stxparam.html). From Reference 12.2 Syntax Object Content (reference/stxops.html) read the `datum->syntax` entry only (the page was searched, not read end to end). Confirmed the signature, defaults and lexical-context behaviour, the `racket/stxparam` library and its `aif` example. The `aif` macro above is a deduction from those rules, not a documented example, and the old "prefer syntax parameters" advice was reworded as an alternative. Replaced the guide/macros index source.
Method: documentation only; no commands were run.
