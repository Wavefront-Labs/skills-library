---
id: computing-software.qa-testing-engineering.vitest.snapshot-inline-and-file
name: snapshot-inline-and-file
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [inline-snapshot, file-snapshot, to-match-file-snapshot, error-snapshot]
level: practitioner
status: docs-checked
description: "Store Vitest snapshots inline with toMatchInlineSnapshot, in a chosen file with toMatchFileSnapshot, and for errors with toThrowErrorMatchingSnapshot variants."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/snapshot.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inline: Vitest adds and updates the snapshot string argument in the test file instead of an external `.snap` file.

```ts
it('formats', () => {
  expect(format({ a: 1 })).toMatchInlineSnapshot()
})
```

File snapshot: compare against a file you control, which keeps syntax highlighting and lets the file be a real artifact (HTML, SQL, and so on). The call returns a promise, so await it.

```ts
await expect(render()).toMatchFileSnapshot('./expected/output.html')
```

Do not point it at a Vitest-managed `__snapshots__` path.

Error snapshots:
- `toThrowErrorMatchingSnapshot()`
- `toThrowErrorMatchingInlineSnapshot()`

For a custom inline snapshot matcher, the snapshot argument must be the last parameter (or second-to-last with property matchers), because Vitest rewrites the last string argument.

Without `await`, `toMatchFileSnapshot` is treated like `expect.soft`: code after it keeps running, and the test fails after it finishes if the snapshot mismatches.

## Checked

2026-11-04. Confirmed against guide/snapshot.md and api/expect.md: inline snapshot rewriting, `toMatchFileSnapshot` returning a promise and its await behaviour, the warning about Vitest-managed snapshot paths, the two error snapshot matchers, and the last-parameter rule. Removed: an opaque-wrapper sentence the pages do not state, and a false-pass claim that contradicted the expect.soft behaviour on the page.

Method: documentation only; no commands were run.
