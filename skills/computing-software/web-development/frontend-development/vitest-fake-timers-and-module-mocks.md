---
id: computing-software.web-development.frontend-development.vitest-fake-timers-and-module-mocks
name: vitest-fake-timers-and-module-mocks
category: computing-software
field: web-development
product: frontend-development
tags: [fake-timers, vi-mock, vitest, vi-spyon, setsystemtime, frontend-testing]
level: practitioner
status: verified
description: "Controlling time and dependencies in Vitest: fake timers with async advancing and setSystemTime, user-event integration, vi.mock hoisting, partial mocks and cleanup."
sources:
  - https://vitest.dev/guide/mocking
  - https://vitest.dev/api/vi.html#vi-usefaketimers
  - https://testing-library.com/docs/user-event/options#advancetimers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vitest fake timers and module mocks

## 1. Fake timers
```ts
beforeEach(() => { vi.useFakeTimers(); vi.setSystemTime(new Date("2026-10-18T09:00:00Z")); });
afterEach(() => { vi.useRealTimers(); });

test("debounced save fires once", async () => {
  const save = vi.fn();
  const d = debounce(save, 500);
  d(1); d(2); d(3);
  await vi.advanceTimersByTimeAsync(499); expect(save).not.toHaveBeenCalled();
  await vi.advanceTimersByTimeAsync(1);   expect(save).toHaveBeenCalledExactlyOnceWith(3);
});
```
- Use the `...Async` variants (`advanceTimersByTimeAsync`, `runAllTimersAsync`) when callbacks await promises; the sync versions do not flush microtasks between timers.
- `vi.runOnlyPendingTimers()` for recursive intervals: `runAllTimers` on a `setInterval` throws "Aborting after running 10000 timers, assuming an infinite loop" (`fakeTimers.loopLimit`, default 10 000).
- `setSystemTime` fakes `Date`. In Vitest 5.0.5 `performance.now` advanced with `advanceTimersByTime(1000)` (delta 1000): `fakeTimers.toFake` defaults to everything available except `nextTick` and `queueMicrotask`; narrow `toFake` (or use `toNotFake`, not both) to leave `performance` real.

## 2. With Testing Library user-event
```ts
const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
await user.type(input, "hello");
```
Without `advanceTimers`, `user.type` timed out (2 s test timeout) under fake timers; with it the test passed (jsdom, user-event 14.6). `findBy*` queries poll with timers too; they work because Testing Library detects Vitest fake timers, but advancing explicitly is more predictable.

## 3. Module mocks
```ts
import { getUser } from "./api";
vi.mock("./api", () => ({ getUser: vi.fn() }));          // hoisted above imports
vi.mocked(getUser).mockResolvedValue({ id: 1, name: "Ada" });

// partial mock: keep the real module, override one export
vi.mock("./date-utils", async (importOriginal) => ({ ...(await importOriginal()), now: vi.fn(() => 0) }));

// variables used inside a factory must be hoisted too
const { mockTrack } = vi.hoisted(() => ({ mockTrack: vi.fn() }));
vi.mock("./analytics", () => ({ track: mockTrack }));
```
- `vi.spyOn(obj, "method")` for objects you own; for other modules' exports prefer `vi.mock` (in a test `vi.spyOn` on an ESM namespace did not throw, but whether importers see the spy depends on the module graph).
- Globals: `vi.stubGlobal("fetch", vi.fn())`, env: `vi.stubEnv("VITE_API", "http://x")`; undo with `vi.unstubAllGlobals()` / `unstubAllEnvs`.
- Network-level mocking (MSW) is usually better than mocking your API module for integration tests.

## 4. Cleanup
Set `restoreMocks: true` (and `unstubGlobals`, `unstubEnvs`) in config so state does not leak between tests.

## Verify
- [ ] Tests pass with `--sequence.shuffle` (no order dependence from leaked mocks or timers).
