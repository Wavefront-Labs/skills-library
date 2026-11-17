---
id: computing-software.data-engineering.etl-pipeline-design.batch-completeness-checks
name: batch-completeness-checks
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, late-arriving-data, batch-completeness-check, control-totals, readiness-markers, publish-gate, expected-files]
level: practitioner
status: docs-checked
description: "Decide when a batch period is complete enough to publish: markers, expected files, control totals, volume baselines, watermarks, and gating publishes."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html
  - https://docs.getdbt.com/docs/deploy/source-freshness
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch completeness checks

**Goal:** daily reports are computed on a complete day of data, not whatever had arrived when the schedule fired.

## Completeness signals (combine at least two)
1. **Explicit markers:** source writes `_SUCCESS`/`done.flag` or a manifest listing files and row counts. Strongest signal; ask source teams for it.
2. **Expected inventory:** a calendar of expected deliveries (e.g. 24 hourly files, 40 store files). Check all arrived.
3. **Control totals:** source provides counts/sums per period (header/trailer records, API totals); compare after load.
4. **Source watermark:** max event time loaded is past the period end + allowed lateness; or CDC source LSN/commit time is past period end.
5. **Volume baseline:** row count within expected range vs same weekday history (catches partial loads when nothing else exists).

## Implementation sketch (warehouse)
```sql
-- completeness table filled by checks
insert into ops.period_completeness (dataset, period, check_name, passed, detail, checked_at)
select 'orders', date '2026-10-17', 'store_files',
       count(distinct store_id) = (select count(*) from ref.active_stores where open_on = date '2026-10-17'),
       count(distinct store_id)::varchar, current_timestamp
from raw.store_sales_files where business_date = '2026-10-17';
```
Publish step (orchestrator):
In Airflow, a sensor is an operator that waits for something to occur and fails at its `timeout` (so you are alerted) if it does not. `PythonSensor` waits for a Python callable to return true, which fits this check:
```python
PythonSensor(
    task_id="orders_complete",
    python_callable=orders_complete,   # returns True when every check for the period passed
    poke_interval=900,
    timeout=6 * 3600,
    mode="reschedule",
)
```
- `poke_interval` is seconds between checks; `timeout` is the maximum run time, measured from the first execution attempt, not per poke.
- `mode="reschedule"` frees the worker slot between checks (the default `poke` holds a slot for the whole run). Use reschedule for checks every minute or slower.
- `soft_fail=True` marks the sensor SKIPPED instead of FAILED at timeout; leave it off if a missing period must alert.
Downstream marts run after the sensor; the dashboard shows a "data complete through" date from the same table.
- dbt can check source freshness against an SLA (`dbt source freshness`); it is not part of `dbt build`, so run it as the first step of a job to stop models running on stale sources, or as the last step or a separate job otherwise. Run freshness jobs at least twice as often as your tightest SLA (a 1 hour SLA: every 30 minutes).

## Policy when incomplete at deadline
- **Publish provisional** with a flag (`is_final = false`) and recompute when complete (see restatements).
- **Hold** and alert the source owner (financial close, regulatory).
- **Publish partial excluding** the incomplete segment (e.g. missing store) with explicit annotation.
Agree the policy per dataset with consumers in the data contract/SLA.

## Late data after "complete"
Even after passing, late records arrive. Either reopen the period (re-run with lookback and mark restated) or route late records to the next period with an adjustment flag. Track late-arrival rates to tune allowed lateness.

## Gotchas
- A marker written before all files are visible (a producer that does not finish uploads before writing it) -> check manifest contents, not just marker existence.
- Time zones: "day complete" must use the source's business day definition.
- Volume baselines fail on holidays/promotions; use them as warnings, not hard gates, unless calibrated.

## Verify
- [ ] Every published period has completeness evidence recorded.
- [ ] A simulated missing file blocks the publish and alerts.

## Checked
Checked 2026-11-08 against the Airflow Sensors page (poke vs reschedule, `poke_interval`, `timeout`, `soft_fail`, PythonSensor; read in full) and the dbt Source freshness page (not in `dbt build`, job placement, check frequency rule; read in full). Replaced the `@task.sensor` decorator example (not on the page) with `PythonSensor`. The warehouse SQL, completeness signals and publish policies are design advice, not documentation claims; the SQL is illustrative, not run.
Method: documentation only; no commands were run.
