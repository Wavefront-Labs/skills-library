---
id: computing-software.software-engineering.scheme-racket.lazy-require
name: lazy-require
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, lazy-require]
level: advanced
status: docs-checked
description: "Defer module loading until first call with racket/lazy-require; know how dynamic-require interacts with raco exe."
sources:
  - https://docs.racket-lang.org/reference/lazy-require.html
  - https://docs.racket-lang.org/guide/module-basics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lazy-require and dynamic-require
**Goal:** load modules on demand.
```racket
(require racket/lazy-require)
(lazy-require [racket/list (partition)])
(partition even? '(1 2 3 4 5))   ; '(2 4) and '(1 3 5)
```
- `lazy-require` defines each listed function so that calling it dynamically requires the export from the module and calls it with the same arguments. Write `[orig-fun-id fun-id]` to rename.
- Loading triggered by a lazily required function also registers an indirect compilation dependency (`register-external-module`).
- `lazy-require-syntax` is the macro version and is only worth it for macros with exceptionally large compile-time components; it needs a runtime-support/compiler/interface module split (see the manual).
- `raco exe` treats modules referenced through filesystem paths differently from collection paths: a `dynamic-require` of a module that resolves relative to a filesystem path can fail in an executable built elsewhere. The Guide's example is `(dynamic-require 'candy/db/lookup #f)`.
## Self-check
Call a function defined via `lazy-require` and confirm the module's top-level output appears only on the first call (the manual's `hello` example prints "starting hello server" first).
## Checked
2026-11-08. Confirmed on the Reference lazy-require page: the `lazy-require` form, rename syntax, `register-external-module` behaviour, `lazy-require-syntax` guidance, and the `partition` example; on the Guide module-basics page: the `raco exe` and `dynamic-require` caveat. Removed: the claim that `lazy-require` registers modules for `raco exe` via `define-runtime-module-path-index` (the page says that happens only when the enclosing phase level is not 0), the "cut startup time" and "break cyclic dependencies" motivations, and the unverified `(dynamic-require 'racket/list 'shuffle)` call.
Method: documentation only; no commands were run.
