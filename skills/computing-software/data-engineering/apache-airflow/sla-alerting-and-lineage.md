---
id: computing-software.data-engineering.apache-airflow.sla-alerting-and-lineage
name: sla-alerting-and-lineage
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, sla, sla-miss, on-failure-callback, alerting, openlineage, data-lineage, anomaly-detection, slack-alert, pagerduty, observability, dag-monitoring, airflow-3, deadline-alerts]
level: practitioner
status: gated
description: "Catch and alert on late, failed or silently-wrong Airflow DAG runs before the business notices: SLAs, callbacks, OpenLineage."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html
  - https://openlineage.io/docs/integrations/airflow/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Catching DAG failures before the business does

**Goal:** know a pipeline is late, failed, or produced garbage before a stakeholder opens a stale dashboard.

## 1. Airflow's `sla` kwarg is a trap — avoid it
The legacy per-task `sla=timedelta(...)` only fires if the task is actually scheduled and running; it does nothing for a DAG that never starts (upstream outage, scheduler backlog), and it was deprecated/removed across Airflow 2.x→3.x minor versions — behaviour differs by version, verify on yours. Don't rely on it for anything you care about. (gated: unconfirmed, source is paywalled or blocked)

## 2. Build alerting from callbacks, not SLAs
Use `on_failure_callback` / `on_success_callback` at the `default_args` or DAG level, and `sla_miss_callback` only if you've confirmed it fires in your version. A reusable callback posts to Slack/PagerDuty with dag_id, task_id, try_number, log_url, and the exception. For "this DAG didn't even start" alerting, use a separate watchdog DAG that queries the metadata DB / REST API for the latest successful `DagRun` per `dag_id` and pages if it's older than the expected cadence — this is the only reliable way to catch a DAG that's stuck behind a scheduler stall or a paused flag someone forgot to unset.
- **Deadline alerts (Airflow 3+):** newer Airflow versions added first-class `DeadlineAlert` on DAGs (fires relative to a reference like logical date + offset) — check your version's docs before building a custom watchdog; it may already exist.

## 3. Fatigue is the real failure mode
A DAG that pages on every retry trains people to ignore the channel. Alert only on final failure (after retries exhaust), route by severity (a dev DAG's failure is not a 2am page), and alert once per run, not once per task — aggregate task failures into one DAG-level message with a `trigger_rule="all_done"` summary task at the end of the DAG that checks `dag_run.get_task_instances()` for failures and sends a single alert.

## 4. "It ran green but the data is wrong" — silent failures
A DAG can succeed while loading zero rows, stale data, or duplicate rows. Green ≠ correct. Add an explicit row-count / freshness assertion task after the load (see computing-software.data-engineering.data-quality.data-tests-and-freshness-slas) that fails the DAG run if the check fails — don't rely on a separate DQ tool running on a different schedule to catch it hours later.

## 5. Lineage: OpenLineage integration
Airflow ships an OpenLineage provider (`apache-airflow-providers-openlineage`) that emits START/COMPLETE/FAIL events per task run with input/output datasets, automatically for many operators (SQL, Spark submit) and via extractors for custom ones. Point `OPENLINEAGE_URL` at Marquez, DataHub, or another consumer. This gives you: which downstream tables/dashboards break when an upstream DAG fails, and column-level lineage for impact analysis — invaluable when triaging "why is this number wrong" without manually tracing DAG dependencies.
- **Gotcha:** lineage from custom `PythonOperator` tasks needs a manual `OpenLineage` extractor or explicit `inlets`/`outlets` — it is not automatic for arbitrary Python.

## 6. Minimum viable observability stack
At minimum: (1) failure callback → chat/pager, (2) a watchdog for "didn't run at all", (3) one freshness/row-count assertion per critical DAG, (4) lineage emission if you have >5 interdependent DAGs so you can answer "what breaks if X fails" without guessing.

## Verify
- [ ] Killing the scheduler for an hour triggers a watchdog alert, not silence.
- [ ] A task that fails on try 1 of 3 does not page; failure after try 3 does.
- [ ] A DAG that "succeeds" but loads 0 rows fails its own run (via an assertion task).
- [ ] `OPENLINEAGE_URL` is set and a test DAG run shows up in the lineage backend with correct input/output datasets.
- [ ] Alert channel has had zero false-positive pages in the last week (tune thresholds if not).

## Checked

2026-11-02

- Confirmed: Airflow Dags concept page (trigger_rule values including all_done) and the Airflow Dags page were fetched.
- Removed or gated: SLA removal across versions, callback names (on_failure_callback, sla_miss_callback) and the OpenLineage provider/env vars are not stated on the fetched pages (the OpenLineage page is a stub); gated, confirm in the Airflow and OpenLineage docs for your version.

Method: documentation only; no commands were run.
