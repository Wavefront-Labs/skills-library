---
id: computing-software.software-engineering.nim.unittest-suites-and-checks
name: unittest-suites-and-checks
category: computing-software
field: software-engineering
product: nim
tags: [unittest-suites-and-checks, unit-testing, unittest, suite, test, check, require, expect, setup, teardown, nimble-test, nim]
level: practitioner
status: docs-checked
description: "Write tests with suite and test blocks, check, require and expect, and select tests by name on the command line."
sources:
  - https://nim-lang.org/docs/unittest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unittest: suite, test, check and expect

Goal: structure automated tests.

```nim
import std/unittest
suite "math":
  setup:
    var x = 2
  test "add":
    check x + 2 == 4
  test "raises":
    expect ValueError:
      discard parseInt("z")
```
- `check expr` records failure and continues, showing sub-expression values; `require expr` aborts the test; `fail()`, `skip()`.
- `expect E1, E2:` asserts an exception type is raised.
- Selective run: pass test names as arguments, `nim c -r tests/t1.nim "math::add"`; `"fast_suite::mytest*"` and `"auth*::"` (all tests of matching suites) wildcards work.
- Output level is the `OutputLevel` enum (`PRINT_FAILURES` prints only failed tests); `-d:nimUnittestAbortOnError:on` quits at the first failure.
- Compiled test files exit with 0 when all tests pass and 1 on failure.

Gotchas:

Verify: a failing check shows the expression values and the test binary exits with 1.

## Checked

2026-11-03. Confirmed against the unittest page: suite, test, setup, check, require, expect, fail, skip, name filters with `::` and wildcards, OutputLevel/PRINT_FAILURES, nimUnittestAbortOnError, exit codes 0 and 1. Removed: `-d:unittest2Compat`, `-d:nimUnittestOutputLevel`, `-d:nimUnittestColor`, the `NIMTEST_*` list, unittest2, nimble test naming rules and the module-level check gotcha (not on the page).

Method: documentation only; no commands were run.
