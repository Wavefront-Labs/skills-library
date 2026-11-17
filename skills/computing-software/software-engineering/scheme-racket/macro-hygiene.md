---
id: computing-software.software-engineering.scheme-racket.macro-hygiene
name: macro-hygiene
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, macro-hygiene]
level: practitioner
status: docs-checked
description: "Rely on hygiene so macro-introduced names do not capture user variables; recognise when hygiene must be deliberately broken."
sources:
  - https://docs.racket-lang.org/guide/pattern-macros.html
  - https://docs.racket-lang.org/reference/stxops.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macro hygiene
**Goal:** understand name capture rules.
```racket
(define-syntax-rule (my-or a b) (let ([t a]) (if t t b)))
(let ([t 5]) (my-or #f t))   ; 5, hygiene keeps t distinct
```
- Racket's pattern-based macros automatically maintain lexical scope. The Guide's `swap` macro (template binding `tmp`) used as `(swap tmp other)` expands as if the template's `tmp` were renamed (`tmp_1`), so the result is `(6 5)` rather than `(5 6)`.
- The same holds for free identifiers in a template: with a local `set!` binding at the use site, `(swap set! other)` still works, because the template's `set!` is not captured.
- So macro authors can reason about variable references in macros and macro uses the way they do for functions and function calls.
- To deliberately give introduced code the lexical context of another syntax object, use `datum->syntax ctxt v`: the converted result gets the lexical context of `ctxt` (see syntax-case).
## Self-check
Predict and test `(let ([t 5]) (my-or #f t))`: the macro's `t` is distinct from the user's, so the result is `5`.

## Checked
2026-11-08. Confirmed against the Racket Guide section on pattern-based macros and lexical scope (the `swap` expansions with `tmp_1` and `set!_1`) and the Reference entry for `datum->syntax`.
Removed: the scope-set wording for pattern variables and template bindings, and the claim that `datum->syntax` is the only way to break hygiene (the pages do not say so). The `my-or` result follows from the same renaming rule as `swap`; it is not an example printed in the docs.
Method: documentation only; no commands were run.
