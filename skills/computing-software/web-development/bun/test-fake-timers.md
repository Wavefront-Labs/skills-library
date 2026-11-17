---
id: computing-software.web-development.bun.test-fake-timers
name: test-fake-timers
category: computing-software
field: web-development
product: bun
tags: [fake-timers, set-system-time, test-timezone, advance-timers]
level: practitioner
status: docs-checked
description: "Control time in bun test: jest.useFakeTimers, setSystemTime, advancing timers (including async variants), TZ handling, and what stays real."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/test/dates-times.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import { jest, expect, test } from "bun:test";

test("fires after full delay", () => {
  jest.useFakeTimers();
  const cb = jest.fn();
  setTimeout(cb, 1000);
  jest.advanceTimersByTime(999);
  expect(cb).not.toHaveBeenCalled();
  jest.advanceTimersByTime(1);
  expect(cb).toHaveBeenCalledTimes(1);
  jest.useRealTimers();
});

jest.setSystemTime(new Date("2020-01-01T00:00:00.000Z")); // same as vi.setSystemTime
```
`setSystemTime()` with no argument resets to real time.

Fake timers replace `setTimeout`, `setInterval`, `clearTimeout`, `clearInterval`; `Date`, `performance.now()` and `process.hrtime()` read the same fake clock. Helpers: `advanceTimersByTime`, `advanceTimersToNextTimer`, `runOnlyPendingTimers`, `runAllTimers`, `getTimerCount`, `clearAllTimers`. Options: `toFake`, `doNotFake`, `shouldAdvanceTime`.

Time zone: `bun test` defaults to UTC. Use `TZ=America/Los_Angeles bun test`, or assign `process.env.TZ`; `delete process.env.TZ` resets to UTC.

Gotchas:
- Callbacks that schedule timers after an `await` need `advanceTimersByTimeAsync` / `runAllTimersAsync`.
- `setImmediate` stays real unless listed in `toFake`; timer functions saved before `useFakeTimers()` and `node:timers` exports stay real.
- `runAllTimers()` throws after too many timers, so endless intervals cannot hang.
- Without isolation, fake timers set at the top level of a preload carry over between files.

## Checked

2026-11-04. Confirmed against the Bun docs page test/dates-times: useFakeTimers example, setSystemTime and reset, the faked APIs, advance helper names, toFake/doNotFake/shouldAdvanceTime, async variants, setImmediate and saved-timer behaviour, runAllTimers limit, preload carry-over, UTC default TZ and delete process.env.TZ. Nothing removed.
Method: documentation only; no commands were run.
