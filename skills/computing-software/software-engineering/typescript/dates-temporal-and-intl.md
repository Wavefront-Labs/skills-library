---
id: computing-software.software-engineering.typescript.dates-temporal-and-intl
name: dates-temporal-and-intl
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, temporal-api, intl, date-handling, time-zones, intl-datetimeformat, intl-numberformat]
level: practitioner
status: gated
description: "Handle dates and formatting in JavaScript: Date pitfalls, Temporal types (Instant, ZonedDateTime, PlainDate), ISO strings at boundaries, and Intl for dates, numbers and plurals."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dates, Temporal and Intl

**Goal:** correct instants, calendar dates and time zones, and locale-aware display
without shipping big formatting libraries.

## Date pitfalls
```js
new Date("2026-03-01")              // UTC midnight (date-only ISO = UTC)
new Date("2026-03-01T00:00")        // LOCAL midnight (date-time without offset = local)
new Date(2026, 2, 1)                // month is 0-based: March
date.setMonth(1)                    // mutates in place; Jan 31 + 1 month -> Mar 3
```
`Date` is an instant (ms since epoch) with local-time accessors - no way to represent "a
calendar date" or "10:00 in Tokyo".

## Temporal (not global in Node 24.22: `typeof Temporal` was `undefined`; use `@js-temporal/polyfill` there. Browser support: MDN marks it "Limited availability", not Baseline; which browsers ship it by default was not confirmed (gated: unconfirmed, source is paywalled or blocked))
| Type | Represents | Example |
|---|---|---|
| `Temporal.Instant` | exact moment | log timestamps, DB `timestamptz` |
| `Temporal.ZonedDateTime` | moment + IANA zone | meeting at 10:00 Europe/Paris |
| `Temporal.PlainDate` | calendar date, no zone | birthday, invoice date |
| `Temporal.PlainTime` / `PlainDateTime` | wall-clock values | opening hours |
| `Temporal.Duration` | length of time | `P1M2DT3H` |
(The Temporal and Intl snippets below were run with `@js-temporal/polyfill` 0.5.1 and Node 24 / V8 13.6; outputs match the comments.)
```js
const meeting = Temporal.ZonedDateTime.from("2026-03-29T10:00[Europe/Paris]");
meeting.add({ days: 1 });                       // DST-aware, immutable
meeting.withTimeZone("America/New_York").toPlainTime();
Temporal.PlainDate.from("2026-01-31").add({ months: 1 });   // 2026-02-28 (constrain)
Temporal.Now.instant().epochMilliseconds;
```

## At boundaries
- Store/transmit instants as ISO 8601 UTC (`2026-03-01T09:30:00Z`) or epoch ms; calendar dates as
  `YYYY-MM-DD`; zoned events as instant **plus** IANA zone name (offsets alone don't survive DST).
- Do date arithmetic in the relevant zone, not UTC, when it means calendar days.

## Intl formatting (built in)
```js
new Intl.DateTimeFormat("en-GB", { dateStyle: "medium", timeStyle: "short", timeZone: "Europe/London" }).format(d);
new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(1234.5);   // "1.234,50 €"
new Intl.RelativeTimeFormat("en", { numeric: "auto" }).format(-1, "day");                 // "yesterday"
new Intl.PluralRules("en", { type: "ordinal" }).select(2);                               // "two" -> "2nd"
new Intl.ListFormat("en", { type: "conjunction" }).format(["a", "b", "c"]);             // "a, b, and c"
```
Create formatters once and reuse (construction is expensive). Server-side rendering: pass the
user's locale and zone explicitly, or SSR and client output will mismatch.

## Verify
- [ ] No `new Date(string)` parsing of non-ISO input; month indices reviewed.
- [ ] Tests cover DST transitions and month-end arithmetic in the user's zones.
