---
id: computing-software.data-engineering.apache-airflow.task-routing-queues-pools-and-executor-config
name: task-routing-queues-pools-and-executor-config
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, executor-config, celery-queues, pool-slots, pod-override, task-routing]
level: advanced
status: gated
description: "Route Airflow tasks to the right workers and resources with queue, pool and pool_slots, priority_weight, per-task executor, and KubernetesExecutor pod_override."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html
  - https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/kubernetes_executor.html
  - https://airflow.apache.org/docs/apache-airflow-providers-celery/stable/celery_executor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task routing: queue, pools, pool_slots, executor_config

**Goal:** send heavy or special tasks to suitable capacity and stop a burst of one workload from starving another.

## Celery queues
```python
heavy = PythonOperator(task_id="train", python_callable=train, queue="gpu")
```
Start workers that consume it: `airflow celery worker --queues gpu` (others default to `[operators] default_queue = default`). A task on a queue no worker listens to sits in `queued` forever. (gated: unconfirmed, source is paywalled or blocked)

## Pools and pool_slots
```bash
airflow pools set warehouse_heavy 8 "Snowflake heavy queries"
```
```python
SQLExecuteQueryOperator(task_id="rebuild", pool="warehouse_heavy", pool_slots=4, sql="...")
```
- A pool caps concurrent **slots**, not tasks; a task with `pool_slots=4` uses half of an 8-slot pool.
- `default_pool` (128 slots) catches everything else. Deferred tasks do not use a slot unless the pool has `include_deferred` set.
- `priority_weight` + `weight_rule` (`downstream`, `upstream`, `absolute`) decides which queued task gets the next free slot.

## Per-task executor (2.10+, multiple executors)
```python
task = BashOperator(task_id="spark_submit", executor="KubernetesExecutor", bash_command="...")
```
Requires `[core] executor = CeleryExecutor,KubernetesExecutor` (first is the default).

## KubernetesExecutor / KubernetesPodOperator resources
```python
from kubernetes.client import models as k8s
executor_config = {"pod_override": k8s.V1Pod(spec=k8s.V1PodSpec(containers=[
    k8s.V1Container(name="base",                       # must be "base" to override the task container
        resources=k8s.V1ResourceRequirements(requests={"cpu": "2", "memory": "8Gi"},
                                             limits={"memory": "8Gi"}))],
    node_selector={"pool": "highmem"}))}
PythonOperator(task_id="big_join", python_callable=f, executor_config=executor_config)
```

## Gotchas
- `max_active_tis_per_dag` / `max_active_tasks` limit per DAG; pools limit across DAGs. You often need both.
- Container name in `pod_override` other than `base` adds a sidecar instead of changing the task container.
- Pool slot counts are not auto-created from code: create pools via CLI, API or Helm values before deploy, or tasks fail to schedule with "pool does not exist".

## Verify
Grid view task details show pool/queue; `airflow pools list` shows used/queued slots during a run.

## Checked

2026-11-02

- Confirmed: The Airflow pools page (pool_slots default of one slot, pool_slots argument) plus the Celery and Kubernetes executor provider pages were fetched.
- Removed or gated: include_deferred, priority_weight/weight_rule, multi-executor config syntax and max_active_tis_per_dag were not seen on the fetched pages; gated, confirm in the Airflow configuration reference.

Method: documentation only; no commands were run.
