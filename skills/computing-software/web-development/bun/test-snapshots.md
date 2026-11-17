---
id: computing-software.web-development.bun.test-snapshots
name: test-snapshots
category: computing-software
field: web-development
product: bun
tags: [snapshot-testing, inline-snapshot, update-snapshots, property-matchers]
level: practitioner
status: docs-checked
description: "Use snapshot tests in bun test: file and inline snapshots, updating with --update-snapshots, property matchers for volatile values, and cross-runner format caveats."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/snapshots.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
APIs: `.toMatchSnapshot()` (writes `__snapshots__/<file>.snap` on first run), `.toMatchInlineSnapshot()`, `.toThrowErrorMatchingSnapshot()`, `.toMatchFileSnapshot("./path")` (path relative to the test file), `expect.addSnapshotSerializer()`.

Inline: call `.toMatchInlineSnapshot()` with no argument, run once, and Bun inserts the snapshot into the file.

```ts
expect({ id: Math.random(), createdAt: new Date().toISOString() }).toMatchSnapshot({
  id: expect.any(Number),
  createdAt: expect.any(String),
});
```
Property matchers are stored as `Any<Number>` rather than actual values.

```bash
bun test --update-snapshots    # after intentional output changes
```

Gotchas:
- In CI Bun does not write new snapshots unless you pass the update flag.
- Timestamps and random IDs fail unless you use property matchers or normalize them.
- A serializer added in a test file lasts until that file ends; one in a preload or imported module applies to later files.
- Bun, Jest and Vitest print functions, classes, mocks, regexes and symbol keys differently, so the format depends on the runner that wrote the file.
- With `--update-snapshots`, Jest/Vitest-format files lose unused entries; Bun-format files keep only entries for tests that ran.
- Normalize Windows versus Unix path separators before snapshotting.

## Checked

2026-11-04. Confirmed against the Bun docs page test/snapshots: the snapshot APIs, __snapshots__ location, CI behaviour, inline snapshot insertion, toMatchFileSnapshot relative path, Any<Number> storage, serializer lifetime, runner format differences and --update-snapshots pruning. Replaced the property-matcher example with the page's own (ISO string timestamp matched with expect.any(String)).
Method: documentation only; no commands were run.
