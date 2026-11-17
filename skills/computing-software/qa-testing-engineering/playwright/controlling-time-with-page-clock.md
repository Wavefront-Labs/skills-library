---
id: computing-software.qa-testing-engineering.playwright.controlling-time-with-page-clock
name: controlling-time-with-page-clock
category: computing-software
field: qa-testing-engineering
product: playwright
tags: [page-clock, fake-timers-browser, playwright-clock, time-dependent-testing, install-clock]
level: practitioner
status: verified
description: "Control browser time in Playwright with page.clock: install, setFixedTime, fastForward, runFor and pauseAt to test timers, expiry, countdowns and inactivity logouts."
sources:
  - https://playwright.dev/docs/clock
  - https://playwright.dev/docs/api/class-clock
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controlling time with page.clock (Playwright)

**Goal:** test time-dependent UI (session timeout, countdown, "posted 5 minutes ago", date boundaries) without waiting. Available from Playwright 1.45.

## Fixed time (Date only, timers run normally; run here: a 200 ms `setTimeout` fired while `Date.now()` stayed frozen)
```ts
await page.clock.setFixedTime(new Date('2026-12-31T23:59:50Z'));
await page.goto('/sale');
await expect(page.getByText('Sale ends today')).toBeVisible();
```

## Full control of timers
```ts
await page.clock.install({ time: new Date('2026-03-29T00:59:00Z') }); // before goto: fakes Date, setTimeout, setInterval, rAF, performance
await page.goto('/session');
await page.clock.fastForward('29:00');          // jump 29 minutes, fires due timers once
await expect(page.getByRole('dialog', { name: 'Still there?' })).toBeVisible();
await page.clock.runFor(60_000);                 // advance 1 min ticking through every timer
await expect(page).toHaveURL(/login/);
```
- `pauseAt(date)`: jump to a time and pause; then `runFor` step by step (run here: after `pauseAt` the page date stayed put for 300 ms of real time, `runFor(1000)` moved it by exactly 1 s, and `resume()` let it run again).
- `resume()`: continue in real time from the fake time.
- `setSystemTime(date)`: change the clock without firing timers (simulate the user changing system time; run here: a 1 s timeout stayed unfired after jumping a year ahead).

Time strings: `'01:00'` (1 min), `'02:34:10'`, or milliseconds (run here: `fastForward('01:00')` moved the page date by 1 min, `'02:34:10'` by 2 h 34 min 10 s). `fastForward` fires each due timer at most once: a 1 s `setInterval` ticked once for a 1-minute jump.

## Typical cases
- Inactivity logout and token refresh.
- Countdowns and polling intervals.
- Month end, leap day, DST transitions (pair with `timezoneId` in context options).
- Animations driven by timers.

## Gotchas
- Call `install` before the page loads scripts, or existing timers keep real time (run here: a timer set before `install` did not fire after `fastForward(200000)`).
- Server time is not faked; server-side expiry still needs backend test hooks or API state.
- Third-party scripts relying on timers also change behaviour.

## Verify
A 30-minute timeout test runs in seconds, and changing the threshold in the app fails the test.
