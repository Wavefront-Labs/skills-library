---
id: computing-software.software-engineering.javascript.js-date-parsing-pitfalls
name: js-date-parsing-pitfalls
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, date-parsing, js-dates]
level: practitioner
status: docs-checked
description: "Avoid Date parsing pitfalls: ISO format only, UTC versus local interpretation, zero-based months, invalid dates, DST gaps and legacy two-digit years."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date parsing and time zone pitfalls

- A `Date` holds one number: milliseconds since the epoch (1970-01-01T00:00:00Z), independent of time zone. The component getters and setters (`getHours()`, `getDate()` ...) work in local time; the `getUTC*` and `setUTC*` variants work in UTC. The local zone is not stored in the object.
- The only string format the specification requires is the date time string format, a simplified ISO 8601: `YYYY-MM-DDTHH:mm:ss.sssZ`, where date-only forms (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`) and a time part (`THH:mm`, `THH:mm:ss`, `THH:mm:ss.sss`) are allowed, with an optional `Z` or `+HH:mm` offset. Other formats are implementation-specific; MDN says to prefer the standard format and to cross-browser test anything else (`new Date("December 17, 1995 03:24:00")` is marked discouraged).
- With no offset, a date-only string such as `"2025-03-01"` is read as UTC, but a date-time string such as `"2025-03-01T00:00"` is read as local time (the UTC reading of date-only forms is a historical spec error kept for web compatibility). The local getters therefore show a different day in zones west of UTC.
- Months are zero-based (`new Date(1995, 11, 17)` is 17 December 1995); `getDate()` is the day of month (1 to 31) and `getDay()` is the weekday (0 to 6). Overflowing a component carries into the next (month 12 becomes January of the next year; day 0 becomes the last day of the previous month).
- Two-digit years passed to the constructor, `Date.UTC()` or `setYear()` are treated as offsets, usually from 1900 (`new Date(99, 5, 24)` is 24 June 1999). Use `setFullYear()` for years 0 to 99.
- Invalid dates hold the timestamp `NaN`; out-of-range timestamps (beyond +/-8.64e15 ms) become "Invalid Date". Implementations are not required to reject out-of-bounds components in non-standard strings, and behave inconsistently for impossible dates like "February 30".
- `toISOString()` returns the standard format in UTC (`Z`), and `toJSON()` calls it. Use it or the epoch number to store or transmit instants.
- DST: the offset depends on the instant (`getTimezoneOffset()`). Setting a local time in a spring-forward gap moves it forward by the gap; in a fall-back overlap the earlier instant is chosen. Elapsed time in units larger than hours is affected by differing day lengths; MDN advises researching it carefully.
- MDN marks `Date` as a legacy feature now that Temporal exists, and suggests Temporal for new code (check browser compatibility).

Self-check: in a zone west of UTC, `new Date("2025-03-01").getDate()` reports 28, while `new Date("2025-03-01T00:00").getDate()` reports 1.

## Checked

Confirmed on the MDN Date page: epoch model, local versus UTC methods, date time string format and its UTC/local rule, zero-based months, two-digit years, NaN and range, `toISOString`/`toJSON`, DST disambiguation, Temporal note. Removed: the `Intl.DateTimeFormat` with `timeZone` advice and the "adding 24 h is not tomorrow" wording (replaced by what the page states about DST and elapsed time).

Method: docs-only read of cited pages, 2026-11-08
