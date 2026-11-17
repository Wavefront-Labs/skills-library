---
id: computing-software.database-administration.clickhouse.with-fill-time-series-gaps
name: with-fill-time-series-gaps
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, with-fill, step, gaps, time-series, tostartofinterval, interpolate]
level: practitioner
status: docs-checked
description: "Fill missing time buckets in ClickHouse results with ORDER BY ... WITH FILL FROM ... TO ... STEP, and carry values with INTERPOLATE."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/developer/time-series-filling-gaps.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# with fill time series gaps
Bucketed time-series queries omit buckets that have no rows. Add `WITH FILL` to the `ORDER BY` column to emit them with default (0 for counts) values.
```sql
SELECT
    toStartOfInterval(timestamp, toIntervalMillisecond(100)) AS bucket,
    count() AS count
FROM images
WHERE (timestamp >= {start:String}) AND (timestamp <= {end:String})
GROUP BY ALL
ORDER BY bucket ASC
WITH FILL
FROM toDateTime64({start:String}, 3)
TO toDateTime64({end:String}, 3) + INTERVAL 1 millisecond
STEP toIntervalMillisecond(100);
```
- `STEP` is the size of the gaps to fill. It defaults to 1 second for DateTime types, so set it for finer buckets.
- Without `FROM`, there is still a gap at the beginning of the range; `FROM` fixes it.
- Without `TO`, buckets after the last row are missing. `TO` is not inclusive, so the page adds a small amount (`+ INTERVAL 1 millisecond`) to the end time to include it.

Filled rows break running totals: with `sum(count) OVER (ORDER BY bucket) AS cumulative`, the filled rows show 0 in `cumulative` rather than the previous value. Add `INTERPOLATE (cumulative)` after `STEP` so filled rows reuse the previous value; list every derived column there (the page adds `barChart`, from `bar(cumulative, 0, 10, 10)`, as `INTERPOLATE (cumulative, barChart)`).

## Checked
2026-11-03. Confirmed against the "Filling gaps in time-series data" page. Removed: the claim that `STEP` must match the bucket width or rows duplicate or shift, and the "600 rows for a one-minute window" Verify step; neither is on the page. Added the `TO` and `INTERPOLATE` behaviour that the page covers.
Method: documentation only; no commands were run.
