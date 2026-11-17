---
id: computing-software.qa-testing-engineering.vitest.describe-suites
name: describe-suites
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [describe, suite-options, describe-shuffle, nested-suites]
level: intro
status: docs-checked
description: "Group Vitest tests with describe or suite, pass inherited options like timeout, and use skip, only, todo, runIf, skipIf, shuffle, concurrent and each on suites."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/describe.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/lifecycle.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { describe, expect, test } from 'vitest'

describe('math', { timeout: 10_000 }, () => {
  test('adds', () => { expect(1 + 1).toBe(2) })

  describe('nested', () => {
    test('inherits the timeout', () => {})
  })
})
```

`describe` and `suite` are the same. Options set on a suite (for example `timeout`) are inherited by nested suites and their tests.

Variants mirror `test`:
- `describe.skip`, `describe.only`, `describe.todo`
- `describe.skipIf(cond)`, `describe.runIf(cond)`
- `describe.concurrent` (see concurrent-tests)
- `describe.shuffle`, or the `shuffle` option, randomises test order inside the suite
- `describe.each(table)` and `describe.for(table)` to generate suites from data

`shuffle` is inherited by nested suites and can be switched off inside with `{ shuffle: false }`; the order depends on `sequence.seed`. `{ concurrent: false }` opts a nested suite out of inherited concurrency. `describe.todo('name')` shows an entry in the report.

The `describe` callback runs immediately during test collection (code in it is not deferred until tests run), so put setup and side effects in hooks.

## Checked

2026-11-04. Confirmed against api/describe.md (alias, options inheritance, skip, skipIf, runIf, only, todo, concurrent, shuffle, each, for) and guide/lifecycle.md (describe bodies run during collection). Removed a claim about suite names joined with a separator in `-t` filters, which the pages do not state.

Method: documentation only; no commands were run.
