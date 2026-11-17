---
id: computing-software.data-engineering.data-quality.dq-root-cause-analysis
name: dq-root-cause-analysis
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, dq-root-cause, root-cause-analysis, five-whys, lineage-tracing, data-incidents, prevention]
level: practitioner
status: draft
description: "Find the root cause of a data quality issue: scope the impact, trace lineage upstream, bisect by time and segment, diff versions, and fix the cause not the symptom."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://openlineage.io/docs/
  - https://asq.org/quality-resources/root-cause-analysis
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DQ root cause analysis

**Goal:** after "the revenue number is wrong", identify what actually broke, why, and what prevents recurrence, quickly and with evidence.

## 1. Characterise the symptom precisely
- Which metric/table/column, by how much, since when (first bad date), which segments (region, channel, source)?
- Is it wrong values, missing rows, duplicates, or late data?
```sql
select order_date, channel, count(*), sum(amount)
from marts.fct_orders where order_date >= current_date - 14 group by 1, 2 order by 1, 2;
```
A sharp step on one date + one segment points to a deploy or source change; gradual drift points to data/behaviour changes.

## 2. Walk lineage upstream, layer by layer
Use the lineage graph (dbt DAG, catalog, OpenLineage) from the broken asset to sources. At each hop, run the **same diagnostic query** and find the first layer where the anomaly appears.
```
mart (wrong) -> intermediate (wrong) -> staging (ok)  => bug in intermediate logic
mart (wrong) -> ... -> raw (wrong) => source/ingestion problem
```

## 3. Bisect by time and change
- Correlate the first bad date with: code deploys (git log of models/pipelines), schema changes (source DDL, schema drift alerts), ingestion incidents (connector failures, resyncs), upstream app releases, reference data updates.
- Diff outputs before/after a suspect change (data diff of model versions, `dbt build` of the old commit into a scratch schema).

## 4. Common root causes
| Pattern | Typical cause |
|---|---|
| Duplicates after a date | join key no longer unique (new source rows), connector resync, retries without idempotency |
| Missing rows | inner join to a dimension missing new keys, filter on a new status value, partial load not detected |
| Shifted values | timezone change, unit change at source (cents vs dollars), currency logic |
| Nulls in a column | upstream rename (old column now null), schema evolution, parsing failure |
| Gradual drift | business change misinterpreted as data error (verify with domain owner) |

## 5. Five whys to the process cause
"Duplicates in fct_orders" -> "join to dim_customer fanned out" -> "dim_customer had duplicate keys" -> "CRM started emitting merged customers as new rows" -> "no uniqueness test on dim key and no contract with CRM team". Fixes: data fix + test + contract.

## 6. Close the loop
- Correct the data (backfill/restatement) and communicate impact.
- Add the test/monitor that would have caught it earlier.
- Record in the DQ issue log with root cause category (source, ingestion, transformation, reference data, definition), for trend analysis.

## Verify
- [ ] Root cause stated with evidence (query results, commit, change ticket), not assumption.
- [ ] A preventive control was added and fails on the original bad data.
