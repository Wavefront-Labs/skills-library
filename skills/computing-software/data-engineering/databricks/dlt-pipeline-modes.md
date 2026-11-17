---
id: computing-software.data-engineering.databricks.dlt-pipeline-modes
name: dlt-pipeline-modes
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, dlt, delta-live-tables, lakeflow, dlt-pipeline-modes, triggered-pipeline, continuous-pipeline, development-mode, production-mode, full-refresh]
level: practitioner
status: docs-checked
description: "Choose Lakeflow/DLT pipeline execution: triggered vs continuous, update run behavior, trigger intervals and when full refresh is safe."
sources:
  - https://docs.databricks.com/aws/en/dlt/pipeline-mode
  - https://docs.databricks.com/aws/en/dlt/updates
  - https://docs.databricks.com/aws/en/dlt/configure-pipeline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DLT / Lakeflow pipeline modes

**Goal:** pick the execution mode that meets latency at the lowest cost, and develop fast without production behaviour getting in the way.

## 1. Triggered vs continuous
| | Triggered | Continuous |
|---|---|---|
| Behaviour | refreshes all tables from the data available when the update started, then stops | runs until manually stopped, processes data as it arrives |
| Best for freshness of | every 10 minutes, hourly or daily | between every 10 seconds and a few minutes |
| Cost | cluster runs only long enough to update | requires an always-running cluster |
| Set by | Pipeline mode setting (triggered is the default) | Pipeline mode setting, or a continuous job |
Most pipelines should be **triggered on a schedule**; continuous is justified when consumers need freshness in the seconds-to-minutes range.
Databricks recommends running continuous pipelines with a continuous job rather than the pipeline's built-in continuous mode (a continuous job unlocks serverless performance modes such as Standard that built-in continuous mode does not support). When a job orchestrates the pipeline, the job decides the execution mode, so leave the pipeline's own Pipeline mode as triggered.
`pipelines.trigger.interval` controls how often a flow starts an update in continuous pipelines. It is not used for triggered pipelines. Set it on individual tables rather than the whole pipeline, because streaming and batch queries have different defaults.
Standalone materialized views and streaming tables always refresh in triggered mode.

## 2. Update run behavior
There is no separate development or production switch in the current docs; behavior depends on how the update is started.
| | Fast-start, debugging-focused | Automatic retry and restart |
|---|---|---|
| Used for | UI "Run now" and ad-hoc updates of non-continuous pipelines | updates started from Jobs or the Pipelines API, and all continuous pipeline updates |
| Cluster | reused to avoid restarts; by default runs for two hours (`pipelines.clusterShutdown.delay`) | restarted on specific recoverable errors (memory leaks, stale credentials); shuts down right after the run |
| Retries | disabled, so errors show immediately | retried on specific errors such as a failure to start a cluster |
**Schedule production pipelines through a job**, not ad-hoc runs. For a triggered pipeline you can override the default with "Run now with different settings".

## 3. Compute
Databricks recommends developing new pipelines on serverless. Serverless performance modes such as Standard are unlocked when a continuous job runs the pipeline; see the serverless pipeline configuration page for the options in your workspace.

## 4. Updates and refresh
- **Refresh** (default update): processes new records for streaming tables; materialized views refresh incrementally when that is more efficient.
- **Full refresh** clears streaming tables and flow checkpoints and reprocesses all source data. Dangerous when the source no longer holds full history (Kafka short retention, object-storage lifecycle policies, records deleted for compliance): records absent from the source are dropped from the target. Protect such tables with the table property `pipelines.reset.allowed` set to `false`:
```python
@dlt.table(table_properties={"pipelines.reset.allowed": "false"})
def bronze_events(): ...
```
- **Reset streaming flow checkpoints** clears checkpoints but not table data; start it through the REST API updates request with `reset_checkpoint_selection` (fully qualified `catalog.schema.flow_name` values).
- Selective refresh: "Select tables for refresh" or "Refresh failed tables" in the UI; the API accepts `refresh_selection` and `full_refresh_selection`.
- **Dry run** (Public Preview) checks the pipeline source for errors without materializing or publishing any datasets; use it while developing and testing.

## Verify
- [ ] Scheduled pipelines are run by a job, not ad-hoc.
- [ ] Continuous mode is used only where a freshness SLA requires it.
- [ ] Tables whose sources can't be replayed have `pipelines.reset.allowed` set to false.
- [ ] A dry run is part of the pre-deploy routine.

## Checked

2026-11-09: reviewed against the Databricks documentation fetched this batch.

Confirmed: triggered versus continuous definitions and freshness guidance, the continuous-job recommendation and job precedence, `pipelines.trigger.interval` guidance, fast-start versus automatic-retry run behavior and the two-hour default, refresh and full refresh semantics, Kafka/object storage/compliance full-refresh outcomes, `pipelines.reset.allowed`, selective refresh, `reset_checkpoint_selection`, dry run, and the serverless recommendation (pipeline mode, updates and configure pipelines pages).

Removed or corrected: the development versus production mode table and `development: true|false` (the updates page now describes run behavior by trigger), the `continuous: true` and `autoscale.mode: ENHANCED` settings, the `validate_only` CI claim (replaced by dry run), and `planning_information`.

Method: documentation only; no commands were run.
