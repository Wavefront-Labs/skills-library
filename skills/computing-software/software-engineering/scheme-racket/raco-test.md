---
id: computing-software.software-engineering.scheme-racket.raco-test
name: raco-test
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, raco-test]
level: intro
status: docs-checked
description: "Run tests with raco test on files, directories or packages; it executes each file's test submodule."
sources:
  - https://docs.racket-lang.org/raco/
  - https://docs.racket-lang.org/pkg/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# raco test
**Goal:** run unit tests.
```bash
raco test file.rkt
raco test -p mypkg
raco test -j 4 dir/        # parallel jobs
raco test -c mycoll        # test the contents of a collection
```
- Exit status is non-zero on failures, so use it in CI.
- If a file has no `test` submodule, `raco test` requires the module itself by default (`-r`); `-x` ignores such files.
## Self-check
Introduce a failing `check-equal?` and confirm exit code 1.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
