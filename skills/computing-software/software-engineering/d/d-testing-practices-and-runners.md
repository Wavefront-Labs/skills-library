---
id: computing-software.software-engineering.d.d-testing-practices-and-runners
name: d-testing-practices-and-runners
category: computing-software
field: software-engineering
product: d
tags: [d-testing-practices-and-runners, unit-tests, test-runner, unit-threaded, silly, test-organisation, ci-testing, version-unittest, fixtures, d]
level: practitioner
status: draft
description: "Structure larger D test suites: separate test modules, version(unittest) helpers, unit-threaded/silly runners, running single modules and CI settings."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test organisation, fixtures and runners

Goal: scale from a few asserts to a maintained suite.

- Keep unittests next to the code for small units; for integration tests make `tests/` and a dub `configuration "tests"` with `sourcePaths "tests"` and `dependency "unit-threaded"`.
- Runners: dub's default runner stops at the first failure; `silly` (add as test dependency, no code change) runs each block, reports names and timing; `unit-threaded` adds test discovery, fixtures, mocking and a CLI to filter tests.
- Use `@("name")` UDAs to label tests; shared setup via helper functions and `scope(exit)` cleanup; temp dirs via `std.file.tempDir` and `std.uuid`.
- Run one file quickly: `rdmd -unittest -main -I=source source/foo.d`.
- CI: `dub test --compiler=ldc2` plus `dub build -b release`; run on dmd, ldc2 for portability.
- Property tests: random inputs with `std.random` using a fixed seed (`Random(42)`) so failures reproduce.

Gotchas:
- Tests that touch real clock/network become flaky; inject `Clock` or temp files.
- A `main` in the library breaks `dub test`; keep it behind `version(unittest) {} else`.

Verify: introduce a failing test and confirm the runner names it.
