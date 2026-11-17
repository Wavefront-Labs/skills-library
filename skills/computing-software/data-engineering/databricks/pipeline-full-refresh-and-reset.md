---
id: computing-software.data-engineering.databricks.pipeline-full-refresh-and-reset
name: pipeline-full-refresh-and-reset
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, dlt, dlt-full-refresh, refresh-selection, reset-allowed, streaming-tables, checkpoint-reset, lakeflow-declarative-pipelines]
level: practitioner
status: docs-checked
description: "Run full and selective refreshes of Lakeflow declarative pipeline (DLT) tables, protect streaming tables with pipelines.reset.allowed, and recover from incompatible changes."
sources:
  - https://docs.databricks.com/en/dlt/updates.html
  - https://docs.databricks.com/en/dlt/properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full refresh and reset of pipeline tables

**Goal:** rebuild exactly the tables that need it after a logic change, without wiping streaming history that cannot be re-read from source.

## Update types
| Update | Materialized views | Streaming tables |
|---|---|---|
| Normal (refresh) | recompute (incrementally when possible) | process new data only |
| Selective refresh | listed tables refreshed | listed tables process new data |
| Full refresh all | recompute | **truncate and reprocess all source data from the beginning**, checkpoints reset |
| Selective full refresh | listed tables recomputed | listed tables truncated and reprocessed |

UI: select tables in the pipeline graph and use "Refresh selection", with the option to fully refresh the selected tables. The Pipelines REST API can also start an update for selected tables and clear the checkpoints of selected flows; take the exact request fields from the Pipelines API reference.

## Protect streaming tables
Bronze streaming tables reading Kafka/Auto Loader with limited source retention cannot be rebuilt by reprocessing. Block resets:
```python
@dlt.table(table_properties={"pipelines.reset.allowed": "false"})
def bronze_events(): ...
```
```sql
CREATE OR REFRESH STREAMING TABLE bronze_events
TBLPROPERTIES ('pipelines.reset.allowed' = 'false') AS SELECT ...;
```
With the property set to false, full refreshes are not run on that table or view.

## When you need a full refresh
- Changed streaming query logic must apply to historical rows (new column derivation, fixed parsing).
- Incompatible changes to a streaming query (for example a changed source or stateful operator): a full refresh clears the flow checkpoints and reprocesses the source.
- Schema changes not handled by evolution (type narrowing).

## Alternatives to avoid full refresh
- Materialized views recompute anyway; changes there need only a normal update.
- For streaming tables, use an append flow to add data to an existing streaming table without requiring a full refresh.

## Gotchas
- Truncation happens at start: consumers see empty/partial tables during the rebuild. For critical gold tables, build into a new pipeline/table and swap views.
- APPLY CHANGES (AUTO CDC) targets: full refresh replays the whole CDC feed; source must retain it.

## Verify
- [ ] Bronze streaming tables carry `pipelines.reset.allowed=false`; a test full refresh leaves their row counts intact.
- [ ] Only the intended tables were selected for the full refresh.

## Checked

- 2026-10-28: confirmed on the pipeline updates page (refresh semantics table, full refresh clears streaming table data and flow checkpoints, can drop records when source data is gone, `pipelines.reset.allowed` blocks full refresh, selective refresh, append flows) and the pipeline properties page (`pipelines.reset.allowed`).
- Removed: CLI flags, the `full_refresh: true` task setting, the error message string, `INSERT INTO ONCE`/DML advice and the continuous-pipeline claim (not found in the fetched pages).

Method: documentation only; no commands were run.
