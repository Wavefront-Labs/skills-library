---
id: computing-software.qa-testing-engineering.vitest.only-skip-todo
name: only-skip-todo
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-only, test-skip, test-todo, allow-only]
level: intro
status: docs-checked
description: "Focus, disable or stub tests with .only, .skip and .todo on test and describe, and understand the CI failure when .only is left in."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/filtering.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/test.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
describe.only('suite', () => { /* runs */ })
it.only('focused test', () => { /* runs */ })
it.skip('skipped test', () => { /* shown as skipped */ })
describe.todo('unimplemented suite')
it.todo('unimplemented test')
```

- `.only` skips every unmarked test in that file. To avoid noise from the whole suite, run the file directly: `vitest interesting.test.ts`.
- `.skip` keeps the test in the report as a reminder.
- `.todo` has no body and shows in the report as planned work. A test with no body is marked todo automatically.

CI guard: when `process.env.CI` is set, Vitest fails the run if it sees `.only`. The `allowOnly` option controls this. The `no-focused-tests` ESLint rule (also in oxlint) catches it earlier.

Skip dynamically with the context: `context.skip()` or `context.skip(condition, 'optional message')`.

## Checked

2026-11-04. Confirmed against guide/filtering.md and api/test.md: the .only, .skip and .todo behaviours, the single-file run, the CI failure with `process.env.CI` and `allowOnly`, the no-focused-tests rule in ESLint and oxlint, auto-todo for a test with no body, and context.skip.

Method: documentation only; no commands were run.
