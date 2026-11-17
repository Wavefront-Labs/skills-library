---
id: computing-software.data-engineering.apache-airflow.setup-and-teardown-tasks
name: setup-and-teardown-tasks
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dag, setup-teardown, as-teardown, ephemeral-cluster, resource-cleanup, on-failure-fail-dagrun, trigger-rules]
level: advanced
status: docs-checked
description: "Create and always clean up resources in Airflow with setup/teardown tasks (2.7+): @setup/@teardown, as_teardown(setups=...), scoping, and how they affect DAG run state."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/howto/setup-and-teardown.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dags.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dag-run.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setup and teardown tasks

**Goal:** spin up a temporary resource (cluster, temp table, sandbox schema), use it, and tear it down even when work fails, without hiding the failure.

## Pattern
```python
from airflow.sdk import dag, task, setup, teardown

@dag(schedule="@daily", catchup=False)
def nightly_spark():
    @setup
    def create_cluster(): return start_emr_cluster()           # returns cluster id

    @task
    def run_job(cluster_id): submit_step(cluster_id, "s3://jobs/agg.py")

    @teardown
    def delete_cluster(cluster_id): terminate(cluster_id)

    c = create_cluster()
    run_job(c) >> delete_cluster(c)
nightly_spark()
```
Classic operators: `create >> work >> delete.as_teardown(setups=create)`.

## Semantics
- A teardown uses the non-configurable trigger rule `all_done_setup_success`: once all upstreams are done and at least one directly connected setup succeeded, it runs, whether or not the work tasks failed.
- If all of a teardown's setups were skipped or failed, those states propagate to the teardown.
- **Teardown failures are ignored for DAG run state by default**: the run's state reflects the work tasks. Pass `on_failure_fail_dagrun=True` when setting the teardown (for example `delete.as_teardown(setups=create, on_failure_fail_dagrun=True)`) if a failed cleanup must fail the run.
- Clearing a task also clears its setups and teardowns, so re-running recreates the resource.
- Tasks in the scope of a setup have an implicit `all_success` constraint on that setup.

## Versus all_done cleanup
A plain `trigger_rule="all_done"` cleanup task has a known problem: if it is a leaf and succeeds, the DAG run is marked success even when work failed. Teardowns are ignored for DAG run state by default, so the run reflects the work tasks.

## Gotchas
- Keep the setup idempotent (reuse an existing cluster on retry instead of creating a second one).
- Pass identifiers via XCom (return values) so the teardown deletes exactly what was created.

## Verify
- [ ] Force `run_job` to fail: cluster is deleted, DAG run is failed.
- [ ] Clear `run_job` and rerun: a new cluster is created and deleted.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the `all_done_setup_success` rule and state propagation, teardowns ignored for DAG run state by default, `on_failure_fail_dagrun=True` with `as_teardown(setups=...)`, and that clearing a task clears its setups and teardowns. Removed the 2.7 version claim and the retry and cost-alert advice, which are not in the docs.

Method: documentation only; no commands were run.
