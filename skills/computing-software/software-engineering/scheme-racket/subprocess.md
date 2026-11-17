---
id: computing-software.software-engineering.scheme-racket.subprocess
name: subprocess
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, subprocess]
level: practitioner
status: docs-checked
description: "Execute programs with racket/system (system, system*, process*) or subprocess, avoid shell injection by passing argument lists, and check exit codes."
sources:
  - https://docs.racket-lang.org/reference/subprocess.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running external programs
**Goal:** call other tools.
```racket
(require racket/system)
(system* (find-executable-path "echo") "hello")
(system*/exit-code (find-executable-path "ls") "-l")
```
- `system` runs through a shell string (injection risk); prefer `system*` with separate arguments.
- Capture output with `(with-output-to-string (lambda () (system* ...)))`.
## Self-check
`system*/exit-code` on a failing command returns a non-zero code.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
