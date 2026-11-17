---
id: computing-software.software-engineering.scheme-racket.syntax-parse
name: syntax-parse
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, syntax-parse]
level: advanced
status: docs-checked
description: "Validate macro input with syntax/parse: syntax classes, ~optional, ~seq and #:with, giving precise error messages."
sources:
  - https://docs.racket-lang.org/syntax/stxparse-intro.html
  - https://docs.racket-lang.org/syntax/stxparse-patterns.html
  - https://docs.racket-lang.org/syntax/stxparse-specifying.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# syntax/parse patterns
**Goal:** robust macros.
```racket
(require (for-syntax racket/base syntax/parse))
(define-syntax (def-const stx)
  (syntax-parse stx
    [(_ name:id val:expr) #'(define name val)]))
```
- `name:id` annotates a pattern variable with the `id` syntax class (written `variable:class`); a non-identifier is rejected with an "expected identifier" error. The annotation does not appear in the template (`name`, not `name:id`).
- In patterns, `...` matches zero or more repetitions and `...+` one or more; only `...` may be used in the template.
- Define reusable classes with `define-syntax-class` (with `#:description`, `#:attributes`, `pattern` variants); a `#:with` clause matches a pattern against a computed term, and `#:fail-when` rejects input with a message.
- `~optional` and `~seq` are pattern forms, documented with the other pattern forms in the syntax/parse patterns chapter; when several errors are possible, the one that progressed furthest in the left-to-right traversal is reported.
- Docs: syntax/parse in the "syntax" manual.
## Self-check
`(def-const 5 1)` reports an "expected identifier" error for `5`.

## Checked
2026-11-08. Confirmed against the syntax/parse manual (introduction, pattern grammar and specifying syntax pages): `id` and `expr` classes, the colon annotation, `...+`, `define-syntax-class`, `#:description`, `#:attributes`, `#:with`, `#:fail-when`, `~optional`, `~seq`, error progress rule, and the `expected identifier` message.
Removed: the `number` syntax class (not found on the fetched pages; the library syntax class page was not readable), the Guide macros page as the only source, and the "pointing at 5" wording.
Method: documentation only; no commands were run.
