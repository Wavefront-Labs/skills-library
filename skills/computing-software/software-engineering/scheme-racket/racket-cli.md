---
id: computing-software.software-engineering.scheme-racket.racket-cli
name: racket-cli
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, racket-cli]
level: intro
status: docs-checked
description: "Run code with racket file.rkt, -e, -l, -t and -i flags, pass arguments, and know the default module and REPL behaviour."
sources:
  - https://docs.racket-lang.org/reference/running-sa.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# racket command-line flags
**Goal:** run Racket from a shell.
```bash
racket main.rkt a b        # run module with args
racket -e '(displayln (+ 1 2))'
racket -l racket/base -e '(displayln 1)'
racket -i                  # REPL
racket -t main.rkt -i      # require then REPL
racket --version
```
- `-e <expr>` evaluates and prints results via `current-print`; `-t <file>` requires the file, then its `main` submodule if available; `-l <path>` requires `(lib "<path>")`, then its `main` submodule if available; `-i` or `--repl` starts the REPL; `-v` or `--version` shows the banner.
- If at least one argument is given and the first non-configuration one is not a flag, `-u` (require as a script) is added before it; `-u` is like `-t` plus setting the program name and treating later arguments as non-flags.
- With no arguments other than configuration options, `-i` is effectively added.
- The exit status is non-zero if an error occurs during a command-line eval, load or require, but only when no REPL is started.
## Self-check
`racket -e '(+ 1 2)'` prints `3`.
## Checked
2026-11-08. Confirmed on the Reference "Running Racket" page (running-sa): the flags `-e`, `-t`, `-l`, `-i`/`--repl`, `-v`/`--version`, `-u`, implicit `-u` and `-i`, and exit-status behaviour. Removed: the raco page as a source (it documents raco, not the racket flags), and the phrase that a lone file is "required, then the program exits" (rewritten to the documented implicit `-u`).
Method: documentation only; no commands were run.
