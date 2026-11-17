---
id: computing-software.qa-testing-engineering.vitest.fake-timers-basics
name: fake-timers-basics
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [fake-timers, use-fake-timers, advance-timers-by-time, run-all-timers]
level: intro
status: docs-checked
description: "Speed up time-based tests with vi.useFakeTimers, advanceTimersByTime, runAllTimers, runOnlyPendingTimers and useRealTimers, with the loop limit and setup pattern."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/timers.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/api/vi.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
beforeEach(() => { vi.useFakeTimers() })
afterEach(() => { vi.useRealTimers() })

it('runs after two hours', () => {
  executeAfterTwoHours(fn)
  vi.advanceTimersByTime(2 * 60 * 60 * 1000)
  expect(fn).toHaveBeenCalledTimes(1)
})
```

Controls:
- `vi.advanceTimersByTime(ms)`, `advanceTimersToNextTimer()`, `advanceTimersToNextFrame()`
- `vi.runAllTimers()`, `vi.runOnlyPendingTimers()`, `vi.runAllTicks()`
- `Async` versions of the timer-running methods flush promise work between timers
- `vi.getTimerCount()`, `vi.clearAllTimers()`, `vi.isFakeTimers()`
- `vi.useFakeTimers({ toFake: [...], toNotFake: [...], now })` picks which APIs are faked; `toFake` and `toNotFake` cannot be used together

Defaults to know:
- `runAllTimers` stops at a loop limit of 10000 timers (`fakeTimers.loopLimit`), which protects against endless `setInterval`.
- `nextTick` and `queueMicrotask` are not faked by default.
- Mocking `nextTick` is unsupported with the forks pool.

Timers stay faked until `vi.useRealTimers()` is called, so restore them in `afterEach`.

## Checked

2026-11-04. Confirmed against api/vi.md (each timer method, `loopLimit` and the 10 000 tries limit, `toFake` and `toNotFake`, nextTick and queueMicrotask not faked by default, nextTick unsupported with `--pool=forks`) and guide/mocking/timers.md (example). Reworded a closing line that claimed frozen time and that `vi.clearAllMocks()` cannot undo it; the page only says timers are wrapped until `vi.useRealTimers()`.

Method: documentation only; no commands were run.
