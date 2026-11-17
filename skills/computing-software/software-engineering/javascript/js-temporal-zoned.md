---
id: computing-software.software-engineering.javascript.js-temporal-zoned
name: js-temporal-zoned
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, temporal-zoneddatetime, js-dates]
level: advanced
status: docs-checked
description: "Choose between Temporal Instant, PlainDate, PlainDateTime, ZonedDateTime and Duration for time zone aware, DST-safe date arithmetic, per the TC39 Temporal docs."
sources:
  - https://tc39.es/proposal-temporal/docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temporal ZonedDateTime and Duration

- Temporal is a global namespace object (like Math) that brings a modern date and time API to ECMAScript, with first-class time zone support including DST-safe arithmetic. The proposal docs point to MDN as the main API reference; check MDN for current engine support before relying on it.
- Types:
  - `Temporal.Instant`: a fixed point in time (exact time), with no calendar or location.
  - `Temporal.ZonedDateTime`: a time zone and calendar aware date and time for a real event, optimised for DST-safe arithmetic; it combines an Instant and a PlainDateTime with a time zone identifier.
  - `Temporal.PlainDate`, `PlainTime`, `PlainDateTime`, `PlainYearMonth`, `PlainMonthDay`: types with no associated time zone ("Plain" prefix).
  - `Temporal.Duration`: a length of time used for arithmetic and for differences between Temporal objects.
- `Temporal.Now.zonedDateTimeISO()` returns the current date and wall-clock time in the system time zone; `Temporal.Now.instant()` returns the current exact time; `Temporal.Now.timeZoneId()` returns the system time zone.
- Converting between Plain types and exact-time types (Instant, ZonedDateTime) can be ambiguous because of time zones and DST; Temporal lets you configure how the ambiguity is resolved. For arithmetic with a zone, PlainDateTime's docs recommend ZonedDateTime because it adjusts for DST automatically.
- Duration units do not wrap around by default: 90 minutes stays 90 minutes unless you balance it (see the Balancing doc).
- Time zones: use IANA identifiers such as `America/Los_Angeles`. Fixed-offset identifiers like `+05:30` are allowed but discouraged, because offsets for a place can change with political decisions. A time zone is required to convert an Instant or PlainDateTime to a ZonedDateTime.

Self-check: pick a date range that crosses a DST change in a chosen IANA zone, do the arithmetic on a ZonedDateTime, and confirm the result against the Time Zones and Resolving Ambiguity doc.

## Checked

Checked 2026-11-08 against the TC39 Temporal proposal documentation index (type descriptions, Temporal.Now list, ambiguity note, time zones section, Duration balancing note). Removed: the engine support statement, the `@js-temporal/polyfill` mention, the `add({ days: 1 })` and `until()`/`since()` examples, and the immutability and strict-units claims (not on the cited page).
Method: docs-only read of cited pages, 2026-11-08
