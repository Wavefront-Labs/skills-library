---
id: computing-software.web-development.frontend-development.intl-datetimeformat-and-time-zones
name: intl-datetimeformat-and-time-zones
category: computing-software
field: web-development
product: frontend-development
tags: [intl-api, intl-datetimeformat, time-zones, i18n, dates, javascript]
level: practitioner
status: verified
description: "Formatting dates with Intl.DateTimeFormat across locales and time zones: storing UTC, timeZone option, formatRange, DST traps, and the Temporal API."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal
  - https://tc39.es/ecma402/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Intl.DateTimeFormat and time zones

## 1. Storage rule
Store instants as UTC (ISO 8601 with `Z`, or epoch ms). Store the user's IANA zone (`Europe/London`) separately when wall-clock meaning matters (meetings, opening hours). Never store offsets like `+01:00` as a zone - they change with DST.

## 2. Format
```js
const fmt = new Intl.DateTimeFormat(navigator.language, {
  dateStyle: "medium", timeStyle: "short", timeZone: "America/New_York",
});
fmt.format(new Date("2026-03-08T07:30:00Z"));   // "Mar 8, 2026, 3:30 AM" in en-US
new Intl.DateTimeFormat("en-GB", { weekday: "long", day: "numeric", month: "long", timeZoneName: "short" }).format(d);
fmt.formatRange(start, end);                      // "Mar 8 – 10, 2026", collapses shared parts
fmt.formatToParts(d);                             // for custom markup
Intl.DateTimeFormat().resolvedOptions().timeZone; // user's zone
```
- `dateStyle`/`timeStyle` cannot be mixed with component options (`month`, `hour`) - `TypeError`.
- Reuse formatter instances; constructing them is expensive (20 000 `new Intl.DateTimeFormat(...).format()` calls took about 0.9 s versus 16 ms with one reused instance in Node 20; cache by locale+options).
- `dateStyle` plus `month` threw `TypeError` in a test.
- `hourCycle: "h23"` forces 24h; otherwise locale decides.

## 3. Traps
- `new Date("2026-03-08")` (date-only) is parsed as **UTC** midnight; `new Date("2026-03-08T00:00")` is **local**. A birthday shown in a western zone becomes the previous day. Keep date-only values as strings or `Temporal.PlainDate`.
- Arithmetic across DST: adding `24*3600*1000` ms is not "one day" in local time. Use `setDate(d.getDate() + 1)` or Temporal `add({ days: 1 })`. Checked in `America/New_York` across 2026-03-08: noon 7 Mar plus 24 h gave 13:00 on 8 Mar, `setDate(+1)` gave 12:00; with `@js-temporal/polyfill`, `ZonedDateTime.add({days:1})` gave `12:00-04:00` and `add({hours:24})` gave `13:00-04:00`.
- Server-rendered dates differ from client hydration when zones differ - format with an explicit `timeZone` on both sides or render on the client only (React hydration mismatch warnings).
- Never parse locale-formatted strings back with `Date` - parse ISO only.

## 4. Temporal
`Temporal.ZonedDateTime`, `PlainDate`, `Instant` fix the above (MDN compat data: Firefox 139+, Chrome 144+, Safari only in Technology Preview; `Temporal` is undefined in Node 20, so use the `@js-temporal/polyfill` there and in other browsers). `Temporal.Now.zonedDateTimeISO("Asia/Tokyo")`.

## Verify
Run tests under several zones: `TZ=America/Los_Angeles node --test` and `TZ=Asia/Kolkata`, including DST-transition dates. On Windows (Git Bash) the `TZ=` environment variable was ignored by Node 20 (it reported `Australia/Brisbane`); setting `process.env.TZ = "America/New_York"` at the top of the script did change the zone, so use that or `cross-env` there.
