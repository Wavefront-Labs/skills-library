---
id: computing-software.data-engineering.apache-airflow.dag-integrity-tests
name: dag-integrity-tests
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dag-testing, airflow-ci, dagbag-test, import-errors, pytest, dag-policy, cycle-detection, parse-time-budget]
level: practitioner
status: docs-checked
description: "Gate Airflow DAG changes in CI: DagBag import-error tests, policy checks (tags, owners, retries, no catchup surprises), parse-time budgets, all in the production image."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-a-dag
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/cluster-policies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAG integrity tests in CI

**Goal:** a DAG that fails to import, has a cycle, or breaks team conventions never reaches the scheduler.

## Run in the same image as production
CI job: `docker run <REGISTRY>/airflow:<tag> pytest tests/dags` with the DAG folder mounted. Import errors are usually missing packages or provider version differences, which only the real image reveals.

## Tests
```python
# tests/dags/test_integrity.py
import pytest
from airflow.models import DagBag

@pytest.fixture(scope="session")
def dagbag():
    return DagBag(dag_folder="dags/")

def test_no_import_errors(dagbag):
    assert dagbag.import_errors == {}, "\n".join(f"{k}: {v}" for k, v in dagbag.import_errors.items())

def test_dags_loaded(dagbag):
    assert len(dagbag.dags) > 0

@pytest.mark.parametrize("dag_id", DagBag(dag_folder="dags/").dag_ids)
def test_conventions(dagbag, dag_id):
    dag = dagbag.get_dag(dag_id)
    assert dag.tags, f"{dag_id} has no tags"
    assert dag.owner != "airflow", f"{dag_id} needs a real owner"
    assert dag.catchup is False or "backfillable" in dag.tags
    for t in dag.tasks:
        assert t.retries >= 1, f"{dag_id}.{t.task_id} has no retries"
```
Cycles raise at load and show up in `import_errors`.

## Parse-time budget
```python
import time, importlib.util, pathlib
PARSE_BUDGET_S = 2.0   # your own budget

def test_parse_time():
    for f in pathlib.Path("dags").rglob("*.py"):
        t0 = time.time()
        spec = importlib.util.spec_from_file_location(f.stem, f); spec.loader.exec_module(importlib.util.module_from_spec(spec))
        assert time.time() - t0 < PARSE_BUDGET_S, f"{f} parses slowly: top-level code?"
```
Or in the image: `airflow dags report` lists duration per file.

## Enforce at runtime too: cluster policies
`airflow_local_settings.py` with `dag_policy(dag)` / `task_policy(task)` (see the cluster policies page) can reject or mutate DAGs on every scheduler, not just in CI.

## Lint
The best-practices page has a "Code Quality and Linting" section on installing and using `ruff` for Airflow rules.

## Verify
- [ ] CI fails on a PR that introduces an import error (try a bad import).
- [ ] The UI "DAG Import Errors" banner is empty in production.

## Checked

2026-10-28. Confirmed against: best-practices page (testing a DAG with DagBag and import_errors, dags report, ruff linting section), cluster policies page (airflow_local_settings.py, dag_policy, task_policy), CLI reference (airflow dags report). Removed (not confirmable in the fetched pages): include_examples argument, AIR rule IDs, forbid-pool example.

Method: documentation only; no commands were run.
