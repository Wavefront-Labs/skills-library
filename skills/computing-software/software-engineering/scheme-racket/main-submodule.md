---
id: computing-software.software-engineering.scheme-racket.main-submodule
name: main-submodule
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, main-submodule]
level: practitioner
status: docs-checked
description: "Implement script entry with (module+ main ...) and read current-command-line-arguments or command-line."
sources:
  - https://docs.racket-lang.org/guide/Module_Syntax.html
  - https://docs.racket-lang.org/reference/runtime.html
  - https://docs.racket-lang.org/reference/Command-Line_Parsing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# main submodule and command-line entry
**Goal:** runnable scripts that are also libraries.
```racket
(module+ main
  (define args (current-command-line-arguments))
  (printf "~a args\n" (vector-length args)))
```
- When a module is given to the `racket` executable (or run in DrRacket) and has a `main` submodule, that submodule runs after the enclosing module. Requiring the module as a library does not run it.
- `module+` is like `module*` with `#f` as the initial module path, and several `module+` forms with the same name are combined into one submodule.
- `current-command-line-arguments` is a parameter holding a vector of strings: the command-line arguments that were not treated as system flags.
- For flags, use `command-line` (from `racket/cmdline` or `racket`, not `racket/base`); it defaults its `#:argv` to `(current-command-line-arguments)`, treats strings starting with `-` or `+` as flags, and stops flag parsing at the first non-flag argument or at `--`.
## Self-check
`racket file.rkt x y` prints `2 args`.

## Checked
2026-11-08. Confirmed in the Racket Guide "Main and Test Submodules" section (read through a page fetch of that section, not a full-page read), the Racket Reference runtime page (`current-command-line-arguments`) and the command-line parsing page (`command-line` library, default `#:argv`, flag rules). Removed the Guide module-basics source, which does not mention `main`, and the unsupported "prefer command-line" wording, replaced with the documented behaviour.
Method: documentation only; no commands were run.
