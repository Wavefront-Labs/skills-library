---
id: computing-software.qa-testing-engineering.vitest.test-annotations
name: test-annotations
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-annotations, annotate-api, annotation-attachments, on-test-annotate]
level: practitioner
status: docs-checked
description: "Attach messages, types and files to a Vitest test with context.annotate and see how the default, verbose, junit, github-actions and tap reporters show them."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-annotations.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/test-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
test('hello world', async ({ annotate }) => {
  await annotate('this is my test')
  await annotate('this should have errored', 'error')
  await annotate('creates a file', { body: createTestSpecificFile() })
  await annotate('creates a file with text', {
    contentType: 'text/markdown',
    body: 'Hello **markdown**',
    bodyEncoding: 'utf-8',
  })
})
```

`annotate(message, type?)` or `annotate(message, { body, contentType, bodyEncoding })`. It returns a Promise; Vitest also awaits any un-awaited annotation before the test ends. Annotations reach reporters through the `onTestAnnotate` hook.

How reporters show them:
- `default`: only when the test failed.
- `verbose`: always (the only terminal reporter that shows annotations on passing tests).
- `html`: in the UI at the line that called it, only for calls made in the test file.
- `junit`: in the testcase `properties` tag; attachments are ignored.
- `github-actions`: a notice by default; the type can be `notice`, `warning` or `error`.
- `tap` and `tap-flat`: diagnostic lines starting with `#`; attachments ignored.

`annotate` was added in 3.2.0.

## Checked

2026-11-04. Confirmed against guide/test-annotations.md and guide/test-context.md: the code sample, the Promise and auto-await warning, the `onTestAnnotate` hook, per-reporter behaviour (default, verbose, html, junit, github-actions, tap and tap-flat), and the 3.2.0 version tag.

Method: documentation only; no commands were run.
