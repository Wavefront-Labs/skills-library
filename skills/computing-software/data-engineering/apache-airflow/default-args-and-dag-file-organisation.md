---
id: computing-software.data-engineering.apache-airflow.default-args-and-dag-file-organisation
name: default-args-and-dag-file-organisation
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dag-default-args, default-args, dag-folder, include-folder, airflowignore, dag-arguments, owner]
level: practitioner
status: docs-checked
description: "Structure an Airflow DAGs repo: default_args vs DAG-level arguments, shared include packages, .airflowignore, tags/owners, and one DAG per file conventions."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#default-arguments
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/modules_management.html
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#airflowignore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# default_args and DAG file organisation

**Goal:** consistent retries/owners/alerts across DAGs, fast parsing, and shared code that imports cleanly on scheduler and workers.

## default_args vs DAG arguments
`default_args` are passed to **every operator** in the DAG (task-level parameters). DAG-level settings go on the DAG itself.
```python
from datetime import timedelta
from pendulum import datetime
from airflow.sdk import dag      # 2.x: from airflow.decorators import dag

DEFAULT_ARGS = {
    "owner": "data-platform",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "execution_timeout": timedelta(hours=1),
    "on_failure_callback": notify_slack,
}

@dag(
    schedule="0 3 * * *",
    start_date=datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    max_active_runs=1,
    tags=["finance", "tier-1"],
    default_args=DEFAULT_ARGS,
    doc_md=__doc__,
)
def finance_daily(): ...
finance_daily()
```
Common mistake: putting `schedule`, `catchup`, `max_active_runs` or `start_date` into `default_args`; keep them on the DAG.

## Repo layout
```
dags/
  finance/
    finance_daily.py
  marketing/
    ...
  .airflowignore
include/            # or plugins/ / a pip-installable package
  common/
    callbacks.py
    sql/
tests/
```
- Import shared code as a package (`from common.callbacks import notify_slack`) with a unique top-level package name and `__init__.py` files (the modules-management page's guidance).
- Better for large teams: ship shared code as a versioned pip package in the image.
- `.airflowignore` excludes `include/`, tests and SQL from DAG parsing; its pattern syntax is set by `[core] dag_ignore_file_syntax` (see the configuration reference).

## Conventions worth enforcing in CI
- One DAG per file; file name = `dag_id`.
- `tags` include domain and tier; `owner` is a team, not a person.
- `doc_md` on every DAG; task `doc_md` for non-obvious steps.
- No top-level DB/API calls (parse-time cost); a DagBag test with import timeout.

## Gotchas
- Mutating a shared `DEFAULT_ARGS` dict in one DAG affects others imported in the same process; copy it (`{**DEFAULT_ARGS, "retries": 0}`).
- Do not use relative imports in DAG files (`from .utils import x`); the modules-management page says to avoid them.

## Verify
- [ ] DagBag import test passes with zero import errors and parse time per file within a budget you choose.
- [ ] All DAGs have owner, tags and retries via a policy check (`airflow_local_settings.dag_policy`) or CI lint.

## Checked

2026-10-28. Confirmed against: core-concepts/dags default_args text, modules_management headings (unique top package name, no relative imports, __init__.py), configuration reference (dag_ignore_file_syntax), cluster policies page (airflow_local_settings.py, dag_policy), airflow.sdk imports. Removed (not confirmable in the fetched pages): default_args precedence claim, sys.path claim, ignore-syntax values, access_control note, 1 s figure.

Method: documentation only; no commands were run.
