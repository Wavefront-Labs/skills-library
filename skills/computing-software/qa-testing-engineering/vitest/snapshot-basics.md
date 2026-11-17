---
id: computing-software.qa-testing-engineering.vitest.snapshot-basics
name: snapshot-basics
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [snapshot-testing, to-match-snapshot, update-snapshots, obsolete-snapshots]
level: intro
status: docs-checked
description: "Use toMatchSnapshot in Vitest, review and commit snapshot files, update with -u or u in watch mode, and know the CI rule that mismatches fail and nothing is written."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/snapshot.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { expect, it } from 'vitest'

it('renders', () => {
  expect(toUpperCase('foobar')).toMatchSnapshot()
})
```

The first run writes a `__snapshots__/*.snap` file beside the test. Its header is `// Vitest Snapshot v1, https://vitest.dev/guide/snapshot.html`. Commit snapshot files and review them like code.

Update intentionally changed output:
- Press `u` in watch mode, or run `vitest -u` / `vitest --update`.

In CI (when `process.env.CI` is set) snapshots are not written automatically. A mismatch, a missing snapshot or an obsolete snapshot fails the run.

Use `expect` from the test context in concurrent tests so the snapshot is tied to the right test.

Differences from Jest:
- the header comment differs
- `printBasicPrototype` defaults to false (set with `snapshotFormat`)
- the hint separator in snapshot names is `>`
- the `Error` snapshot format differs

## Checked

2026-11-04. Confirmed against guide/snapshot.md and api/expect.md: `toMatchSnapshot`, the snapshot file header, committing and reviewing snapshots, `u` in watch mode, `-u` and `--update`, the CI behaviour (no writes; mismatch, missing and obsolete snapshots fail), the concurrent-test warning, and the four Jest differences. Removed: a generic rubber-stamp gotcha.

Method: documentation only; no commands were run.
