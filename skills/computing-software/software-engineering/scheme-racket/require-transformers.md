---
id: computing-software.software-engineering.scheme-racket.require-transformers
name: require-transformers
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, require-transformers, racket-modules-advanced]
level: practitioner
status: docs-checked
description: "Control imports with only-in, except-in, rename-in, prefix-in and for-syntax, for-label phases to avoid name clashes."
sources:
  - https://docs.racket-lang.org/reference/require.html
  - https://docs.racket-lang.org/reference/module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# only-in, except-in, rename-in, prefix-in
**Goal:** resolve conflicts.
```racket
(require (prefix-in l: racket/list) (except-in racket/string string-join)
         (rename-in racket/list [first head]) (for-syntax racket/base))
```
- Forms: `(only-in spec id-or-[orig new] ...)`, `(except-in spec id ...)`, `(prefix-in prefix spec)`, `(rename-in spec [orig new] ...)`, `(combine-in spec ...)`; `for-syntax` and `for-label` wrap a spec to import at another phase or only for binding information.
- No identifier can be bound multiple times at one phase level and binding space by imports, unless all the bindings refer to the same original definition in the same module. So the same binding reached by two paths is fine; two different bindings for one name is an error.
- In a module, bindings from the module language (`#lang` or `module` path) can be shadowed by definitions and requires in the body. A definition via `define-values` or `define-syntaxes` can also shadow an import from `require`, unless a preceding `#%declare` includes `#:require=defined`; an identifier cannot otherwise be both imported and defined.
## Self-check
Import `first` twice from different modules to see the conflict message.

## Checked
2026-11-08. Confirmed against the Reference "Importing and Exporting: require and provide" section (require-spec forms, the no-duplicate-binding rule, same-definition exception) and the `module` form (module-language shadowing, definition shadowing an import, `#:require=defined`).
Removed: the claim that a definition shadows a module-language import "but not an explicit require" (the reference says definitions can shadow `require`d imports too), and the Guide module-basics page as the only source.
Method: documentation only; no commands were run.
