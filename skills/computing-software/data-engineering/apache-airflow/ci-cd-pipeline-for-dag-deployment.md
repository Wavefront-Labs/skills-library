---
id: computing-software.data-engineering.apache-airflow.ci-cd-pipeline-for-dag-deployment
name: ci-cd-pipeline-for-dag-deployment
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, dag-deployment-pipeline, ci-cd, dag-integrity, ruff-air-rules]
level: advanced
status: docs-checked
description: "Build a CI/CD pipeline for Airflow DAGs: lint (ruff AIR rules), import and policy tests, image vs Dag bundle delivery, and promotion through environments."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/dag-bundles.html
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/production-deployment.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD pipeline for DAG deployment

**Goal:** every DAG change is linted, import-tested and delivered to each environment the same way, with a rollback.

## CI stages (on every PR)
1. **Lint**: `ruff check dags/ --select AIR3` (the Airflow best-practices page shows this for Airflow 3 migration findings such as AIR301 and AIR302) plus your normal ruff config.
2. **Import test** in the same image as production, following the Airflow unit-test example:
```python
import pytest
from airflow.dag_processing.dagbag import DagBag

@pytest.fixture()
def dagbag():
    return DagBag()

def test_no_import_errors(dagbag):
    assert dagbag.import_errors == {}
```
3. **Policy tests**: your own rules (owner/tags, retries, explicit `schedule` and `catchup`) and a parse-time check; the best-practices page shows timing a Dag file with `time python <dag file>`.
4. **Unit tests** for custom operators/hooks; `dag.test()` runs a simulated execution of a Dag, usable as a smoke test.

## Delivery options
| Method | How | Rollback |
|---|---|---|
| Bake into image | `COPY dags/` in Dockerfile, deploy image tag | redeploy previous tag |
| DAG bundles (Airflow 3, `GitDagBundle`) | `GitDagBundle` supports versioning: each Dag run records the Git commit, so reruns use the same code | revert commit |
Airflow's production-deployment page recommends the Dag Bundle mechanism (including `GitDagBundle`). Other delivery methods (git-sync, object-storage sync) are described in the Helm chart and managed-service docs, which this skill does not cover.

## Promotion
Branch or tag per environment (dev -> staging -> prod), same artifact promoted. Environment differences come from Variables/Connections/secrets backend, not code forks.

## Gotchas
- Testing in a different Python/provider set than production hides import errors: run CI inside the production image.
- Parse-time network calls (Variables at top level) make CI flaky and parsing slow; the import test should run with no network.

## Verify
A PR with a broken import fails CI; after merge, the new DAG version appears in each environment with no import errors.

## Checked
2026-11-01. Confirmed in the Apache Airflow repo docs (best-practices, dag-bundles, production-deployment): DagBag unit-test pattern and import path, `ruff check dags/ --select AIR3` with AIR301/AIR302 examples, `time python` parse timing, `dag.test()`, `GitDagBundle` versioning and the bundle recommendation. Removed: Helm `dags.gitSync` and `aws s3 sync` rows, `airflow dags delete` gotcha, and the `retries >= 1` rule presented as a requirement.
Method: documentation only; no commands were run.
