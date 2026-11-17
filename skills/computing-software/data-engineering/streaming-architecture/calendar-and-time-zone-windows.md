---
id: computing-software.data-engineering.streaming-architecture.calendar-and-time-zone-windows
name: calendar-and-time-zone-windows
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, calendar-windows, time-zones, daily-windows, window-offset, dst, event-time]
level: advanced
status: draft
description: "Build day, week and month windows aligned to a local time zone in streaming engines: offsets, DST shifts, month lengths, and when to aggregate hourly then roll up."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/timezone/
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.window.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calendar and time-zone aligned windows

Engines align tumbling windows to the Unix epoch in **UTC**. A "daily" window is therefore midnight-to-midnight UTC, which is wrong for a business in Sydney or New York.

## Fixed offsets
```java
// Flink DataStream: day windows starting at 00:00 UTC+10 (offset -10 h)
.window(TumblingEventTimeWindows.of(Duration.ofDays(1), Duration.ofHours(-10)))
```
```python
# Spark: window(timeColumn, windowDuration, slideDuration, startTime)
df.groupBy(F.window("ts", "1 day", "1 day", "14 hours"))   # 00:00 at UTC+10 = 14:00 UTC
```
Offsets are fixed: they ignore **daylight saving**. A region with DST is off by one hour for half the year.

## DST-correct approaches
1. **Flink SQL with TIMESTAMP_LTZ** and session time zone: window TVFs on a `TIMESTAMP_LTZ` rowtime use `table.local-time-zone` for alignment, so `TUMBLE(..., INTERVAL '1' DAY)` produces local-day windows including DST shifts (23 h and 25 h days).
```sql
SET 'table.local-time-zone' = 'Australia/Sydney';
SELECT window_start, window_end, SUM(amount)
FROM TABLE(TUMBLE(TABLE orders, DESCRIPTOR(ts_ltz), INTERVAL '1' DAY)) GROUP BY window_start, window_end;
```
2. **Compute a local calendar key and group by it** (works everywhere): `local_date = to_date(from_utc_timestamp(ts, 'America/New_York'))` (Spark) and aggregate by `(local_date, key)` with a watermark. The "window" end is then "watermark passed local midnight in that zone"; implement with state + timers (Flink `KeyedProcessFunction` registering a timer at next local midnight converted to UTC).
3. **Aggregate hourly in UTC, roll up downstream**: hours are unambiguous (except half-hour-offset zones like India +5:30 and Nepal +5:45: use 15-minute buckets for global coverage). Daily/weekly/monthly totals per time zone are a cheap second-stage aggregation (or a warehouse query). Most robust for multi-region businesses.

## Weeks and months
- Weeks: decide ISO week (Monday start) vs locale; epoch-aligned 7-day windows start on a Thursday (1970-01-01). Use offsets or a calendar key.
- Months: variable length; tumbling windows cannot express them. Use a calendar key (`date_trunc('month', local_ts)`) with timers, or roll up from daily.

## Late data and finalisation
A local day closes when the watermark passes local midnight; keep allowed lateness/grace for stragglers and emit corrections. Downstream reports should show "provisional" until then.

## Verify
- [ ] Test DST transition days (23 h / 25 h) and a half-hour-offset zone with fixed fixtures.
- [ ] Daily totals equal a batch query grouped by local date.
