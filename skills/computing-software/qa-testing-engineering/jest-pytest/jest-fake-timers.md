---
id: computing-software.qa-testing-engineering.jest-pytest.jest-fake-timers
name: jest-fake-timers
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [fake-timers, jest-timers, usefaketimers, time-dependent-testing, jest]
level: practitioner
status: verified
description: "Control time in Jest with fake timers: useFakeTimers, advanceTimersByTime, runAllTimers, setSystemTime, async variants for promises, and pitfalls with real I/O."
sources:
  - https://jestjs.io/docs/timer-mocks
  - https://jestjs.io/docs/jest-object#fake-timers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fake timers (Jest)

## Basics
```ts
beforeEach(() => jest.useFakeTimers());
afterEach(() => jest.useRealTimers());

test('debounces search by 300 ms', () => {
  const onSearch = jest.fn();
  const search = debounce(onSearch, 300);
  search('be'); search('bea'); search('bean');
  jest.advanceTimersByTime(299);
  expect(onSearch).not.toHaveBeenCalled();
  jest.advanceTimersByTime(1);
  expect(onSearch).toHaveBeenCalledWith('bean');
});
```
Modern fake timers (the default, based on @sinonjs/fake-timers) fake `setTimeout`, `setInterval`, `setImmediate`, `Date`, `queueMicrotask`, `process.nextTick` (configurable) and `performance.now` (all ran on Jest 30: `Date.now()` and `performance.now()` advance with `advanceTimersByTime`; `runOnlyPendingTimers` also flushed the faked microtask, tick and immediate callbacks).

## API
- `jest.advanceTimersByTime(ms)`: run timers due in that window.
- `jest.runOnlyPendingTimers()`: run currently queued timers (safe with recursive timers).
- `jest.runAllTimers()`: run until no timers remain (infinite loop risk with intervals; throws after 100000 timers by default, configurable with `fakeTimers: { timerLimit }` or `jest.useFakeTimers({ timerLimit: n })`).
- `jest.advanceTimersToNextTimer()`.
- `jest.setSystemTime(new Date('2026-02-28T23:59:59Z'))`: change `Date.now()` without running timers.
- `jest.getTimerCount()`.

## With promises
```ts
await jest.advanceTimersByTimeAsync(1000);   // flushes promise callbacks between timers (Jest 29.5+; ran on Jest 30)
await jest.runAllTimersAsync();
```
Older versions: interleave `await Promise.resolve()` or use `jest.useFakeTimers({ advanceTimers: true })`.

## Config
```ts
jest.useFakeTimers({ now: new Date('2026-01-01'), doNotFake: ['nextTick', 'setImmediate'] });
// jest.config: fakeTimers: { enableGlobally: true }
```

## React Testing Library
With user-event: `userEvent.setup({ advanceTimers: jest.advanceTimersByTime })`. Wrap timer advances that trigger state updates in `act()` (RTL's async utilities handle it).

## Gotchas
- Real I/O (HTTP via a real server, database) does not advance with fake time; timeouts in libraries using real timers hang tests.
- `doNotFake: ['nextTick']` is needed by some libraries (e.g. certain DB drivers).
- Legacy timers (`legacyFakeTimers: true`) lack Date mocking (`Date.now()` did not move after `advanceTimersByTime(1000)`).

## Verify
Time-based tests run in milliseconds, timers are restored after each test, and boundary times (month end, DST) are covered with setSystemTime.
