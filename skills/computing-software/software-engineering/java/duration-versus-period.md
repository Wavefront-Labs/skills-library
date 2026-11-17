---
id: computing-software.software-engineering.java.duration-versus-period
name: duration-versus-period
category: computing-software
field: software-engineering
product: java
tags: [java, java-time-api, duration-vs-period, chronounit, temporal, date-arithmetic, between]
level: practitioner
status: docs-checked
description: "Choose Duration (seconds and nanos) or Period (years, months, days) in java.time, compute differences with between and ChronoUnit, and avoid month-end and DST surprises."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/Duration.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/Period.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/LocalDate.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/temporal/ChronoUnit.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/ZonedDateTime.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duration versus Period

| | Duration | Period |
|---|---|---|
| Measures | seconds plus nanoseconds (time-based) | years, months and days (date-based) |
| Days | a day is exactly 24 hours (86,400 seconds), DST is ignored | a calendar day |
| Typical | timeouts, elapsed time | ages, terms, calendar offsets |

```java
Duration timeout = Duration.ofSeconds(30);
Duration d = Duration.between(start, end);   // start inclusive, end exclusive
d.toMinutes(); d.toMillis();
Period p = Period.between(birth, today);     // LocalDate start inclusive, end exclusive
p.getYears();
LocalDate.of(2024, 1, 31).plusMonths(1);     // 2024-02-29: day-of-month clamped
```
(`start`, `end`, `birth` and `today` are placeholders.)

- `Duration.between` needs temporals that support the SECONDS unit and throws `DateTimeException` if the seconds cannot be obtained. The result is negative if end is before start; call `abs()` when you want the magnitude.
- `Period.between(2010-01-15, 2011-03-18)` is 1 year, 2 months, 3 days (Javadoc example).
- Period months are not normalised into years: 15 months is not 1 year 3 months. `toTotalMonths()` is years times 12 plus months and ignores days.

## Total difference in one unit
```java
ChronoUnit.DAYS.between(a, b);       // whole complete units; negative if b is before a
a.until(b, ChronoUnit.HOURS);        // equivalent form
```
`ChronoUnit.X.between(start, end)` is start inclusive, end exclusive and counts only complete units. It is equivalent to `start.until(end, unit)`.

## DST
`Period.ofDays(1)` added to a `ZonedDateTime` with `plusDays` or `plus(Period)` works on the local time-line: the days are added to the local date-time and converted back using the zone. A `Duration` of days is always 24 hours. Choose by intent: "same time tomorrow" is a Period, "24 hours later" is a Duration.

## Parsing
- `Duration.parse("PT1H30M")` accepts the ISO-8601 form `PnDTnHnMn.nS`, with days taken as exactly 24 hours.
- `Period.parse("P1Y2M")` accepts `PnYnMnD` and `PnW` (weeks multiplied by 7), for example `"P5D"`.

## Gotchas
- Months have no fixed length, so `Duration.ofDays(30)` is 30 times 24 hours, not one month.
- `plusMonths` clamps to the last valid day of the new month, so adding a month and then subtracting one may not return the original date.

## Verify
Compare `ChronoUnit.DAYS.between` and `Period.between` for the same two dates in a unit test, and test a `ZonedDateTime` across a DST change in your zone with both `plusDays` and `plus(Duration.ofDays(1))`.

## Checked
2026-11-03. Confirmed against the Java SE 21 pages for Duration, Period, LocalDate, ChronoUnit and ZonedDateTime: seconds/nanos and 24-hour day, between inclusivity and exceptions, Period fields and example, parse formats, toTotalMonths, plusMonths clamping, ChronoUnit.between semantics, local time-line behaviour of date units.
Removed (not in the pages read): the `Thread.sleep(Duration)` Java 19 claim, "Java 9+" for `*Part` methods, the claim that `Duration.between` on `LocalDate` throws `UnsupportedTemporalTypeException` (only `DateTimeException` is documented), the "works with" type list, the sample `P34Y2M5D` output, an unrun `Period.between(2024-01-31, 2024-03-01)` check, and the dev.java source (page unavailable).
Method: documentation only; no commands were run.
