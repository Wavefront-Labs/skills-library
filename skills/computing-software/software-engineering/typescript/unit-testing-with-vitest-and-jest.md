---
id: computing-software.software-engineering.typescript.unit-testing-with-vitest-and-jest
name: unit-testing-with-vitest-and-jest
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, typescript-testing, vitest, jest, module-mocking, fake-timers, test-doubles, coverage]
level: practitioner
status: verified
description: "Unit test TypeScript with Vitest or Jest: config, ESM/TS transforms, mocking modules and timers, spying, snapshot discipline, coverage and test isolation."
sources:
  - https://vitest.dev/guide/
  - https://vitest.dev/guide/mocking.html
  - https://jestjs.io/docs/getting-started
  - https://jestjs.io/docs/ecmascript-modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit testing TypeScript with Vitest or Jest

**Goal:** fast, isolated unit tests with module mocking that works under ESM and TypeScript.

## 1. Choosing
- **Vitest**: native ESM and TS via Vite/esbuild, Jest-compatible API (`describe/it/expect/vi`), fast watch. Default for new projects and Vite apps.
- **Jest**: huge ecosystem; ESM support still experimental (`--experimental-vm-modules`, per the Jest ESM docs); TS via `ts-jest` or `@swc/jest`/babel.

## 2. Vitest setup
```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";
export default defineConfig({
  test: {
    environment: "node",           // "jsdom"/"happy-dom" for DOM code
    restoreMocks: true,            // restore spies after each test
    coverage: { provider: "v8", reporter: ["text", "lcov"], thresholds: { lines: 80, branches: 75 } },
  },
});
```
`vitest` (watch), `vitest run` (CI), `vitest run --coverage`. (This config, the mocks and fake timers below ran on Vitest 5.0.5 with Node 24.)

## 3. Mocking modules
```ts
import { vi, it, expect, beforeEach } from "vitest";
import { sendWelcome } from "./signup";
import * as mailer from "./mailer";

vi.mock("./mailer", () => ({ send: vi.fn().mockResolvedValue({ id: "m1" }) }));   // hoisted above imports

it("sends a welcome mail", async () => {
  await sendWelcome("a@x.co");
  expect(mailer.send).toHaveBeenCalledWith(expect.objectContaining({ to: "a@x.co" }));
});
```
Partial mock: `vi.mock("./cfg", async (orig) => ({ ...(await orig()), flag: true }))`. Variables used inside the factory must be created with `vi.hoisted` (tested: a top-level `const mockSend = vi.fn()` fails with "Cannot access 'mockSend' before initialization"; `vi.hoisted(() => vi.fn())` passes). Jest equivalents: `jest.mock`, `jest.fn`, `jest.requireActual`.

## 4. Spies and timers
```ts
const spy = vi.spyOn(Date, "now").mockReturnValue(1_700_000_000_000);
vi.useFakeTimers();
const p = retryWithBackoff(op);
await vi.advanceTimersByTimeAsync(5_000);     // async variant flushes promises between timers
await expect(p).resolves.toBe("ok");
vi.useRealTimers();
```

## 5. Design for testability
Prefer dependency injection (pass the mailer/clock in) over module mocking; it survives refactors and works in every runner. Reserve `vi.mock` for third-party modules at boundaries. For HTTP, MSW (Mock Service Worker) intercepts `fetch` at the network layer.

## Gotchas
- Mocks leak between tests without `restoreMocks`/`clearMocks` or `afterEach(vi.restoreAllMocks)`.
- Mocking the module under test's own internal functions does not work if they are called directly within that module (bindings are local); split modules or inject.
- Snapshot tests of large objects get rubber-stamped with `-u`; keep snapshots small and inline (`toMatchInlineSnapshot`).
- `toBe` vs `toEqual` vs `toStrictEqual`: identity, deep equality, deep equality including undefined properties and class types.
- Jest + ESM-only dependencies: "SyntaxError: Cannot use import statement outside a module"; transformIgnorePatterns or move to Vitest.

## Verify
- `vitest run --coverage` passes thresholds in CI, and running tests in random order (`--sequence.shuffle`) stays green.
