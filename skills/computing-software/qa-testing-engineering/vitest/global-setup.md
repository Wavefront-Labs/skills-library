---
id: computing-software.qa-testing-engineering.vitest.global-setup
name: global-setup
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [global-setup, project-provide, global-teardown, inject-values]
level: advanced
status: docs-checked
description: "Run once-per-run Vitest setup and teardown in the main process with globalSetup, and share values with tests through project.provide."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/lifecycle.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/config/globalsetup.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/projects.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`globalSetup` modules run once in the main process, before workers exist. Export `setup(project)` and optionally `teardown`, or a `default` function that returns a teardown function. Setup runs before workers are created and only if at least one test is queued; teardown runs after all test files finish (in watch mode, before the process exits).

```ts
// global-setup.ts
import type { TestProject } from 'vitest/node'

export async function setup(project: TestProject) {
  project.provide('baseUrl', 'http://localhost:3000')
}

export async function teardown() {
  // stop what setup started
}
```

Register it with `globalSetup: ['./global-setup.ts']` in the test config.

`project.provide(key, value)` shares serialisable values with tests (read them with `inject`). A fixture marked `injected: true` can be overridden from the project `provide` config.

- The root `globalSetup` is not inherited by projects.
- Watch mode does not rerun it; use `project.onTestsRerun(async () => {...})` to react to reruns. Do not destructure `onTestsRerun` from `project`.
- Global setup runs in a different global scope from the tests, so tests cannot read variables defined there. For code in the same process as the tests use `setupFiles`, which runs before every test file.
- Multiple global setup files run `setup` in order and `teardown` in reverse order.

## Checked

2026-11-04. Confirmed against config/globalsetup.md (export forms, timing, `provide` and `inject`, `onTestsRerun`, ordering), guide/lifecycle.md (main process scope, no rerun in watch mode), guide/projects.md (root `globalSetup` not inherited) and guide/test-context.md (`injected: true`). Replaced a claim about test-file mocks not applying, which the pages do not state.

Method: documentation only; no commands were run.
