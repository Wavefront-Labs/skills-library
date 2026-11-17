---
id: computing-software.software-engineering.typescript.node-built-in-test-runner
name: node-built-in-test-runner
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, nodejs, node-runtime, node-test-runner, node-test, mocking, coverage, typescript-testing]
level: practitioner
status: verified
description: "Test with node --test and node:test: describe/it, built-in mocking and fake timers, snapshots, coverage, watch mode and running TypeScript without a framework."
sources:
  - https://nodejs.org/api/test.html
  - https://nodejs.org/api/cli.html#--test
  - https://nodejs.org/api/typescript.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# node --test: the built-in test runner

**Goal:** zero-dependency tests for Node libraries and services, using only the runtime.

## 1. Writing tests
```ts
// src/price.test.ts
import { describe, it, before, mock } from "node:test";
import assert from "node:assert/strict";
import { applyDiscount } from "./price.ts";

describe("applyDiscount", () => {
  it("applies percentage discounts", () => {
    assert.equal(applyDiscount(100, { pct: 10 }), 90);
  });
  it("rejects negative totals", () => {
    assert.throws(() => applyDiscount(-1, { pct: 5 }), { name: "RangeError" });
  });
  it("awaits async code", async () => {
    await assert.rejects(fetchPrice("missing"), /not found/);
  });
});
```
Use `node:assert/strict` (deep strict equality by default).

## 2. Running
```bash
node --test                                  # finds **/*.test.{js,mjs,cjs,ts,...} and test/ dirs
node --test --watch
node --test --test-name-pattern="discount"
node --test --test-concurrency=4 --test-reporter=spec --test-reporter=junit --test-reporter-destination=stdout --test-reporter-destination=junit.xml
node --test --experimental-test-coverage --test-coverage-lines=80
```
TypeScript: Node 22.18+/23.6+ strips types by default (erasable syntax only: no enums/namespaces/parameter properties; it is stable from 24.12/25.2), so `node --test` runs `.ts` files directly. Checked: on 22.17.1 plain `node --test` found 0 `.ts` tests and needed `--experimental-strip-types`; on 24.22.0 it ran them. Older versions: `node --import tsx --test`.

## 3. Mocking
```ts
it("retries", async (t) => {
  const fetchMock = t.mock.method(globalThis, "fetch", async () => new Response("ok"));
  await client.get("/x");
  assert.equal(fetchMock.mock.callCount(), 1);
  assert.deepEqual(fetchMock.mock.calls[0].arguments[0], "https://api/x");
});                                           // t.mock restores automatically after the test

it("expires tokens", (t) => {
  t.mock.timers.enable({ apis: ["setTimeout", "Date"] });
  const token = issue();
  t.mock.timers.tick(61_000);
  assert.equal(token.isExpired(), true);
});
```
Module mocking: `t.mock.module("./db.ts", { namedExports: { query: async () => [] } })` (needs `--experimental-test-module-mocks`).

## 4. Other features
- `it.skip`, `it.todo`, `it.only` (with `--test-only`), `{ timeout: 5000 }`, `before/after/beforeEach/afterEach`.
- Snapshots: `t.assert.snapshot(value)` and `--test-update-snapshots` (stable in Node 23.4+).
- Subtests via `t.test()` must be awaited.

## When to choose Vitest/Jest instead
Front-end code needing a DOM environment, rich watch UI, extensive module mocking, or a team already invested in Jest APIs.

## Gotchas
- Each test file runs in its own subprocess by default (`--test-isolation=process`); module state is not shared across files.
- Forgotten `await` on subtests or async assertions lets the test finish before the assertion runs, so failures surface late or are lost.
- Coverage is marked experimental in the Node docs (`--experimental-test-coverage`); the minimum-percentage options (`--test-coverage-lines` etc.) are documented as added in v22.10.0 and v23.0.0 (via the `run()` options). Snapshots: `t.assert.snapshot` needs a first `--test-update-snapshots` run to create `<file>.snapshot` (checked: ENOENT without it).

## Verify
- `node --test` exits non-zero on a failing assertion in CI, and the JUnit reporter output is picked up by the CI test summary.
