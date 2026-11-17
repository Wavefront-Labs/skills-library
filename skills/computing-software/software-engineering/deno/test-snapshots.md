---
id: computing-software.software-engineering.deno.test-snapshots
name: test-snapshots
category: computing-software
field: software-engineering
product: deno
tags: [test, snapshot, assert-snapshot, update-snapshots, serializer, node-test-snapshot]
level: practitioner
status: docs-checked
description: "Snapshot testing with t.assertSnapshot: creating and updating .snap files, reviewing diffs, CI verification, custom serializers and when not to snapshot."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/snapshots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts title="example_test.ts"
Deno.test("isSnapshotMatch", async (t) => {
  const a = { hello: "world!", example: 123 };
  await t.assertSnapshot(a);
});
```

Create or update snapshots with `deno test --update-snapshots` (`-u`). Normal `deno test` compares, failing with an `AssertionError` diff. No read/write permission is needed in the default location.

Snapshots live in `__snapshots__/example_test.ts.snap`, keyed by test name plus a counter (`isSnapshotMatch 1`), serialized with `Deno.inspect` with sorted keys. Commit them and review `git diff` after updating, since updating records bugs as expected output.

In CI, run `deno test` without `--update-snapshots`.

Options (second argument): `serializer` (deterministic; strip ANSI, replace timestamps/UUIDs, redact secrets), `name`, `dir`/`path` (custom location needs read and write permission), `msg`.

```ts
await t.assertSnapshot(output, {
  serializer: (actual) => stripAnsiCode(actual),
});
```

Classes can implement `Symbol.for("Deno.customInspect")`. With `node:test`, use `t.assert.fileSnapshot(value, "./__snapshots__/user.json")`.

Avoid snapshots when a precise assertion is easy, output is non-deterministic, output is huge, or you should verify behaviour rather than representation.

## Checked

2026-11-04. Confirmed against docs runtime/test/snapshots.md: t.assertSnapshot, --update-snapshots and -u, __snapshots__ .snap location and keys, Deno.inspect serialization, options, node:test fileSnapshot.

Method: documentation only; no commands were run.
