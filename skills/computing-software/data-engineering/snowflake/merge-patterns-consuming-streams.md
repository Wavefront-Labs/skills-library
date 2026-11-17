---
id: computing-software.data-engineering.snowflake.merge-patterns-consuming-streams
name: merge-patterns-consuming-streams
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, streams, stream-merge-pattern, metadata-action, metadata-isupdate, merge, cdc, tasks]
level: advanced
status: docs-checked
description: "Apply Snowflake stream changes to a target with MERGE: METADATA$ACTION/ISUPDATE semantics, dedup to latest per key, deletes, and advancing the offset exactly once."
sources:
  - https://docs.snowflake.com/en/user-guide/streams-intro
  - https://docs.snowflake.com/en/user-guide/streams-examples
  - https://docs.snowflake.com/en/sql-reference/sql/merge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MERGE patterns consuming streams

**Goal:** propagate inserts, updates and deletes captured by a stream into a downstream table correctly and idempotently.

## Stream metadata
Each stream row has `METADATA$ACTION` (`INSERT`/`DELETE`), `METADATA$ISUPDATE` (true when the INSERT/DELETE pair represents an update), `METADATA$ROW_ID`.
A standard (delta) stream shows the **net change** since the offset: an update appears as a DELETE (old) + INSERT (new) pair, both with `ISUPDATE = TRUE`. A row inserted and deleted within the window does not appear.

## Basic MERGE
```sql
merge into analytics.customers t
using (
  select * from raw.customers_stream
  where not (metadata$action = 'DELETE' and metadata$isupdate)   -- drop the "old" half of updates
) s
on t.customer_id = s.customer_id
when matched and s.metadata$action = 'DELETE' then delete
when matched and s.metadata$action = 'INSERT' then update set
  t.name = s.name, t.segment = s.segment, t.updated_at = s.updated_at
when not matched and s.metadata$action = 'INSERT' then insert
  (customer_id, name, segment, updated_at) values (s.customer_id, s.name, s.segment, s.updated_at);
```

## Dedup when the source can have multiple rows per key
Append-only streams on raw landing tables (e.g. CDC events) can hold several versions per key; MERGE returns an error when several source rows match one target row (`ERROR_ON_NONDETERMINISTIC_MERGE` = TRUE, the default). Keep the latest:
```sql
using (
  select * from (
    select *, row_number() over (partition by customer_id order by event_ts desc, event_seq desc) rn
    from raw.customer_events_stream) where rn = 1
) s
```
For CDC with op codes, map `op = 'd'` to delete in the `when matched` clause.

## Offset semantics
A stream's offset advances when a DML statement consumes its change data, so the data is no longer available to another consumer (see CREATE TASK and the streams docs). A plain MERGE that reads the stream consumes it once; use one stream per consumer.

## Task wiring
```sql
create or replace task etl.apply_customers
  warehouse = TRANSFORM_WH schedule = '5 minute'
  when system$stream_has_data('raw.customers_stream')
as merge into ... ;
alter task etl.apply_customers resume;
```
`WHEN system$stream_has_data` skips runs (no warehouse resume) when there is nothing new.

## Gotchas
- Stream staleness: if not consumed within the source table's data retention (plus the extension allowed by `MAX_DATA_EXTENSION_TIME_IN_DAYS`, 14 days maximum by default), the stream becomes stale and must be recreated (full reload).
- Two consumers need two streams; one stream's offset is shared.

## Verify
- [ ] Target row counts and a sample of keys match the source after updates and deletes.
- [ ] `show streams` shows `stale = false` and `stale_after` well in the future.

## Checked
2026-10-28. Confirmed against the Snowflake streams introduction (METADATA$ACTION, METADATA$ISUPDATE, METADATA$ROW_ID, updates as DELETE and INSERT pairs, stale_after, extension up to 14 days by default), the MERGE page (ERROR_ON_NONDETERMINISTIC_MERGE default TRUE) and CREATE TASK (a consuming DML advances the offset, SYSTEM$STREAM_HAS_DATA). Removed: the error message text, QUALIFY, the transaction and plain-select offset rules and the CREATE OR REPLACE claim.
Method: documentation only; no commands were run.
