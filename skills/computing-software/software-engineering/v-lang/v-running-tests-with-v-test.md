---
id: computing-software.software-engineering.v-lang.v-running-tests-with-v-test
name: v-running-tests-with-v-test
category: computing-software
field: software-engineering
product: v-lang
tags: [v-running-tests-with-v-test, testing, v test, -stats, test runner, test filter, run_only, ci, parallel tests, coverage, v-lang]
level: practitioner
status: draft
description: "Run directories or files with v test, use -stats, filter by name, run in parallel and wire tests into CI."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running tests with v test

Goal: run and report tests in dev and CI.

- `v test .` (recursively finds `_test.v`), `v test mymod/`, `v mymod/mymod_test.v` or `v run file_test.v`.
- Verbosity: `v -stats test .` prints per-test timings and asserts; `-silent` hides passing output.
- Filter functions: `VTEST_ONLY=test_add v test .` (env var, confirm) or `v -test-runner ...` variants (confirm).
- Compile-time options: `v -prod test .`, `v -g test .` (symbols for debugging), `v -enable-globals test .`.
- Parallel: V's test runner compiles/executes files concurrently; use `VJOBS=4` to cap (confirm).
- CI: `v fmt -verify .`, `v vet .`, `v test .`; exit code non-zero on failure.

Gotchas:
- Files with `fn main` are run as normal programs, not tests, in `v test`.
- Tests relying on cwd should resolve paths via `@VMODROOT`/`@DIR`-style constants (confirm names).

Verify: introduce a failing assert and confirm exit code 1.
