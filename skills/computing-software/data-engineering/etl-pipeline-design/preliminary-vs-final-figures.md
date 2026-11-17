---
id: computing-software.data-engineering.etl-pipeline-design.preliminary-vs-final-figures
name: preliminary-vs-final-figures
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, preliminary-figures, data-finality, restatements, reporting-periods]
level: advanced
status: draft
description: "Publish preliminary figures that later become final: flagging data maturity, cut-off rules, versioned snapshots of reported numbers, and communicating revisions."
sources:
  - https://www.bls.gov/bls/revisions-schedule.htm
  - https://docs.getdbt.com/docs/build/snapshots
  - https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/accumulating-snapshot-fact-table/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Preliminary vs final figures

**Goal:** consumers get early numbers fast, know they may change, and can always see what was reported when.

## Define maturity
- **Preliminary**: period still open; late data and corrections expected (e.g. first 3 days after day end; ad networks restating spend for 7 days).
- **Final**: after a cut-off, or after an explicit close (finance month-end close). Later changes go through a restatement process.
Base the cut-off on measured lateness/correction distributions, not guesswork.

## Model it
```sql
select event_date, revenue,
       case when event_date >= current_date - 3 then 'preliminary' else 'final' end as data_status
from agg_revenue_daily;
```
- Expose `data_status` (or `is_final`) in marts and dashboards; style preliminary values differently (dashed lines, asterisks).
- For hard closes, store close dates in a control table (`period_close(period, closed_at)`) and derive status from it.

## Keep what was reported
- Snapshot published figures per run (`reported_at`) into an append-only table, or use warehouse time travel/dbt snapshots on the aggregate.
- Revisions report: difference between first-reported and final value per period. Large revisions point to pipeline lateness problems.

## After final
- Freeze: pipelines skip reprocessing final periods automatically (partition filter on status).
- Corrections: explicit restatement run with approval, versioned output and a note to consumers.

## Gotchas
- Silent changes to "final" numbers destroy trust faster than late numbers.
- Different consumers may need different cut-offs (ops wants live, finance wants closed): expose both, labelled.

## Verify
Dashboard shows the status flag; the revisions table records preliminary vs final values for last month.
