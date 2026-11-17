---
id: computing-software.software-engineering.scheme-racket.module-begin
name: module-begin
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, module-begin]
level: advanced
status: docs-checked
description: "Override #%module-begin, #%app and #%datum to alter module-level behaviour in a language; understand how each wraps forms."
sources:
  - https://docs.racket-lang.org/guide/module-languages.html
  - https://docs.racket-lang.org/reference/application.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# #%module-begin, #%app and #%datum
**Goal:** control implicit forms.
- `#%module-begin` is an implicit form that wraps the body of a module; a module used as a module language must provide it. Redefining it is the most frequently useful of these: the Guide shows an alternate `#%module-begin` that removes `provide` and quasiquote boilerplate in an HTML-description language, and a lambda-calculus language whose `#%module-begin` accepts a single expression.
- `#%app` is the implicit form for function calls (the expander converts `(proc arg ...)` to `(#%app proc arg ...)`), `#%datum` is for literals, and `#%top` is for identifiers with no binding. They exist mainly so a module language can restrict or change the meaning of implicit uses; they rarely need redefining.
- Export your versions under the standard names (for example with `(rename-out [module-begin #%module-begin])`) from the language module.
## Self-check
Write a language module that provides `lambda`, `#%module-begin`, `#%app` and `#%datum`, then redefine `#%datum` to reject literals and confirm a literal now errors with `#%datum: no`, as in the Guide's lambda-calculus example.

## Checked
2026-11-08. Confirmed against the Racket Guide "Module Languages" section and the Reference "Procedure Applications and #%app" section.
Removed: suggestions to override `#%module-begin` to print results or inject checks, `#%app` for tracing, and wrapping numbers in a struct via `#%datum` (plausible uses, but the docs do not describe them).
Method: documentation only; no commands were run.
