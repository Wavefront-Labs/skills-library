---
id: computing-software.software-engineering.scheme-racket.raco-make
name: raco-make
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, raco-make, racket-raco]
level: intro
status: docs-checked
description: "Compile modules ahead of time with raco make to bytecode."
sources:
  - https://docs.racket-lang.org/raco/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raco make and compiled output
**Goal:** precompile.
```bash
raco make main.rkt          # compile main and its dependencies
```
- See the raco make chapter of the raco manual for options and the bytecode and dependency files it writes.
## Self-check
Run before/after `raco make` and compare load time.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
