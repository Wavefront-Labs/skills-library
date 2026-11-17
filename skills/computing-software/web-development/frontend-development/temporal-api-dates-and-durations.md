---
id: computing-software.web-development.frontend-development.temporal-api-dates-and-durations
name: temporal-api-dates-and-durations
category: computing-software
field: web-development
product: frontend-development
tags: [temporal-api, temporal-zoneddatetime, plaindate, durations, time-zones, javascript]
level: advanced
status: docs-checked
description: "Using the Temporal API (PlainDate, ZonedDateTime, Instant, Duration) for correct date arithmetic, time zones and DST, polyfills and interop with Date."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal/ZonedDateTime/add
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Temporal/Duration/total
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temporal API

Temporal replaces `Date`: immutable, 1-based months, explicit time zones, nanosecond precision. Per mdn/browser-compat-data it ships in Chrome 144 and Firefox 139, with Safari still in preview, so use a polyfill or check support before shipping.

## 1. Pick the type
| Type | Means | Example |
|---|---|---|
| `Temporal.Instant` | exact moment, no zone | log timestamps |
| `Temporal.ZonedDateTime` | moment + IANA zone | meeting at 09:00 Europe/London |
| `Temporal.PlainDate` | calendar date | birthday, due date |
| `Temporal.PlainTime` / `PlainDateTime` | wall-clock without zone | store opening hours |
| `Temporal.Duration` | amount of time | "2 h 30 min" |

## 2. Arithmetic
```js
const d = Temporal.PlainDate.from("2026-01-31");
d.add({ months: 1 });                         // 2026-02-28  (overflow: "constrain" default)
d.add({ months: 1 }, { overflow: "reject" }); // throws RangeError
const meet = Temporal.ZonedDateTime.from("2026-03-28T09:00[Europe/London]");
meet.add({ days: 1 }).toString();             // 09:00 next day across DST change (wall clock kept)
meet.add({ hours: 24 });                      // 10:00 local: exact elapsed time
```
Differences:
```js
const a = Temporal.PlainDate.from("2026-01-15"), b = Temporal.PlainDate.from("2026-10-18");
a.until(b, { largestUnit: "month" }).toString();   // "P9M3D"
Temporal.PlainDate.compare(a, b);                   // -1
```

## 3. Now and conversion
```js
Temporal.Now.instant();
Temporal.Now.zonedDateTimeISO("America/New_York");
Temporal.Now.plainDateISO();                       // today in system zone
const inst = Temporal.Instant.fromEpochMilliseconds(legacyDate.getTime());
const zdt = inst.toZonedDateTimeISO("Asia/Tokyo");
new Date(zdt.epochMilliseconds);                    // back to Date for old APIs
```
Formatting: `zdt.toLocaleString("en-GB", { dateStyle: "full", timeStyle: "short" })` (uses Intl).

## 4. Storage and APIs
Send `Instant` as ISO string with `Z`; send `ZonedDateTime` with the bracketed zone (`2026-03-28T09:00:00+00:00[Europe/London]`) when the zone matters for future recurrence; store `PlainDate` as `YYYY-MM-DD` (DB `date` column), never as midnight UTC.

## Gotchas
- Comparing with `<` throws on purpose; use `compare` or `equals`.
- `Duration` with months/years needs a `relativeTo` date to total or round (`d.total({ unit: "day", relativeTo: start })`).

## Verify
- [ ] Tests cover DST-transition days, Jan 31 + 1 month and leap years.

## Checked

2026-10-26. MDN Temporal overview, PlainDate add/valueOf (valueOf throws TypeError so `<` cannot be used), ZonedDateTime.add (date part uses calendar arithmetic, time part uses exact time), Duration.total (needs relativeTo for calendar units) and browser-compat-data for support. The DST example (24 hours from 09:00 GMT on 28 Mar 2026 is 10:00 BST) follows from the UK clock change on the last Sunday of March. Removed the unconfirmed polyfill-size claim and the polyfill package names.

Method: documentation only; no commands were run.
