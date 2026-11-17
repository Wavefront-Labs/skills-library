---
id: computing-software.data-engineering.etl-pipeline-design.source-system-discovery-and-profiling
name: source-system-discovery-and-profiling
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, source-discovery, data-profiling, source-analysis, requirements]
level: practitioner
status: draft
description: "Discover and profile a new source system before building a pipeline: ownership, change patterns, keys, volumes, data quality, access limits and a source analysis document."
sources:
  - https://www.dama.org/cpages/body-of-knowledge
  - https://books.google.com/books?vid=ISBN9781098108304
  - https://docs.profiling.ydata.ai/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Source system discovery and profiling

**Goal:** know a source well enough to choose the extraction method and model it correctly, before writing pipeline code.

## Questions for the source owner
- What is the system of record for each entity? Who owns it, and who approves access?
- How do records change: inserts only, updates in place, hard deletes, soft deletes? Is there a reliable `updated_at`? Is CDC/log access possible?
- Volumes (rows/day, total), peak hours, maintenance windows, rate limits, read replicas.
- Planned changes (migrations, upgrades) and how schema changes are communicated.
- Known data quality issues and business rules hidden in application code.

## Profile the data
```sql
select count(*) rows, count(distinct id) distinct_ids,
       sum(case when updated_at is null then 1 else 0 end) null_updated,
       min(created_at), max(created_at), max(updated_at)
from src.orders;
select status, count(*) from src.orders group by 1 order by 2 desc;
```
Or `ydata-profiling` / dbt `codegen` + `dbt_profiler` on a sample. Check:
- Candidate keys actually unique; composite keys.
- Null rates, distinct counts, value distributions, outliers.
- Timestamp time zones and precision; whether `updated_at` changes on every update (test by updating a row in a test env).
- Orphan foreign keys; encoding/odd characters.

## Write a source analysis doc
Entities and grain, keys, change capture method chosen and why, volumes, freshness need, PII columns, known issues, contacts. Keep it next to the pipeline code.

## Gotchas
- Trusting `updated_at` without testing: many apps do not update it on bulk/admin changes.
- Profiling production at peak time: use replicas or off-hours.

## Verify
Every design decision (incremental column, key, delete handling) cites a profiling result in the doc.
