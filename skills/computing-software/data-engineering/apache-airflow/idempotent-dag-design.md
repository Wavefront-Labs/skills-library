---
id: computing-software.data-engineering.apache-airflow.idempotent-dag-design
name: idempotent-dag-design
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dag, idempotency, data-interval, data-interval-start, logical-date, execution-date, catchup, backfill, retries, max-active-runs, sensors, deferrable-operators, reschedule-mode, taskflow-api, jinja-templating, airflow-3, airflow-2, orchestration, scheduler, mwaa, cloud-composer, astronomer]
level: practitioner
status: docs-checked
description: "Write Airflow DAGs that are safe to retry, backfill and re-run: data-interval templating, catchup, retries, concurrency limits, deferrable sensors and Airflow 2 vs 3 changes."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html
  - https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/sensors.html
  - https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html
  - https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Idempotent Airflow DAG design — every run can be re-run

**Goal:** a DAG run for interval X produces the same result whether it runs once, is retried, is cleared and re-run, or is backfilled a year later.

## 1. Bind every task to its data interval, never to "now"
Each scheduled run covers `[data_interval_start, data_interval_end)`. Use those, not `datetime.now()`:
```python
from airflow.decorators import dag, task   # Airflow 3: import from airflow.sdk instead
import pendulum

@dag(schedule="@daily", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
     catchup=False, max_active_runs=1,
     default_args={"retries": 3, "retry_delay": pendulum.duration(minutes=5)})
def orders_daily():
    @task
    def load(data_interval_start=None, data_interval_end=None):
        run_sql("""DELETE FROM mart.orders WHERE order_date >= %s AND order_date < %s;
                   INSERT INTO mart.orders SELECT ... WHERE order_date >= %s AND order_date < %s""",
                (data_interval_start, data_interval_end) * 2)
    load()
orders_daily()
```
In templated operator fields use `{{ data_interval_start }}`, `{{ data_interval_end }}`, `{{ ds }}` (date string of the logical date).
- **Gotcha:** a daily run for 2026-03-01 *starts after* that day ends (on 03-02). The logical date is the interval start, not the time it ran.

## 2. Make the write idempotent
Pick one pattern per task:
- **Delete-then-insert / partition overwrite** for the interval (above), in one transaction.
- **MERGE/upsert** on a natural key.
- **Write to a path keyed by interval** (`s3://.../dt={{ ds }}/`) and overwrite it.
Never plain `INSERT` or append without a key — retries duplicate rows. See computing-software.data-engineering.etl-pipeline-design.idempotent-incremental-loads.

## 3. Catchup, backfill, concurrency
- `catchup=True` creates a run for every missed interval since `start_date`. The scheduler-wide default comes from `[scheduler] catchup_by_default`; set `catchup` explicitly on every DAG.
- Backfill: `airflow backfill create --dag-id <DAG_ID> --from-date <FROM_DATE> --to-date <TO_DATE>`; add `--dry-run` first (see the CLI reference).
- `max_active_runs=1` when runs must be sequential (e.g. each depends on the previous state); otherwise let backfills parallelise. `depends_on_past=True` makes a task wait for its previous run's success.
- `airflow backfill create` also accepts `--max-active-runs` to limit how many backfill runs execute at once.

## 4. Retries that are actually safe
- Set `retries` and a retry delay for flaky network calls.
- Retrying is only safe if section 2 holds. Non-idempotent side effects (emails, API POSTs, payments) need a dedupe key or a separate, non-retried task.
- Set `execution_timeout` on every task so a hung task fails instead of holding a slot forever. With deferrable operators it counts total runtime, including time spent deferred.

## 5. Sensors and waiting
- Default `mode="poke"` holds a worker slot the whole time. Use `mode="reschedule"` for waits over a few minutes, or better, **deferrable** operators/sensors (`deferrable=True` on many provider sensors), which hand the wait to the triggerer process — requires a running `airflow triggerer`.
- Always set `timeout` (sensor default is 7 days) and `poke_interval`.
- Prefer data-aware scheduling (Assets) over sensors when both DAGs are yours.

## 6. Keep DAG files cheap to parse
The scheduler re-parses DAG files repeatedly (no more often than every `min_file_process_interval` seconds). No top-level DB queries, API calls, `Variable.get()` or heavy imports at module level — put them inside tasks or use Jinja `{{ var.value.x }}`. Pass small values via XCom only; large data goes to storage, with the path in XCom.

## 7. Airflow 2 → 3 gotchas
- Asset-triggered Dags have no logical date, so `logical_date` and `ds`-style variables are unavailable there; check the templates reference for what your version provides.
- The DAG-run page says to use the logical date explicitly instead of assuming it matches `data_interval_start` or `data_interval_end`.

## Verify
- [ ] Clearing and re-running a completed run leaves row counts in the target unchanged.
- [ ] No `now()`/`today()` calls in task logic; all ranges come from `data_interval_*`.
- [ ] `catchup` and a static `start_date` are set explicitly on every DAG.
- [ ] Importing the DAG file is fast and makes no network calls.
- [ ] Long waits use deferrable or `reschedule` sensors with a `timeout`.
- [ ] A 3-day backfill runs without exhausting the source pool.

## Checked
2026-10-28. Confirmed on the Airflow stable docs (best practices, DAG runs, templates reference, deferring, sensors, CLI reference, configuration reference): `airflow backfill create` with `--dag-id`, `--from-date`, `--dry-run`, `--max-active-runs`; `catchup_by_default` setting; `depends_on_past`; sensor default timeout of 7 days; `poke_interval`; `min_file_process_interval` and the top-level-code warning; deferrable sensors versus `mode="reschedule"` and the triggerer; `execution_timeout` counting deferred time; XCom for small messages with large data in remote storage; use of `logical_date` rather than assuming it equals the data interval; Asset-triggered Dags having no logical date; `from airflow.sdk import DAG`.
Removed as unconfirmed: the `~30 s` default parse interval, the static `start_date` rule, `pools` and `max_active_tasks` advice, the `execution_date` and `*_ds` deprecation claim, the exact Airflow 3 import path for the `dag` and `task` decorators.
Method: documentation only; no commands were run.
