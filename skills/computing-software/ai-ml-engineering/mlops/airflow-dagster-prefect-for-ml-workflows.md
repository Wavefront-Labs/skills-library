---
id: computing-software.ai-ml-engineering.mlops.airflow-dagster-prefect-for-ml-workflows
name: airflow-dagster-prefect-for-ml-workflows
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, pipeline-orchestration, airflow-ml, dagster, prefect, kubernetespodoperator, asset-orchestration, ml-workflows]
level: practitioner
status: draft
description: "Choose and use a general orchestrator for ML: Airflow with KubernetesPodOperator, Dagster assets and partitions, Prefect flows; idempotent tasks and passing data by reference."
sources:
  - https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html
  - https://docs.dagster.io/guides/build/assets
  - https://docs.prefect.io/v3/develop/write-flows
  - https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Airflow, Dagster and Prefect for ML workflows

**Goal:** schedule and monitor feature builds, training, batch scoring and evaluation with a general-purpose orchestrator.

## Choosing
| | Strength | Fits when |
|---|---|---|
| Airflow | mature, huge operator ecosystem, schedule-centric DAGs | org already runs Airflow; ML is part of data platform jobs |
| Dagster | software-defined **assets**, partitions, lineage, asset checks | you think in datasets/models produced, need lineage and partial backfills |
| Prefect | Pythonic flows/tasks, dynamic workflows, easy local->cloud | small teams, dynamic branching, fast iteration |
ML-specific platforms (Kubeflow, SageMaker/Vertex Pipelines) add artifact tracking and managed compute; many teams use Airflow/Dagster to *trigger* those.

## Airflow pattern: heavy work in containers
```python
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
train = KubernetesPodOperator(
    task_id="train", name="train-churn", namespace="ml",
    image="registry/churn-train:{{ var.value.train_image_tag }}",
    arguments=["--date", "{{ ds }}", "--out", "s3://ml/models/churn/{{ ds }}/"],
    container_resources=k8s.V1ResourceRequirements(limits={"nvidia.com/gpu": "1", "memory": "32Gi"}),
    get_logs=True,
)
```
Keep the scheduler/worker light; training runs in its own image with pinned deps. Pass S3 paths through XCom, never data (XCom lives in the metadata DB).

## Dagster pattern: assets and partitions
```python
@asset(partitions_def=DailyPartitionsDefinition(start_date="2025-01-01"))
def features(context) -> None:
    build_features(context.partition_key)

@asset(deps=[features])
def churn_model(context) -> None: ...

@asset_check(asset=churn_model)
def auc_above_floor() -> AssetCheckResult: ...
```
Backfilling a date range rematerialises just those partitions; asset checks gate downstream assets.

## Prefect pattern
```python
@task(retries=3, retry_delay_seconds=60, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def build_features(day: str) -> str: ...
@flow
def nightly(day: str):
    path = build_features(day); train(path)
```
Deploy with work pools (Kubernetes, ECS) so flows run on proper infrastructure.

## Rules for all three
- Tasks idempotent and keyed by logical date/partition: re-running writes the same output path (overwrite, not append).
- Parameterise by the data interval (`{{ ds }}`, partition key), never `now()`, so backfills reproduce history.
- Retries for transient failures only; set timeouts on every task.
- Alert on failure and on SLA misses (data not ready by time X).

## Verify
- [ ] Re-running a past date reproduces the same artifacts.
- [ ] No large payloads through XCom/task returns.
- [ ] Failure alerts reach the owning team.
