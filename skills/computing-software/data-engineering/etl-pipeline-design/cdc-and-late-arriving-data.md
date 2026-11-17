---
id: computing-software.data-engineering.etl-pipeline-design.cdc-and-late-arriving-data
name: cdc-and-late-arriving-data
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, cdc, late-arriving-data, out-of-order-events, late-arriving-dimension, event-time-vs-processing-time, merge-ordering, sequence-number, idempotent-merge, early-arriving-fact]
level: advanced
status: draft
description: "Handle change-data-capture ordering, out-of-order and late-arriving records correctly in ETL pipelines without corrupting slowly-changing state."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://www.kimballgroup.com/2012/05/design-tip-142-building-bridges/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CDC ordering and late-arriving data — the bugs that only show up under load

**Goal:** a batch load or CDC merge that applies changes in the wrong order corrupts state silently (no error, just a wrong "current" value) — this is about preventing that, not just detecting it after the fact.

## 1. Why "arrival order" and "event order" are different, and why the difference matters
CDC events, retried API calls, and multi-partition Kafka topics all can deliver records in an order different from when the underlying change actually happened. A `MERGE` that applies whatever record it sees last as "the current value" is implicitly trusting **arrival order** — correct only when arrival order matches event order, which breaks under retries, replays, multi-threaded producers, or reprocessing a backfill out of chronological order. The fix is always the same shape: carry an explicit **sequence indicator** (a source-system updated_at timestamp, a monotonic LSN/offset, or an explicit version/sequence column) through the pipeline, and make the merge logic compare it, not just overwrite.

## 2. Idempotent, order-safe merge pattern
```sql
MERGE INTO target t
USING staging s ON t.id = s.id
WHEN MATCHED AND s.sequence_num > t.sequence_num THEN UPDATE SET ...
WHEN MATCHED AND s.sequence_num <= t.sequence_num THEN NOTHING  -- stale/duplicate, ignore
WHEN NOT MATCHED THEN INSERT ...
```
This single pattern makes the merge safe to re-run, safe to receive the same record twice, and safe to receive records out of order — a replay of an old event after a newer one already applied is a no-op instead of silently reverting state. Without the `sequence_num` comparison, a `MERGE`'s `WHEN MATCHED THEN UPDATE` blindly overwrites regardless of which record is actually newer — this is the single most common CDC pipeline bug, and it produces no error, just occasionally-wrong "current" values that look like a shrug-worthy data quality blip rather than the systemic ordering bug it is.

## 3. Late-arriving dimension rows ("early-arriving fact")
A fact record referencing a dimension key that hasn't been loaded yet (the dimension's own ETL runs later, or the source systems are out of sync) is the classic **early-arriving fact / late-arriving dimension** problem. Options, in order of general preference: (a) insert a placeholder/"unknown member" dimension row with the business key and minimal attributes, then update it with full attributes once the real dimension row arrives (requires a later reconciliation step — track which fact rows pointed at placeholders); (b) defer loading the fact row until its dimension key resolves (adds latency, risks losing/delaying the fact if the dimension never arrives due to upstream deletion); (c) for SCD Type 2 dimensions specifically, inserting a dimension row with an effective-date range means late facts can correctly attribute to the dimension state *as it was* at the fact's event time rather than the dimension's current state — getting this right is what makes historical reporting accurate, getting it wrong (always joining to current dimension state) silently rewrites history every time a dimension attribute changes.

## 4. Watermarking a backfill or reprocessing run
Replaying old data (backfill, reprocessing after a bug fix) interacts badly with sequence-based merge logic if the backfill's sequence numbers/timestamps are lower than what's already in the target — the merge pattern in section 2 handles this correctly automatically (stale records are no-ops), but **only if every write path uses the same merge logic**. A direct `INSERT`/append-only write path that bypasses the sequence-aware merge (common for "just backfill this one table quickly") reintroduces the exact bug the merge pattern was built to prevent — audit every write path to a CDC-fed table, not just the primary scheduled one.

## Verify
- [ ] Every write path to a CDC-target table (scheduled job, manual backfill, ad hoc fix script) goes through the same sequence-aware merge logic — none bypass it with a raw INSERT/UPDATE.
- [ ] Deliberately replaying an old CDC event after a newer one already applied leaves the target unchanged (tested, not assumed).
- [ ] Early-arriving facts have a defined, tested resolution path (placeholder dimension row or deferred load) rather than silently dropping or erroring.
- [ ] Historical reports joining facts to SCD Type 2 dimensions use the dimension state valid at the fact's event time, not the dimension's current state.
