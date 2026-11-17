---
id: computing-software.software-engineering.debugging.time-zone-and-locale-bugs
name: time-zone-and-locale-bugs
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, production-debugging, timezone-bugs, locale-bugs, dst, clock-skew, unicode]
level: practitioner
status: gated
description: "Find and fix time and locale bugs: UTC storage, DST gaps and overlaps, naive vs aware datetimes, clock skew, leap days, locale-dependent parsing, casing and collation."
sources:
  - https://www.iana.org/time-zones
  - https://docs.python.org/3/library/zoneinfo.html
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html
  - https://unicode-org.github.io/icu/userguide/locale/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zone and locale bugs

## Symptoms that point here
Fails only around midnight, month end, DST changes, New Year, Feb 29; fails for users in one country; passes locally, fails in CI (CI runs in UTC); off-by-one-hour or off-by-one-day values; sorting or uppercase wrong for some users.

## Time rules
- **Store instants in UTC** (`timestamptz` in Postgres stores UTC; MySQL `DATETIME` stores no zone - convert explicitly). Convert to local time only at the edges (display, user input).
- **Store the IANA zone id** (`Europe/London`), never a fixed offset, for future local events (meetings, schedules) - offsets change with DST and politics. For a future local event store local date-time + zone and compute the instant late.
- **Never use naive datetimes** for instants: Python `datetime.now(timezone.utc)` not `datetime.utcnow()` (deprecated since 3.12, naive; run on 3.14: emits `DeprecationWarning`); Java `Instant`/`ZonedDateTime`, not `java.util.Date`/`LocalDateTime` for instants (gated: unconfirmed, source is paywalled or blocked); JS `Date` is always UTC internally but formats in local time - use `Intl.DateTimeFormat` with `timeZone` or Temporal.
- **DST gaps and overlaps:** 02:30 does not exist on spring-forward day; 01:30 happens twice in autumn. Python `fold` (run with `America/New_York`: 2026-03-08 02:30 does not exist and converts through the pre-gap offset to 07:30 UTC, which reads back as 03:30 EDT; 2026-11-01 01:30 gives 05:30 UTC with `fold=0` and 06:30 UTC with `fold=1`), Java `ZonedDateTime.ofLocal` with `withEarlierOffsetAtOverlap()` (gated: unconfirmed, source is paywalled or blocked). Daily jobs scheduled at 02:30 local skip or run twice - schedule in UTC or pick a safe time.
- **Durations vs calendar periods:** "one day later" is 23 or 25 hours across DST (run with zoneinfo: noon 7 Mar 2026 plus `timedelta(days=1)` in New York is noon on 8 Mar, 23 hours later; 1 Nov 2026 is a 25-hour day). Use calendar arithmetic (`plusDays`, `relativedelta`) for dates, durations for elapsed time.
- **Elapsed time uses a monotonic clock:** `time.monotonic()`, `System.nanoTime()`, `performance.now()`, `Stopwatch` - wall clocks jump (NTP, manual changes).
- **Clock skew between machines:** do not compare timestamps from different hosts for ordering; allow leeway in JWT `exp/nbf` validation (30-60 s); use logical clocks/sequence numbers for ordering.
- Leap years and month lengths: Feb 29 plus one year, "same day next month" on Jan 31. Test them (run with `relativedelta`: 2024-02-29 plus one year is 2025-02-28, 2026-01-31 plus one month is 2026-02-28; other libraries may clamp differently).
- Keep tzdata updated (OS package, `tzdata` PyPI package on Windows, JDK `tzupdater`, `moment-timezone` data).

## Locale rules
- Parse and format machine data with an invariant locale: Java `Locale.ROOT`, .NET `CultureInfo.InvariantCulture` (gated: unconfirmed, source is paywalled or blocked), Python avoid `locale.atof` for data; JSON/CSV numbers always `.` decimal.
- **Turkish-i problem:** `"TITLE".toLowerCase()` in `tr-TR` gives dotless-i (run in Node: `'TITLE'.toLocaleLowerCase('tr-TR')` is `tıtle`, `toLowerCase()` is `title`), breaking comparisons. Use `toLowerCase(Locale.ROOT)` / `ToLowerInvariant()` for identifiers; case-insensitive comparison via `equalsIgnoreCase`/`StringComparison.OrdinalIgnoreCase`.
- Sorting user-visible text: locale-aware collation (ICU, `Intl.Collator`, DB collation); for keys/ids use ordinal comparison.
- Default encodings: set UTF-8 explicitly (Java 18+ defaults to UTF-8; older uses platform charset; Windows console code pages).
- Unicode normalisation (NFC vs NFD) makes visually equal strings unequal (run in Node: `'é' === 'é'` is false, equal after `normalize('NFC')`; macOS file names are NFD).

## Testing
- Run the suite with different TZ and locale: `TZ=Pacific/Chatham pytest` (works for the C library on Linux and macOS; Python on Windows has no `time.tzset`, so set the zone in the test instead), `TZ=America/Sao_Paulo`, `LANG=tr_TR.UTF-8`, JVM `-Duser.timezone=Asia/Kolkata -Duser.language=tr`.
- Freeze time at the nasty instants (freezegun, time-machine, sinon fake timers; Java `Clock.fixed` and .NET `FakeTimeProvider` (gated: unconfirmed, source is paywalled or blocked)): DST transition, 23:59:59.999, Dec 31, Feb 29.

## Verify
- [ ] A regression test pins the failing instant/zone/locale.
- [ ] CI matrix includes a non-UTC timezone and a non-English locale job.
