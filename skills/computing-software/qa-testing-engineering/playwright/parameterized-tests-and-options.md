---
id: computing-software.qa-testing-engineering.playwright.parameterized-tests-and-options
name: parameterized-tests-and-options
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, playwright-parameterize, data-driven-testing, option-fixtures, test-each, csv-driven-tests]
level: practitioner
status: verified
description: "Parameterize Playwright tests: loops generating tests from data, option fixtures configured per project, CSV/JSON-driven tests, and unique titles."
sources:
  - https://playwright.dev/docs/test-parameterize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameterized Playwright tests

**Goal:** run the same test logic for many data sets or configurations.

## Generate tests from data
```ts
const cases = [
  { name: 'standard', total: 100, discount: '5%' },
  { name: 'gold', total: 100, discount: '10%' },
  { name: 'gold under threshold', total: 99.99, discount: '0%' },
]
for (const c of cases) {
  test(`discount for ${c.name}`, async ({ page }) => {
    // ... use c.total and assert c.discount
  })
}
```
Titles must be unique in a file, or Playwright errors (run here: `Error: duplicate test title "dup", first declared in tags.spec.ts:9`, and nothing is listed).

## From files
```ts
import fs from 'fs'
import { parse } from 'csv-parse/sync'
const records = parse(fs.readFileSync('data/discounts.csv'), { columns: true, skip_empty_lines: true })
for (const r of records) test(`discount ${r.id}`, async ({ page }) => { ... })
```

## Project-level parameters (option fixtures)
```ts
// fixtures.ts
export type Options = { persona: string }
export const test = base.extend<Options>({ persona: ['standard', { option: true }] })
// playwright.config.ts
projects: [{ name: 'standard', use: { persona: 'standard' } },
           { name: 'gold', use: { persona: 'gold' } }]
```
Every test then runs once per persona project (run here: the same three tests ran under `[standard]` and `[gold]`, and `persona` read `standard` and `gold`). Use `mergeTests` to combine this `test` with other fixture sets.

## Environment-driven
`process.env.TENANT` read in config or tests; pass via `TENANT=acme npx playwright test`.

## Gotchas
- Test generation runs at collection time in the runner and in every worker (run here: a module-level log printed 3 times with 2 workers); keep data loading fast and deterministic (no random data in titles).
- Huge data sets at E2E level are slow; push combinatorics down to API/unit tests.

## Verify
`--list` shows one test per data row with readable titles.
