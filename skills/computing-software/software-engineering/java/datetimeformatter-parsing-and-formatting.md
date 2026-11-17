---
id: computing-software.software-engineering.java.datetimeformatter-parsing-and-formatting
name: datetimeformatter-parsing-and-formatting
category: computing-software
field: software-engineering
product: java
tags: [java, java-time-api, datetimeformatter, iso-8601, parse-resolver-style, locale, pattern-letters]
level: practitioner
status: docs-checked
description: "Format and parse with java.time DateTimeFormatter: ISO constants, pattern letters (y vs u, h vs H, Y), default FORMAT locale, resolver styles and thread safety."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/format/DateTimeFormatter.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DateTimeFormatter

## Prefer constants for interchange
```java
DateTimeFormatter.ISO_LOCAL_DATE;           // 2011-12-03
DateTimeFormatter.ISO_OFFSET_DATE_TIME;     // 2011-12-03T10:15:30+01:00
DateTimeFormatter.ISO_INSTANT;              // 2011-12-03T10:15:30Z
```
Use ISO for APIs and storage. Pattern formatters are for human-facing output.

## Custom patterns
```java
var f = DateTimeFormatter.ofPattern("dd MMM uuuu HH:mm", Locale.UK);
LocalDateTime.parse("03 Nov 2026 09:30", f);
```
Pattern letters that bite (per the Javadoc table):
- `y` is year-of-era, `u` is year; `G` is era. For a proleptic year use `uuuu`.
- `Y` is week-based-year, `w` week-of-week-based-year: use `y`/`u` for calendar years.
- `H` hour-of-day (0-23), `h` clock-hour-of-am-pm (1-12, pair with `a`), `K` hour-of-am-pm (0-11), `k` clock-hour-of-day (1-24).
- `M`/`L` month-of-year: fewer than 3 letters is a number, 3 or more is text. Text style: under 4 letters short, exactly 4 full, 5 narrow. `m` is minute-of-hour.
- `S` fraction-of-second (1 to 9 letters, truncated), `n` nano-of-second.
- Up to two letters of `d`, `H`, `h`, `K`, `k`, `m`, `s` may be used. Two-letter `yy` parses with base 2000 (2000-2099).
- Every letter A-Z and a-z is reserved; an unrecognised letter is an error. Quote literal text in single quotes (`'T'`), and `''` is a literal quote.
- `[` `]` mark an optional section; `#`, `{`, `}` are reserved.

## Locale and zones
`ofPattern(String)` uses the default FORMAT locale; change it with `withLocale(Locale)` or `ofPattern(String, Locale)`. An `Instant` holds only a point in time, so it cannot be formatted as date or time without a zone: `ISO_INSTANT` handles that using UTC, and `withZone(ZoneId)` overrides the zone for other formatters (the value is converted to a `ZonedDateTime` before formatting).

## Resolving
Parsing has two phases: parse text into fields, then resolve them into a date/time. `ResolverStyle` has STRICT, SMART and LENIENT; SMART is the default and is what the localized-style factories use. Set with `withResolverStyle(ResolverStyle)`. See the `ResolverStyle` Javadoc for exactly which out-of-range values each style accepts.

## Gotchas
- A `DateTimeFormatter` is immutable and thread-safe (the Javadoc says so), so a `static final` constant is fine.
- Parse failures throw `DateTimeParseException`, which carries the error index.
- Unquoted non-letter characters are output directly today, but the Javadoc recommends quoting all literal text so future changes do not break it.

## Verify
Round-trip test: `parse(format(x)).equals(x)` for edge dates (Feb 29, Dec 31) and a locale other than your own.

## Checked
Confirmed on the DateTimeFormatter Javadoc (Java SE 21): predefined ISO constants and example outputs, the pattern letter table and count rules, default FORMAT locale, withZone behaviour, ISO_INSTANT note, resolver styles (SMART default), immutability and thread safety, DateTimeParseException error index.
Removed: the claim that STRICT requires an era with `yyyy`, the 2026-02-30 behaviour per style, the CLDR/COMPAT locale-provider note, and the dev.java source (page returned no text).
Method: docs-only read of cited pages, 2026-11-08
