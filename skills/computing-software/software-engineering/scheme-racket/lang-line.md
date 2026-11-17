---
id: computing-software.software-engineering.scheme-racket.lang-line
name: lang-line
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, lang-line, racket-lang-line]
level: intro
status: docs-checked
description: "Start a Racket file with #lang racket or racket/base so it reads as a module; run it with racket file.rkt or raco make."
sources:
  - https://docs.racket-lang.org/guide/module-basics.html
  - https://docs.racket-lang.org/guide/module-languages.html
  - https://docs.racket-lang.org/reference/running-sa.html
  - https://docs.racket-lang.org/raco/make.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# #lang line and file structure
**Goal:** write a runnable module file.
```racket
#lang racket/base
(provide greet)
(define (greet n) (string-append "hi " n))
(module+ main (displayln (greet "bob")))
```
- `#lang X` goes at the top of the module file (every Guide example does this). The reader treats `#lang` as the start of a reader-extension use; `X` also names the module language that supplies the bindings (and the implicit forms such as `#%module-begin`).
- Run: `racket file.rkt`. With at least one argument that is not a flag, `racket` implicitly adds `-u`, which requires the file and then its `main` submodule if available. Compile ahead of time: `raco make file.rkt`, which compiles the module to bytecode (recompiling only when the source or a dependency changed).
- Other modules import a module by relative path, for example `(require "cake.rkt")`, with Unix-style relative paths on every platform.
## Self-check
Create the file above, run `racket file.rkt`, see `hi bob`.

## Checked
2026-11-08. Confirmed against the Racket Guide "Module Basics" and "Module Languages" sections, the Reference "Running Racket" page (`-u`, `-t`, implicit `-u`, `main` submodule), the Reference reader dispatch table (`#lang`), and the raco make overview.
Removed: "must be the first line", "writes `compiled/`", and the claim about what `racket` does with a file lacking `#lang` (none are stated on the fetched pages).
Method: documentation only; no commands were run.
