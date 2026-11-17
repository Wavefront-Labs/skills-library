---
id: computing-software.software-engineering.scheme-racket.rackunit-suites
name: rackunit-suites
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, rackunit-suites]
level: practitioner
status: docs-checked
description: "Group RackUnit checks with test-case and test-suite (#:before/#:after) and run them with run-tests from rackunit/text-ui."
sources:
  - https://docs.racket-lang.org/rackunit/api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# test-case and test-suite
**Goal:** structured suites.
```racket
(require rackunit rackunit/text-ui)
(define s (test-suite "math" #:before (lambda () (void))
  (test-case "add" (check-equal? (+ 1 2) 3))))
(run-tests s)
```
- `test-case` is like `test-begin` plus a name reported on failure. If an expression in the group fails by raising an exception, the remaining expressions in that group are not evaluated.
- A `test-suite` is not run immediately; it holds checks, test cases or nested suites, and optional `#:before` and `#:after` thunks run before and after the tests.
- `run-tests` (in `rackunit/text-ui`, package `rackunit-lib`) takes a test case or suite and an optional verbosity of `'quiet`, `'normal` or `'verbose`, and returns the number of unsuccessful tests.
## Self-check
Two cases, one failing: `run-tests` reports the failure and returns a count of unsuccessful tests.
## Checked
2026-11-08. Confirmed on the RackUnit API page: `test-case`, `test-begin`, `test-suite` with `#:before`/`#:after`, `run-tests` signature, verbosity values and return value. Removed: "aborts that case only" (the page says remaining expressions in the group are skipped, and says nothing on other cases), and "one failure and one success" report wording.
Method: documentation only; no commands were run.
