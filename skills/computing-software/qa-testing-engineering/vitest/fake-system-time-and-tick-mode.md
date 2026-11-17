---
id: computing-software.qa-testing-engineering.vitest.fake-system-time-and-tick-mode
name: fake-system-time-and-tick-mode
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [set-system-time, timer-tick-mode, fake-date, auto-advance-timers]
level: advanced
status: docs-checked
description: "Control Date with vi.setSystemTime, and let fake timers advance themselves with vi.setTimerTickMode (manual, nextTimerAsync, interval) and in waitFor and poll."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/timers.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/dates.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/expect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Date handling:

```ts
vi.useFakeTimers()
vi.setSystemTime(new Date(2020, 0, 1))
expect(new Date().getFullYear()).toBe(2020)
vi.getMockedSystemTime() // the faked date, or null if the date is not mocked
vi.getRealSystemTime()   // the real clock
```

Tick modes (4.1.0), set with `vi.setTimerTickMode(mode, ms?)`:
- `'manual'` (default): time moves only when you advance it.
- `'interval'`: advances fake time by a fixed step on a real-time interval; suits state that only lasts for a limited time.
- `'nextTimerAsync'`: runs the next pending timer after each macrotask, so chained timers fire almost back to back; state that only lasts for a limited time can vanish before an assertion sees it.

Automatic advancing: while fake timers are on, `vi.waitFor` and `vi.waitUntil` advance timers by `interval` before every check, and `expect.poll` advances them after every failed attempt.

`vi.setSystemTime` also works without fake timers, in which case it mocks only `Date.*` and `Temporal.Now.*`; with fake timers it does not fire any timers.

An async function that rejects during `vi.advanceTimersByTimeAsync` triggers an unhandled rejection even if you assert `.rejects.toThrow()` afterwards. The docs prefer `vi.setTimerTickMode('nextTimerAsync')`, or creating the `rejects` assertion before advancing the timers and awaiting it afterwards.

## Checked

2026-11-04. Confirmed against api/vi.md (`setSystemTime`, `getMockedSystemTime`, `getRealSystemTime`, `setTimerTickMode` and its modes, 4.1.0), guide/mocking/timers.md (automatic advancing, tick mode descriptions), guide/mocking/dates.md and api/expect.md (unhandled rejection warning and the two remedies).

Method: documentation only; no commands were run.
