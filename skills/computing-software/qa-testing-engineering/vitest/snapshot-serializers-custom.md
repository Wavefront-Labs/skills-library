---
id: computing-software.qa-testing-engineering.vitest.snapshot-serializers-custom
name: snapshot-serializers-custom
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [snapshot-serializer, custom-snapshot-matcher, snapshot-format, domain-snapshot]
level: advanced
status: docs-checked
description: "Customise Vitest snapshots with serializers, snapshotFormat, custom snapshot matchers built on the Snapshots export (4.1.3), and domain snapshot adapters (4.1.4)."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/snapshot.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/migration/jest.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Serializers change how a value is printed in a snapshot:
- `expect.addSnapshotSerializer(serializer)` in a test or setup file
- `snapshotSerializers: ['pkg-or-path']` in config (for example `jest-serializer-vue` for Vue snapshots that would otherwise be wrapped in a string with escaped quotes)

Formatting: the `snapshotFormat` option configures general snapshot formatting, for example `printBasicPrototype`.

Custom snapshot matchers (experimental, 4.1.3) build on the `Snapshots` export from `vitest`:

```ts
import { Snapshots } from 'vitest'
const { toMatchSnapshot } = Snapshots

expect.extend({
  toMatchTrimmedSnapshot(received: string, length: number) {
    return toMatchSnapshot.call(this, received.slice(0, length))
  },
})
```

For inline snapshots, use `Snapshots.toMatchInlineSnapshot` and pass the inline snapshot argument last.

Domain snapshot adapters (4.1.4): implement `DomainSnapshotAdapter` with `capture`, `render`, `parseExpected` and `match`, and call `Snapshots.toMatchDomainSnapshot`.

The documented examples call the Snapshots functions with `.call(this, ...)`.

## Checked

2026-11-04. Confirmed against guide/snapshot.md, guide/migration/jest.md and api/expect.md: `expect.addSnapshotSerializer`, `snapshotSerializers`, `snapshotFormat` and `printBasicPrototype`, the experimental 4.1.3 and 4.1.4 version tags, the Snapshots composables, the last-argument rule for inline matchers, and the four adapter methods. Removed: an unstated reason attached to the `.call(this, ...)` gotcha.

Method: documentation only; no commands were run.
