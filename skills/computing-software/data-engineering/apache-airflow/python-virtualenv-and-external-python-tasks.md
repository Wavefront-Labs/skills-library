---
id: computing-software.data-engineering.apache-airflow.python-virtualenv-and-external-python-tasks
name: python-virtualenv-and-external-python-tasks
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, pythonvirtualenvoperator, externalpythonoperator, task-virtualenv, task-external-python, bashoperator, dependency-isolation]
level: practitioner
status: docs-checked
description: "Isolate conflicting Python dependencies in Airflow tasks with @task.virtualenv, @task.external_python, @task.docker or KubernetesPodOperator, and pick the right core operator."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#handling-conflicting-complex-python-dependencies
  - https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/operators/python.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtualenv and external-Python tasks

**Goal:** run a task that needs library versions incompatible with the Airflow environment, without breaking the scheduler or other DAGs.

## Options, cheapest to most isolated
| Approach | Startup cost | Isolation | When |
|---|---|---|---|
| `@task` (PythonOperator) | none | shares Airflow's env | deps already in image |
| `@task.virtualenv` | creates a venv per run (cache with `venv_cache_path`) | Python packages | small, occasional extra deps |
| `@task.external_python(python=...)` | none | pre-built venv on workers | stable conflicting deps, fast |
| `@task.docker` / `@task.kubernetes` / KubernetesPodOperator | container start | full OS | heavy/native deps, other languages |
| BashOperator | none | process | command-line tools |

## Examples
```python
from airflow.sdk import dag, task   # Airflow 3; in 2.x: from airflow.decorators import dag, task

@task.virtualenv(requirements=["pandas<2", "pyarrow"], system_site_packages=False,
                 venv_cache_path="/tmp/venv-cache")
def legacy_transform(path: str) -> int:
    import pandas as pd                 # imports MUST be inside the function
    return len(pd.read_parquet(path))

@task.external_python(python="/opt/venvs/ml/bin/python")
def score(batch_id: str):
    import sklearn
    ...

```

## Rules for isolated Python tasks
- The function is serialized as source and run in another interpreter: no closures over module-level variables, all imports inside.
- Arguments and return values pass through serialization (pickle, cloudpickle or dill; see the provider docs), so keep them simple (paths, ids). Return small values; they become XComs.
- Airflow context is limited in isolated tasks; prefer passing values such as `ds` explicitly via templates (see the provider docs for what is available).
- Build external venvs in the worker image (Dockerfile), not at runtime.

## Gotchas
- `@task.virtualenv` without a cache rebuilds the venv every run: minutes of pip per task and PyPI dependency at runtime.
- `system_site_packages=True` can leak Airflow's package versions into the venv; set it to False for real isolation.
- Python version of the venv for `external_python` must be one cloudpickle/pickle can bridge (same major.minor safest).
- For Airflow 3, these operators live in the `apache-airflow-providers-standard` package.

## Verify
- [ ] Task log shows the venv interpreter path and expected package versions (`pip freeze` step or logged `__version__`).
- [ ] DAG file parses in the scheduler without the isolated deps installed (no top-level imports of them).

## Checked

2026-10-28. Confirmed against: best-practices page (conflicting dependencies, @task.docker/@task.kubernetes), standard provider python operator page (venv_cache_path, system_site_packages, cloudpickle/dill, @task.external_python(python=...)), Airflow 3 upgrade guide (apache-airflow-providers-standard). Removed (not confirmable in the fetched pages): @task.bash example, serializer option values, context-availability rules, system_site_packages default, pinned pandas/pyarrow versions.

Method: documentation only; no commands were run.
