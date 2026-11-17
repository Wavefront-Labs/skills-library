---
id: computing-software.data-engineering.apache-flink.window-table-valued-functions
name: window-table-valued-functions
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-sql, table-api, window-tvf, tumble, hop, cumulate, session-window, window-top-n, window-join]
level: practitioner
status: docs-checked
description: "Write Flink SQL windowed queries with window TVFs: TUMBLE, HOP, CUMULATE and SESSION, time attributes, window aggregation, Top-N, deduplication and window joins."
sources:
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/sql/reference/queries/window-tvf.md
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/sql/reference/queries/window-agg.md
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/sql/reference/queries/window-topn.md
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/sql/reference/queries/window-deduplication.md
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/sql/reference/queries/window-join.md
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Flink SQL window table-valued functions

**Goal:** windowed aggregations in Flink SQL that emit one final result per window and purge state when the window is done.

## 1. Time attribute
In streaming mode the time column must be an event-time or processing-time attribute (see watermarks-in-flink-sql). In batch mode it must be a TIMESTAMP or TIMESTAMP_LTZ column.

## 2. The TVFs
Four built-ins, used in a FROM clause. Each returns all input columns plus `window_start`, `window_end` and `window_time` (always `window_end - 1ms`; in streaming it is a time attribute usable in later windowing, interval joins and over aggregations). The original time column becomes a regular timestamp.
```sql
TUMBLE(TABLE data, DESCRIPTOR(timecol), size [, offset])
HOP(TABLE data, DESCRIPTOR(timecol), slide, size [, offset])         -- slide first, then size
CUMULATE(TABLE data, DESCRIPTOR(timecol), step, size [, offset])     -- size must be an integral multiple of step
SESSION(TABLE data [PARTITION BY keycols], DESCRIPTOR(timecol), gap) -- streaming only
```
```sql
SELECT window_start, window_end, SUM(price) AS total_price
FROM TUMBLE(TABLE Bid, DESCRIPTOR(bidtime), INTERVAL '10' MINUTES)
GROUP BY window_start, window_end;
```
- Tumbling windows have fixed size and do not overlap; hopping windows overlap when slide < size, so a row can fall in several windows; cumulating windows share a start and grow by step up to size (e.g. step 1 hour, size 1 day gives [00:00,01:00), [00:00,02:00) ... [00:00,24:00)); session windows close after a gap of inactivity.
- Named parameters work (`DATA =>`, `TIMECOL =>`, `SIZE =>`, ...); the DATA parameter must be first.- Window aggregation groups by `window_start, window_end` (plus optional keys; GROUPING SETS, ROLLUP and CUBE are shown in the docs). Unlike other continuous aggregations it emits only the final result at window end and purges intermediate state.
- Session windows: no aggregation optimisations from the performance tuning page; session window join, TopN and deduplication are in beta.

## 3. Patterns on top
- Window Top-N: `ROW_NUMBER() OVER (PARTITION BY window_start, window_end [, keys] ORDER BY col DESC)` then filter on the row number. PARTITION BY must contain `window_start` and `window_end`.
- Window deduplication: same pattern ordered by a time attribute; ASC keeps the first row, DESC the last. The pattern must be followed exactly or the optimiser will not translate it. The page both says event or processing time are supported and, in its limitations, that the order key must currently be an event time attribute; treat processing-time ordering as unsupported.
- Window join: supports INNER, LEFT, RIGHT, FULL OUTER, ANTI and SEMI; join condition includes `L.window_start = R.window_start AND L.window_end = R.window_end`. Limitation: the windowing TVFs on both inputs must currently be the same.
All of these emit final results only and purge state.

## 4. Gotchas
- The legacy Group Window Aggregation (`GROUP BY TUMBLE(time_attr, ...)`) is deprecated in favour of TVFs, and only supports window aggregation, not Top-N or joins.
- In batch mode, SESSION is not supported.

## Checked
Method: 2026-11-08 read the window-tvf page (TUMBLE, HOP, CUMULATE, SESSION sections) and checked the window-agg, window-topn, window-deduplication and window-join pages (full text of intro/limits via targeted search plus syntax sections). Added those pages as sources since the old single time-attributes source did not support these claims. Removed unsupported claims: update/retract output for ungrouped queries, late-row dropping, mini-batch/two-phase tuning, Kafka idle timeout tip, and the EXPLAIN/state verify steps. Corrected dedup ordering caveat and session beta status.
