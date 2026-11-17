---
id: computing-software.software-engineering.haskell.time-library-usage
name: time-library-usage
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, time, utctime, getcurrenttime, diffutctime, formattime, parsetimem, nominaldifftime, calendardays, timezone, time-library-usage, haskell-datetime]
level: practitioner
status: docs-checked
description: "Work with dates and times using the time package: UTCTime, Day, NominalDiffTime, formatTime/parseTimeM, time zones and monotonic clocks."
sources: ["https://hackage.haskell.org/package//time", "https://hackage.haskell.org/package//random"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The time library

**Goal:** correct date/time handling. Package: `time`.

```haskell
import Data.Time
import Data.Time.Clock.POSIX (getPOSIXTime)
import GHC.Clock (getMonotonicTime)

now <- getCurrentTime                                       -- UTCTime (UTC instant)
let day = utctDay now                                       -- Day
fromGregorian 2026 11 2                                     -- Day (invalid dates clip; use fromGregorianValid)
addDays 30 day; diffDays d2 d1
addUTCTime 3600 now; diffUTCTime t2 t1                      -- NominalDiffTime (seconds)
formatTime defaultTimeLocale "%Y-%m-%dT%H:%M:%S%QZ" now
parseTimeM True defaultTimeLocale "%Y-%m-%d" "2026-11-02" :: Maybe Day
tz <- getCurrentTimeZone; utcToLocalTime tz now             -- LocalTime (no zone)
utcToZonedTime tz now
```
Elapsed measurement: `GHC.Clock.getMonotonicTime` (in base).

## Facts
- Types: `UTCTime` (instant), `Day`, `TimeOfDay`, `LocalTime` (day + time, no zone), `ZonedTime`, `NominalDiffTime`/`DiffTime`.
- `iso8601Show` and `iso8601ParseM` are in `Data.Time.Format.ISO8601`.

## Gotchas
- Never store `LocalTime` for events; store `UTCTime` and the zone name.
- `parseTimeM`'s first argument says whether to accept leading and trailing whitespace; it fails (in `MonadFail`) if the input does not match the format.
- Month arithmetic (`addGregorianMonthsClip`) clips end-of-month.
- `NominalDiffTime` ignores leap seconds.

## Self-check
- [ ] Timers use a monotonic clock.
- [ ] Persisted timestamps are UTC.

## Checked

2026-11-03. Confirmed against the time Data.Time.Format, Calendar, Clock, LocalTime, ISO8601 pages and base GHC.Clock: fromGregorian clipping, addGregorianMonthsClip, parseTimeM whitespace flag, %Q, leap seconds, getMonotonicTime. Removed: System.Clock, aeson and tz/timezone-olson claims.
Method: documentation only; no commands were run.
