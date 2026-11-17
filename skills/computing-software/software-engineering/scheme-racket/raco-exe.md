---
id: computing-software.software-engineering.scheme-racket.raco-exe
name: raco-exe
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, raco-exe]
level: practitioner
status: docs-checked
description: "Create standalone executables with raco exe and bundle runtime with raco distribute for deployment."
sources:
  - https://docs.racket-lang.org/raco/
  - https://docs.racket-lang.org/raco/exe-dist.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raco exe and raco distribute
**Goal:** ship a binary.
```bash
raco exe -o app main.rkt
raco distribute dist/ app     # bundle with needed libraries
```
- Modules loaded dynamically (`eval`, `load`, `dynamic-require`) are not embedded automatically; add them with `++lib`. Declare run-time files with `define-runtime-path`.
## Self-check
Run the executable from the distribution directory (layout varies by platform) on a machine without Racket.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
