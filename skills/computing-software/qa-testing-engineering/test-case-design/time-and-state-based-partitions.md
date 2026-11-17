---
id: computing-software.qa-testing-engineering.test-case-design.time-and-state-based-partitions
name: time-and-state-based-partitions
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [time-based-partitions, equivalence-partitioning, date-time-testing, state-based-testing, clock-control]
level: practitioner
status: docs-checked
description: "Partition over time and state-dependent values: business hours, periods, expiry windows, time zones and DST, using a controllable clock in tests."
sources:
  - https://time-machine.readthedocs.io/en/latest/usage.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/Clock.html
  - https://jestjs.io/docs/jest-object
  - https://playwright.dev/docs/clock
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partitions over time and state-dependent values

**Goal:** behaviour that changes with the clock or with accumulated state gets partitioned like any input.

## Time partitions
| Rule | Partitions |
|---|---|
| Business hours 09:00-17:30 Mon-Fri | weekday in hours, weekday out of hours, weekend, public holiday |
| Token valid 15 min | fresh, about to expire, expired |
| Monthly billing | first day, mid-month, last day (28/29/30/31), leap day |
| Age from birth date | today is birthday, day before, day after |
| Time zone | user zone ahead/behind UTC, DST start (missing hour), DST end (repeated hour), date line |
| Fiscal/period close | open period, closed period |

## State-dependent partitions
The same input behaves differently by state: account active/suspended/closed, cart empty/non-empty, 3rd failed login (lock threshold), quota under/at/over. Treat the state as an extra input parameter; use state transition testing when sequences matter.

## Controlling the clock
- Inject a clock into production code. The `java.time.Clock` docs recommend passing a `Clock` into any method that needs the current instant and time zone; `Clock.fixed(instant, zone)` returns the same instant every time, which keeps tests independent of the real clock.
- Python: `time-machine` provides `time_machine.travel(destination, tick=True)` as a decorator, context manager or via `start()` and `stop()`. With the default `tick=True` time keeps moving after the jump; pass `tick=False` to freeze it. A destination with a `zoneinfo.ZoneInfo` tzinfo also mocks the current time zone (Unix only). Example: `@time_machine.travel("2024-03-31 01:59:00+00:00")`.
- Jest: `jest.useFakeTimers()` then `jest.setSystemTime(...)`.
- Playwright: `page.clock.setFixedTime(...)` is the recommended way to set a specific time; `page.clock.install()` lets you pause, fast forward and tick, and must come before other clock calls.
- Databases: avoid `NOW()` in queries under test, or control it through session time zone and fixed data.

## Gotchas
- Tests that pass except at midnight or month end are time-partition bugs; run the suite with a randomised fixed clock.
- Store UTC, convert at the edges; test display in at least one non-UTC zone.
- "Expires in 30 days" vs "1 month" are different partitions on 31-day months.

## Verify
Each time rule lists its partitions, and tests pin the clock explicitly instead of depending on the run date.

## Checked
2026-11-08. Checked against the time-machine usage page (`travel`, `tick`, `start`/`stop`, ZoneInfo handling), the Java 21 `java.time.Clock` page (inject a Clock, `Clock.fixed`), the Jest object page (`jest.useFakeTimers`, `jest.setSystemTime`) and the Playwright Clock page (`setFixedTime`, `install`, ordering note). Removed: `freezegun` (its docs page returned 404) and the combined `useFakeTimers().setSystemTime` chain. The partition tables, state examples and gotchas are test-design guidance, not factual claims. Replaced the ISTQB, IANA and PyPI sources.

Method: documentation only; no commands were run.
