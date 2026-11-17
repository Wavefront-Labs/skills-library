---
id: computing-software.qa-testing-engineering.playwright.annotations-tags-and-grep
name: annotations-tags-and-grep
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, test-annotations, test-tags, grep, test-skip, test-fixme, test-slow, test-fail]
level: practitioner
status: verified
description: "Control Playwright test execution with annotations (skip, fixme, fail, slow), tags and grep filtering, test.step reporting and custom annotations for traceability."
sources:
  - https://playwright.dev/docs/test-annotations
  - https://playwright.dev/docs/api/class-test
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright annotations, tags and grep

**Goal:** select, skip and describe tests without editing test bodies.

## Annotations
```ts
test.skip(({ browserName }) => browserName === 'webkit', 'Feature not in Safari')   // conditional skip at file or describe level (run here: the file's test was skipped)
test('upload large file', async ({ page }) => {
  test.slow()                     // triples timeout
  ...
})
test.fixme('broken after redesign', async () => {})   // not run, reported as skipped
test.fail('known bug PAY-321', async ({ page }) => {})  // must fail; passes if it fails
test('refund', { annotation: { type: 'issue', description: 'https://jira/PAY-123' } }, async () => {})
```
`test.describe.configure({ mode: 'serial', retries: 1 })` per group.

## Tags
```ts
test('checkout works', { tag: ['@smoke', '@checkout'] }, async ({ page }) => {})
test.describe('admin', { tag: '@admin' }, () => { ... })
```
```bash
npx playwright test --grep @smoke
npx playwright test --grep "@smoke|@checkout"
npx playwright test --grep-invert @slow
```
Or per project: `grep: /@smoke/` in config.

## Steps
```ts
await test.step('add to basket', async () => { ... })   // nested steps show in report and trace
```
`test.step(..., { box: true })` reports errors at the step call site (run here the stack began at the `test.step.box` call, not inside the step body).

## Gotchas
- `test.fail` tests passing unexpectedly fail the run (`Expected to fail, but passed.`): good signal that the bug is fixed; remove the annotation.
- Skips without a reason or ticket become permanent; review `fixme`/`skip` counts.

## Verify
`npx playwright test --grep @smoke --list` lists exactly the intended tests (run here: `--grep @smoke`, `--grep "@smoke|@checkout"`, `--grep @admin` for a describe-level tag, and `--grep-invert @slow` selected the expected tests; a tag written as an `@slow` token in the title is matched too). Tags must start with `@` (docs).
