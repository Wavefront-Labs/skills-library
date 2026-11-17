---
id: computing-software.software-engineering.scheme-racket.raco-pkg
name: raco-pkg
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, raco-pkg]
level: practitioner
status: docs-checked
description: "Install, update and publish packages with raco pkg install, update, show, remove, new and the Racket package catalog."
sources:
  - https://docs.racket-lang.org/raco/
  - https://docs.racket-lang.org/pkg/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raco pkg install and manage
**Goal:** manage dependencies.
```bash
raco pkg install --auto rackunit-lib
raco pkg show
raco pkg update --all
raco pkg install --link ./mypkg     # develop locally
raco pkg remove mypkg
```
- `--auto` installs dependencies without prompting.
- Installation scope defaults to user or installation depending on setup (`--scope`).
- Dependencies declared in `info.rkt` with `deps`.
## Self-check
Install a small package then `raco pkg show` and remove it.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
