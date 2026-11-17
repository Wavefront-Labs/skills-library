---
id: computing-software.software-engineering.scheme-racket.eval-namespaces
name: eval-namespaces
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, eval-namespaces]
level: practitioner
status: docs-checked
description: "Evaluate data as code with eval in an explicit namespace (make-base-namespace); use racket/sandbox for untrusted input."
sources:
  - https://docs.racket-lang.org/guide/eval.html
  - https://docs.racket-lang.org/reference/Namespaces.html
  - https://docs.racket-lang.org/reference/Sandboxed_Evaluation.html
  - https://docs.racket-lang.org/reference/pairs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# eval and namespaces
**Goal:** run constructed code with an explicit namespace.
```racket
(define ns (make-base-namespace))
(eval '(+ 1 2) ns)                  ; 3
(parameterize ([current-namespace ns]) (eval '(* 2 3)))
(namespace-require 'racket/list ns)
```
- `eval` takes a quoted form or syntax object and an optional namespace; otherwise it uses `current-namespace`. It cannot see local bindings of the context where it is called.
- When a module is run directly, the initial current namespace is empty, so `(eval '(cons 1 2))` in a module fails. The Guide's advice: create a namespace explicitly with `(make-base-namespace)` (initialised with the exports of `racket/base`) and pass it to `eval`.
- `(namespace-require quoted-raw-require-spec [namespace])` performs the import in the namespace's top-level environment; `namespace` defaults to `(current-namespace)`.
- `module->namespace` reflects a module into a namespace; inside a module use `define-namespace-anchor` and `namespace-anchor->namespace`.
- `racket/sandbox` (package sandbox-lib, not `racket/base`) provides `make-evaluator` for sandboxed evaluators with restricted memory and time, filesystem and network access; defaults are very limited. `sandbox-memory-limit` (default 30 MB) and `sandbox-eval-limits` set limits.
- Advice: do not `eval` raw user text in an unrestricted namespace.
## Self-check
`(eval '(first '(1 2)) ns)` fails until `racket/list` is required into `ns`, because `first` is provided by `racket/list`, not `racket/base`.

## Checked
2026-11-08. Read in full: Racket Guide 15.1 eval (guide/eval.html), including Namespaces and Namespaces and Modules. Read in the Racket Reference the `make-base-namespace`, `make-base-empty-namespace` and `namespace-require` entries (reference/Namespaces.html), the opening, `make-evaluator`, `sandbox-memory-limit` and `sandbox-eval-limits` entries of 14.12 Sandboxed Evaluation, and the `racket/list` header and `first` entry in reference/pairs.html (these long pages were searched and read at those entries only). Replaced the over-broad "modules have no top-level namespace" with the Guide's exact statement about the initial namespace, added the sandbox library requirement and limits, and replaced the guide/qq source (quasiquote, unrelated).
Method: documentation only; no commands were run.
