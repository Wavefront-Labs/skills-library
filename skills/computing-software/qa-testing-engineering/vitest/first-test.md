---
id: computing-software.qa-testing-engineering.vitest.first-test
name: first-test
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [first-test, test-file-naming, test-script, run-once]
level: intro
status: docs-checked
description: "Write and run a first Vitest test: file naming with .test. or .spec., the package.json test script, vitest run for a single pass, and reading the summary."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```js
// sum.test.js
import { expect, test } from 'vitest'
import { sum } from './sum.js'

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3)
})
```

By default a test file must contain `.test.` or `.spec.` in its name.

Add a script, then run it with your package manager:

```json
{ "scripts": { "test": "vitest" } }
```

The summary prints `Test Files  1 passed (1)`, `Tests  1 passed (1)`, start time and duration.

`vitest` alone stays in watch mode in development. To run once without watching, use `vitest run`. Extra flags work too, such as `--reporter` or `--coverage`. List every option with `npx vitest --help`.

With Bun as package manager, run `bun run test`: plain `bun test` runs Bun's own test runner.

## Checked

2026-11-04. Confirmed against guide/index.md: the sum example, `.test.` or `.spec.` naming, the `test` script, the printed summary lines, `vitest run`, extra flags, `npx vitest --help`, the Bun warning. Removed a closing line about the `globals` option, which this page does not mention.

Method: documentation only; no commands were run.
