---
id: computing-software.software-engineering.scheme-racket.syntax-rules-ellipsis
name: syntax-rules-ellipsis
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, syntax-rules-ellipsis]
level: practitioner
status: docs-checked
description: "Use define-syntax with syntax-rules for multiple patterns, literal keywords and ... repetition, including nested ellipses."
sources:
  - https://docs.racket-lang.org/guide/pattern-macros.html
  - https://docs.racket-lang.org/reference/stx-patterns.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# syntax-rules, literals and ellipses
**Goal:** multi-clause pattern macros.
```racket
(define-syntax my-cond
  (syntax-rules (else)
    [(_ [else e ...]) (begin e ...)]
    [(_ [c e ...] rest ...) (if c (begin e ...) (my-cond rest ...))]))
```
- The form is `(syntax-rules (literal-id ...) [pattern template] ...)`; `define-syntax-rule` is a macro that expands to `define-syntax` with `syntax-rules` and a single pattern.
- A literal id matches a syntax object that is an identifier with the same binding (`free-identifier=?`), not the same spelling.
- `pattern ... ` matches zero or more elements and binds the variable at an incremented depth; a variable of depth n may appear in a template only under at least n ellipses, never fewer (an error is raised), while deeper use iterates over the innermost ellipses.
- `(... template)` makes ellipses in the template literal; the Guide's `define-cbr` example emits a literal `...` with `(... ...)`.
## Self-check
`(my-cond [#f 1] [else 2])` returns `2`: the first clause fails (`#f` is not `else`), the second expands to `(if #f (begin 1) (my-cond [else 2]))`.

## Checked
2026-11-08. Confirmed against the Racket Guide pattern-based macros pages (`syntax-rules` form, multiple patterns, `(... ...)` in `define-cbr`) and the Reference syntax-case and syntax-rules entries (literals match by binding, ellipsis depth rules, `(ellipsis template)` escape).
Removed: the wording "the same ellipsis depth as in the pattern" (the reference allows deeper use, forbids shallower), and the Guide macros overview as a source.
Method: documentation only; no commands were run.
