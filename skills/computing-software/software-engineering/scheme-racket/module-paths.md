---
id: computing-software.software-engineering.scheme-racket.module-paths
name: module-paths
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, module-paths]
level: practitioner
status: docs-checked
description: "Racket module path forms: relative strings, collection ids, (lib ...), (file ...), (submod ...); where collections are found."
sources:
  - https://docs.racket-lang.org/guide/module-paths.html
  - https://docs.racket-lang.org/guide/module-basics.html
  - https://docs.racket-lang.org/reference/require.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module path forms
**Goal:** resolve the right module.
| Form | Meaning |
|---|---|
| `"x.rkt"` | relative to the enclosing file (Unix-style `/` separators) |
| `racket/list` | installed library: collection `racket`, file `list.rkt` |
| `(file "/abs/x.rkt")` | file, using the platform's path conventions; not portable |
| `(lib "racket/list")` | like the identifier form, written as a string |
| `(submod "x.rkt" test)` | submodule `test` of that module |
| `(submod "." test)` | submodule of the current module |
- An id with no `/` gets `/main` added, so `racket` means `racket/main`; `.rkt` is added automatically to identifier and `(lib ...)` forms unless the string ends in a file suffix.
- Collections are searched in the installation's `collects` directory, the user-specific collects directory, directories in the `PLTCOLLECTS` search path, and, most typically, installed packages.
- Within one project, relative paths are preferred over collection paths; `raco exe` treats filesystem-path modules differently from collection-path modules.
## Self-check
`(require (submod "x.rkt" test))` requires the `test` submodule of `x.rkt`; confirm that `(lib "racket/list")` and `racket/list` give the same bindings.
## Checked
2026-11-08. Confirmed on the Guide Module Paths and Module Basics pages and the Reference require page: all path forms in the table, `/main` and `.rkt` defaults, collection search locations, and the relative-path advice. Removed: the `(find-system-path ...)` and `define-runtime-path` data-file advice and the claim that requiring the submodule "loads the test submodule only" (neither is stated on the cited pages).
Method: documentation only; no commands were run.
