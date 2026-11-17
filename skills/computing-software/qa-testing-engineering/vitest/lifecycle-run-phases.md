---
id: computing-software.qa-testing-engineering.vitest.lifecycle-run-phases
name: lifecycle-run-phases
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-lifecycle, setup-files, hook-order, run-phases]
level: advanced
status: docs-checked
description: "Order of a Vitest run: init, global setup, worker creation, setupFiles, collection, execution, reporting, global teardown, plus hook order inside a file."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/lifecycle.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Phases, in order:
1. Init: config loaded in the main process.
2. `globalSetup` runs in the main process.
3. Workers are created per the pool settings; by default they are not reused, so each file gets an isolated one.
4. `setupFiles` run before each test file. They run in parallel by default; `sequence.setupFiles` changes that.
5. Collection and execution of the file.
6. Reporting.
7. Global teardown.

Hook order inside a file: `aroundAll`, `beforeAll`, `aroundEach`, `beforeEach`, the test, `afterEach`, cleanup returned from `beforeEach`, `onTestFinished`, `onTestFailed` (on failure), `afterAll`, cleanup returned from `beforeAll`.

Use `setupFiles` to initialise global state or configuration before each test file, and keep them light because they run before every file. Use `globalSetup` for expensive once-per-run work such as seeding a database or starting a server.

Watch mode does not rerun global setup; teardown runs at exit. Use `project.onTestsRerun` in the global setup to react to reruns.

## Checked

2026-11-04. Confirmed against guide/lifecycle.md: the phase order, worker reuse rules, parallel setup files and `sequence.setupFiles`, the hook order including cleanups, `onTestFinished` and `onTestFailed`, global teardown in watch mode, and the performance advice. Replaced the example uses for setup files (custom matchers, global mocks), which the page does not give.

Method: documentation only; no commands were run.
