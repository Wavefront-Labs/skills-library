---
id: computing-software.database-administration.mongodb.datetrunc-and-time-zone-bucketing
name: datetrunc-and-time-zone-bucketing
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-aggregation, datetrunc, date-operators, timezone, time-bucketing]
level: practitioner
status: verified
description: "Group MongoDB data by day, week or hour in the right time zone with $dateTrunc, $dateToString, $dateDiff and $dateAdd, avoiding UTC-boundary errors."
sources:
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/dateTrunc/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/dateToString/
  - https://www.mongodb.com/docs/manual/reference/operator/aggregation/dateDiff/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# $dateTrunc and time-zone bucketing

**Goal:** daily/weekly reports whose day boundaries match the business's local time, not UTC. BSON dates are UTC; every date operator defaults to UTC unless given `timezone`.

## Daily totals in local time ($dateTrunc is New in 5.0)
```javascript
db.orders.aggregate([
  { $match: { createdAt: { $gte: ISODate("2026-10-01T00:00:00+10:00"), $lt: ISODate("2026-11-01T00:00:00+11:00") } } },
  { $group: {
      _id: { $dateTrunc: { date: "$createdAt", unit: "day", timezone: "Australia/Sydney" } },
      orders: { $sum: 1 }, revenue: { $sum: "$total" } } },
  { $sort: { _id: 1 } }
])
```
- `unit`: `year|quarter|month|week|day|hour|minute|second|millisecond`; `binSize: 15, unit: "minute"` gives 15-minute buckets.
- Weeks: `startOfWeek: "monday"` (default Sunday).
- Use Olson names (`Australia/Sydney`), not fixed offsets such as `"+10:00"` (accepted, but it never shifts for DST).
- Compute the `$match` range in the same zone (above) or the first/last day is partial.

## Older servers
```javascript
_id: { $dateToString: { format: "%Y-%m-%d", date: "$createdAt", timezone: "Australia/Sydney" } }
```
Returns a string; fine for grouping, worse for further date maths.

## Other operators
- `$dateDiff: { startDate, endDate, unit: "day", timezone }` counts boundaries crossed, not 24-hour periods.
- `$dateAdd` / `$dateSubtract` for "30 days ago" calculations relative to `$$NOW`.
- `$dateFromString` with `format` and `onError` to parse imported strings.
- `$week` / `$isoWeek` / `$isoWeekYear` for ISO week reports (year-end weeks belong to the ISO year).

## Gap filling
Follow with `$densify: { field: "_id", range: { step: 1, unit: "day", bounds: "full" } }` and `$fill` to emit zero rows for empty days.

## Gotchas
- Strings that look like dates are not dates; `$dateTrunc` on a string errors. Fix the data with `$toDate`.
- Time-series collections bucket on `timeField` in UTC; still truncate with `timezone` in queries.

## Verify
Pick an order placed at 23:30 local time; confirm it lands on the local date, not the next UTC date.

## Checked
- MongoDB 9.0.4 Community and mongosh 2.13.0 on Windows, run in a scratch folder. The Sydney daily `$group` returned local-day buckets (14:00Z before the 4 October 2026 DST start, 13:00Z after); the `$match` bounds with `+10:00` and `+11:00` evaluate to 2026-09-30T14:00Z and 2026-10-31T13:00Z. A 23:30Z order landed on the next Sydney day as expected.
- `binSize: 15` minute, `startOfWeek` (default Sunday 2026-09-27, monday 2026-09-28), all nine units, a fixed offset, `$dateToString`, `$dateDiff` (counts boundaries: 23:30 to 00:30 UTC across midnight = 1 day), `$dateAdd`, `$dateSubtract` on `$$NOW`, `$dateFromString` `onError`, `$week`/`$isoWeek`/`$isoWeekYear`, `$densify` + `$fill`, and `$dateTrunc` on a string ("requires 'date' to be a date") with `$toDate` as the fix all ran.
- Docs fetched: `$dateTrunc` page (New in version 5.0, `startOfWeek`).
