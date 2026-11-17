---
id: computing-software.data-engineering.apache-airflow.celery-worker-autoscaling-with-keda
name: celery-worker-autoscaling-with-keda
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, celeryexecutor, keda-autoscaling, helm-chart, worker-scaling, kubernetes, scale-to-zero, worker-concurrency]
level: advanced
status: docs-checked
description: "Autoscale Airflow Celery workers on Kubernetes with KEDA via the official Helm chart: the task-count query, concurrency math, scale-down safety and termination grace."
sources:
  - https://airflow.apache.org/docs/helm-chart/stable/keda.html
  - https://keda.sh/docs/latest/scalers/postgresql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Celery worker autoscaling with KEDA

**Goal:** worker count follows queued+running tasks, scaling to near zero at night, without killing running tasks on scale-down.

## Enable in the Helm chart
```bash
helm install keda kedacore/keda -n keda --create-namespace
```
```yaml
# values.yaml
executor: CeleryExecutor
workers:
  keda:
    enabled: true
    minReplicaCount: 0
    maxReplicaCount: 20
    pollingInterval: 5
    cooldownPeriod: 3700                    # slightly larger than terminationGracePeriodSeconds
  terminationGracePeriodSeconds: 3600       # let running tasks finish
config:
  celery:
    worker_concurrency: 16
```
The chart creates a `ScaledObject` with a PostgreSQL (or MySQL) scaler querying the metadata DB:
```sql
SELECT ceil(COUNT(*)::decimal / 16)
FROM task_instance
WHERE (state='running' OR state='queued')
  AND queue IN ('default')        -- per worker queue set
```
Desired replicas = ceil((running + queued) / worker_concurrency).

## Requirements and constraints
- KEDA queries the metadata DB directly; see the chart's KEDA page for the connection options when PgBouncer is in use.
- See the chart's KEDA page for restrictions on worker persistence (StatefulSet workers) when KEDA is enabled.
- Use remote logging; local worker logs disappear with scaled-down pods.

## Scale-down safety
On scale-down, k8s sends SIGTERM; Celery warm shutdown stops taking tasks and waits for running ones up to `terminationGracePeriodSeconds`. Tasks longer than that are killed and retried (if retries). For very long tasks, use KubernetesExecutor/KPO instead or a dedicated non-autoscaled queue.

## Queues
To scale GPU or high-memory queues independently, run a separate worker Deployment per queue (separate release or chart feature, depending on chart version), each with its own ScaledObject whose query filters on that queue.

## Tuning
- `worker_concurrency`: match pod CPU/memory; heavy tasks -> lower concurrency.
- Set `cooldownPeriod` slightly larger than `terminationGracePeriodSeconds`, so the cluster does not downscale to 0 workers before cleanup is finished.
- Scale-from-zero latency = KEDA poll + pod scheduling + image pull. Pre-pull images or keep `minReplicaCount: 1` for latency-sensitive DAGs.

## Verify
- [ ] Queue 100 tasks: replicas rise to ceil(100/concurrency) within a minute.
- [ ] Scale-down during running tasks: tasks finish (no `SIGTERM` failures) within grace period.

## Checked

2026-10-28. Confirmed in the Airflow Helm chart KEDA page: `workers.keda` settings (`minReplicaCount`, `pollingInterval`, `cooldownPeriod`), the task-count query shape (`ceil(COUNT(*) / worker_concurrency)` over running and queued task instances), `terminationGracePeriodSeconds`, and the advice to set `cooldownPeriod` slightly above it. Fixed: the example set `cooldownPeriod: 30` against a 3600 s grace period, contradicting that advice. Removed: `usePgbouncer` and `persistence.enabled` option names and the 300 s default.
Method: documentation only; no commands were run.
