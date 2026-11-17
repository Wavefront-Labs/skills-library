---
id: computing-software.software-engineering.scheme-racket.rackunit-submodule-test
name: rackunit-submodule-test
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, rackunit-submodule-test]
level: practitioner
status: docs-checked
description: "Put RackUnit tests in a (module+ test ...) submodule and run them with raco test; know -s, -r and -x options."
sources:
  - https://docs.racket-lang.org/raco/test.html
  - https://docs.racket-lang.org/reference/module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tests in a test submodule
**Goal:** idiomatic test layout.
```racket
(module+ test
  (require rackunit)
  (check-equal? (f 2) 4))
```
- `module+` declares and/or adds to a submodule; all `module+` pieces with the same name are combined and moved to the end of the enclosing module.
- `raco test` requires and runs the `test` submodule (by default) of each path given. `-s <name>` or `--submodule <name>` runs another submodule instead.
- If the relevant submodule is absent, `raco test` requires the top-level module by default (`-r`/`--run-if-absent`); `-x`/`--no-run-if-absent` ignores such files.
- `raco test` sets the current directory to the test file's directory before running it.
## Self-check
Add a `(module+ test ...)` block, run `raco test file.rkt` and confirm the checks run.
## Checked
2026-11-08. Confirmed on the raco test page: default `test` submodule, `-s`, `-r`, `-x`, and the working-directory behaviour; on the Reference module page: `module+` semantics. Removed: the rackunit page as a source (stub), the claim that plain `racket file.rkt` skips the submodule (not stated on these pages), and the `rackunit-lib` / `build-deps` info.rkt advice (the raco test page documents info.rkt test configuration separately and it was not verified here).
Method: documentation only; no commands were run.
