---
id: computing-software.data-engineering.druid.druid-compaction-use-cases
name: druid-compaction-use-cases
category: computing-software
field: data-engineering
product: druid
tags: [compaction, segment-size, small-segments, query-granularity, dimension-order]
level: practitioner
status: docs-checked
description: "Recognise when to compact Druid segments, what compaction can change, and how it handles granularity, dimensions and rollup."
sources:
  - https://github.com/apache/druid/blob/master/docs/data-management/compaction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Query performance depends on optimally sized segments. Compaction tasks read existing segments for an interval and combine the data into a new compacted set, sometimes larger but fewer, sometimes smaller. Fewer, better-sized segments need less per-segment processing and less memory overhead for ingestion and querying.

## When to compact

- Streaming ingestion delivers data out of order and creates many small segments.
- Native batch uses `appendToExisting`, producing suboptimal segments.
- `index_parallel` tasks create many small segments.
- A misconfigured task created oversized segments.
- Not helpful everywhere: if every ingestion task rewrites the data, you do not need compaction. Check the segment optimization guidance first.

## What it can change

By default compaction does not modify the data. You can deliberately:
- Increase segment granularity when the interval's data is sparse.
- Coarsen the query granularity of older data (minute to hour, hour to day) to save storage.
- Change dimension order to improve sorting and shrink segments.
- Remove unused columns or apply an aggregation metric to older data.
- Switch from dynamic partitioning with best-effort rollup to hash or range partitioning with perfect rollup.

## Ways to run it

- Automatic compaction is the first option. The Coordinator periodically finds segments, newest to oldest, that are uncompacted or compacted with a different spec, and submits compaction tasks for their interval.
- Use manual compaction tasks when auto compaction is limited by its task slots (manual tasks can use all available slots and run more intervals concurrently), or to force a specific time range or compact out of chronological order.
- For different compaction configs at different data ages (coarsening, deleting old rows, changing compression) the page points to cascading reindexing.

## Behaviour to know

- Druid overwrites the original segments with the compacted set and locks the interval. If an ingestion task needs a locked interval, by default ingestion supersedes compaction and the compaction task fails. Avoid conflicts by adjusting the input interval (manual), setting `skipOffsetFromLatest` (auto), or giving compaction higher priority than ingestion.
- `dropExisting` in `ioConfig` set to true replaces all existing segments fully contained by the interval. The page marks it beta.
- Segment granularity is retained unless you change it in `granularitySpec`. Non-overlapping segments of different granularity get separate compaction tasks. For overlapping ones Druid uses the closest granularity level covering the overlapped span (a day segment overlapping a month-long segment compacts to month granularity).
- Query granularity is retained unless changed; if inputs differ, the finest wins (day plus minute gives minute). Going coarser (month to year) overshadows the finer segments, and a later kill task on the overshadowed segments permanently loses the finer data.
- Dimensions: if inputs differ, the output holds all dimensions; recent segments take precedence for order and types. Set a custom `dimensionsSpec` to control order or types.
- Rollup: the output is rolled up only when `rollup` is set on all input segments. Verify with a segment metadata query.

## Checked

2026-11-08. Read the cited compaction page in full. Expanded the draft with the data-handling rules (locking and conflicts, granularity, dimension and rollup behaviour) and the manual vs automatic guidance; added the stated caveat that compaction does not always help.

Method: documentation only; no commands were run.
