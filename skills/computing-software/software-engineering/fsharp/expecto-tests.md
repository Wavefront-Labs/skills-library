---
id: computing-software.software-engineering.fsharp.expecto-tests
name: expecto-tests
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, expecto-tests, fsharp-test-frameworks, expecto, test-list]
level: practitioner
status: docs-checked
description: "Write and run tests with Expecto using testList, testCase, test builders and the runTestsWithCLIArgs entry point."
sources:
  - https://github.com/haf/expecto
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expecto
**Goal:** tests as plain values.

```fsharp
open Expecto

let tests =
    testList "math" [
        test "adds" {
            Expect.equal (1 + 1) 2 "1+1 should be 2"
        }
        testCase "simple" <| fun () ->
            Expect.equal (2 + 2) 4 "2+2 = 4"
        testAsync "async" {
            let! v = async { return 3 }
            Expect.equal v 3 "async value"
        }
    ]

[<EntryPoint>]
let main args = runTestsWithCLIArgs [] args tests
```
- Tests compile to `Test` values that you compose. Kinds: `testCase`, `testCaseAsync`, `testCaseTask`, `testList`, the `test` / `testAsync` builders, `testSequenced` and `testSequencedGroup`.
- Pending tests (not run) use a `p` prefix such as `ptestCase` or `ptest`; focused tests (the only ones run) use `f`, such as `ftestCase` or `ftest`.
- `testCaseTask` takes a function returning a Task, because tasks start immediately.
- Property tests come from the `Expecto.FsCheck` package: `testProperty`, `testPropertyWithConfig`.
- Fully qualified test names must be unique across the test project.

## Gotchas
- Tests are parallel and async by default; use `testSequenced` / `testSequencedGroup`, or pass `--sequenced` to the exe, for tests that share state or measure performance.
- If console output looks garbled under parallel runs, try `--no-spinner`.

## Checked

Method: docs-checked 2026-11-09 against https://github.com/haf/expecto README. Removed unconfirmed: Expect.throws, --filter and --list-tests flags, YoloDev.Expecto.TestSdk guidance, Expect.equal argument-order claim, exit-code claim.
