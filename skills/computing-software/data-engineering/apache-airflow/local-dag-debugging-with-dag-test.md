---
id: computing-software.data-engineering.apache-airflow.local-dag-debugging-with-dag-test
name: local-dag-debugging-with-dag-test
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dag-testing, dag-test-method, airflow-dags-test, airflow-tasks-test, local-debugging, ide-debugger, airflow-standalone, breeze]
level: practitioner
status: docs-checked
description: "Debug Airflow DAGs locally: dag.test() in one process with an IDE debugger, airflow dags test / tasks test CLIs, test connections via env vars, and airflow standalone."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/debug.html
  - https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local DAG debugging with dag.test()

**Goal:** run a whole DAG or a single task on your machine with breakpoints, without a scheduler or workers.

## dag.test()
```python
# at the bottom of the DAG file
if __name__ == "__main__":
    dag_obj = load_orders()           # the @dag-decorated call result
    dag_obj.test()                    # see the best-practices page for the available arguments
```
`python dags/load_orders.py` runs the DAG in one process: set breakpoints in your IDE, step into operators. `dag.test(use_executor=True)` runs the workloads through the configured executor instead.

## CLI equivalents
```bash
airflow dags test load_orders 2026-10-15                 # full run, no scheduler; writes to metadata DB
airflow tasks test load_orders transform 2026-10-15      # one task, ignores dependencies, no state recorded
airflow tasks render load_orders transform 2026-10-15    # show templated fields
```
`tasks test` is the quickest loop for a single operator or SQL template.

## Connections and variables without a DB
```bash
export AIRFLOW_CONN_WAREHOUSE='postgresql://user:pass@localhost:5432/dw'
export AIRFLOW_VAR_ENV=dev
```
Use `AIRFLOW_CONN_{CONN_ID}` and `AIRFLOW_VAR_{KEY}` for connections and variables.

## A local full stack when needed
- `airflow standalone`: runs an all-in-one copy of Airflow (dev only).
- Docker Compose from the official docs.

## Tips
- Point local runs at dev/sandbox resources; `dag.test` really executes tasks.
- Use small date ranges and run-configuration flags to limit data volume.
- Reproduce a production failure by running the same logical date with the production image locally.

## Verify
- [ ] `python dags/<file>.py` runs the DAG end to end against dev resources.
- [ ] A breakpoint in a TaskFlow function is hit in the IDE.

## Checked

2026-10-28. Confirmed against: best-practices page (dag.test, use_executor, AIRFLOW_VAR_/AIRFLOW_CONN_), CLI reference (airflow dags test, tasks test, tasks render, standalone). Removed (not confirmable in the fetched pages): dag.test keyword arguments, version gates, AWS JSON connection example, Astro CLI and Breeze mentions, precedence claim.

Method: documentation only; no commands were run.
