---
id: computing-software.qa-testing-engineering.playwright.custom-reporter
name: custom-reporter
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [playwright, custom-reporter, playwright-reporters, reporter-api, ontestend, slack-notifications]
level: practitioner
status: docs-checked
description: "Write a Playwright custom reporter with the Reporter API (onBegin, onTestEnd, onEnd) to push results to dashboards or chat, and combine it with built-in reporters."
sources:
  - https://playwright.dev/docs/api/class-reporter
  - https://playwright.dev/docs/test-reporters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playwright custom reporter

**Goal:** send results where your team looks (test management tool, metrics DB, chat) without parsing files.

## Built-in reporters first
`list`, `line`, `dot`, `html`, `json`, `junit`, `blob`, `github` (annotations in GitHub Actions). Several at once:
```ts
reporter: [['list'], ['html', { open: 'never' }], ['junit', { outputFile: 'results/junit.xml' }], ['./reporters/metrics.ts']]
```

## Custom reporter
```ts
// reporters/metrics.ts
import type { Reporter, FullConfig, Suite, TestCase, TestResult, FullResult } from '@playwright/test/reporter'

export default class MetricsReporter implements Reporter {
  private rows: any[] = []
  onBegin(config: FullConfig, suite: Suite) { console.log(`Running ${suite.allTests().length} tests`) }
  onTestEnd(test: TestCase, result: TestResult) {
    this.rows.push({
      title: test.titlePath().join(' > '), project: test.parent.project()?.name,
      status: result.status, outcome: test.outcome(),   // 'flaky' when passed on retry
      duration: result.duration, retry: result.retry,
      tags: test.tags, annotations: test.annotations,
    })
  }
  async onEnd(result: FullResult) {
    const flaky = this.rows.filter(r => r.outcome === 'flaky').length
    await fetch(process.env.METRICS_URL!, { method: 'POST', body: JSON.stringify({ status: result.status, flaky, rows: this.rows }) })
  }
  printsToStdio() { return false }
}
```

## Gotchas
- `onTestEnd` is called when a test run has finished and each retry has its own `TestResult` (`result.retry`); dedupe by test and use `test.outcome()` (`'skipped'`, `'expected'`, `'unexpected'`, `'flaky'`) for the final status.
- Sending data once from `onEnd` (called once after all tests finished) keeps the reporter simple.
- If the reporter prints nothing to the terminal, implement `printsToStdio()` and return `false`; Playwright then adds one of the standard terminal reporters alongside it.
- Custom reporters receive `onlyFailures: true` in their constructor options when `--reporter-only-failures` is set.

## Verify
Run with a forced flaky test (`--retries=1` and a test failing once): your reporter records it as flaky.

## Checked

2026-10-25: checked against the Playwright docs (microsoft/playwright main, docs/src, commit of 2026-10-24). Confirmed: the Reporter interface (onBegin, onTestEnd, onEnd, printsToStdio), the TestCase members outcome(), titlePath(), tags, annotations and parent, TestResult duration, status and retry, the outcome values including flaky for a pass on retry, referencing a reporter file by path in the reporter option, and the printsToStdio behaviour. Removed: the claim that heavy synchronous work slows the run (not documented).

Method: documentation only; no commands were run.
