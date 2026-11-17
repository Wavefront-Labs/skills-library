---
id: computing-software.software-engineering.clojure.java-time-instant-zoneddatetime-duration
name: java-time-instant-zoneddatetime-duration
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, java-time, instant, local-date, zoned-date-time, duration, formatter, inst, timezones, clojure-java-time, java-time-interop, clojure-time]
level: practitioner
status: draft
description: "Handle dates and times with java.time (Instant, LocalDate, ZonedDateTime, Duration, DateTimeFormatter), convert java.util.Date and #inst, and avoid timezone traps."
sources: ["https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/time/package-summary.html", "https://clojure.org/reference/java_interop"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# java.time from Clojure

**Goal:** correct date/time handling with the JDK's immutable API.

```clojure
(import '(java.time Instant LocalDate ZonedDateTime ZoneId Duration)
        '(java.time.format DateTimeFormatter))
(Instant/now)  (Instant/parse "2026-01-01T00:00:00Z")
(LocalDate/of 2026 11 2)  (.plusDays d 7)  (.isBefore d1 d2)
(ZonedDateTime/now (ZoneId/of "Australia/Sydney"))
(Duration/between t1 t2)  (.toMillis dur)
(.format (DateTimeFormatter/ofPattern "yyyy-MM-dd HH:mm") zdt)
(LocalDate/parse "2026-11-02")
(.toInstant #inst "2026-01-01")        ; java.util.Date -> Instant  (since Clojure 1.9, Instant is also a valid #inst)
(java.util.Date/from instant)          ; Instant -> Date
```
- Prefer `Instant` for machine timestamps (UTC), `LocalDate` for calendar dates without zone,
  `ZonedDateTime` for human-facing times with zone rules. Store UTC; convert at the edge.
- `#inst` literals are `java.util.Date`; `inst?` and `inst-ms` work on both Date and Instant (1.9+).
- Use IANA zone ids (`Australia/Sydney`), not offsets like `+10:00`, for recurring local times (daylight saving).
- `DateTimeFormatter` is thread-safe; `SimpleDateFormat` is not: avoid it.
- Library `clojure.java-time` / `tick` wrap java.time with Clojure idioms; core interop is enough for most code.
- Arithmetic: `(.plus instant (Duration/ofHours 2))`, `(.until a b ChronoUnit/DAYS)`.

## Failure modes
- `DateTimeParseException` on unexpected formats: parse with an explicit formatter.
- `UnsupportedTemporalTypeException` when asking an Instant for a calendar field; convert to a ZonedDateTime.

## Self-check
Parse a UTC instant, convert to Sydney time, and format it; confirm the offset changes across DST.
