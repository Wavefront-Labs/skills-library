---
id: computing-software.data-engineering.apache-airflow.executors-connections-and-secrets
name: executors-connections-and-secrets
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, executor, celeryexecutor, kubernetesexecutor, localexecutor, connections, secrets-backend, hashicorp-vault, aws-secrets-manager, variables, pools, kubernetespodoperator, mwaa, cloud-composer, astronomer, worker-pods]
level: practitioner
status: docs-checked
description: "Choose and operate an Airflow executor (Local/Celery/Kubernetes), and manage connections and secrets safely at scale."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html
  - https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/secrets-backend/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Executors, connections and secrets

**Goal:** pick the right executor for your scale, and stop storing production credentials in the metadata DB's Connections table in plaintext-equivalent form.

## 1. Executors — what actually runs a task
- **LocalExecutor**: runs tasks as subprocesses on the scheduler host. Fine for a single-node install with modest concurrency (tens of concurrent tasks); scheduler host CPU/RAM is your ceiling.
- **CeleryExecutor**: tasks go on a message broker (Redis/RabbitMQ) to a pool of persistent worker processes. Scales horizontally by adding workers; workers need the same DAG code/dependencies deployed (sync problem — use a shared volume, baked image, or git-sync sidecar). Worker autoscaling is manual/external (Celery's own autoscale option, or scale the worker deployment).
- **KubernetesExecutor**: each task gets its own pod, scheduled by k8s, torn down after. No idle workers, true per-task resource isolation (give one task more memory than the next), but pod startup latency (seconds) adds up for many small/fast tasks — bad fit for DAGs with hundreds of sub-second tasks.
- Configuring more than one executor lets you mix: steady-state tasks on Celery workers, heavy/odd ones to Kubernetes pods via a task-level `executor=` override (see the Executor docs).
- Managed services (MWAA, Cloud Composer, Astronomer) pick one for you (usually Celery or Kubernetes) and expose worker count/size as a knob — check which before assuming you can switch.

## 2. Connections — where credentials actually live
- Connections table in the metadata DB stores a Fernet-encrypted password field (`AIRFLOW__CORE__FERNET_KEY`), not secure against anyone with DB access + the key, which is usually in the same env/secret store. Treat it as encrypted-at-rest, not a vault.
- `AIRFLOW_CONN_<CONN_ID>` env var (URI-encoded) sets a connection without touching the DB — the standard way to inject per-environment creds from CI/CD secrets.
- **Secrets backend** (`secrets.backend` config) lets Airflow fetch connections/variables directly from HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, or Azure Key Vault at lookup time instead of storing them in the DB at all — the correct answer for production. Configure `backend_kwargs` with the path prefix (e.g. `connections_prefix: airflow/connections`) and Airflow checks the backend before the DB/env.
- **Gotcha:** the documented search order is secrets backend first, then environment variables, then the metastore (not configurable), so a connection missing from the backend still resolves from a stale env var or DB row left from before migration. Delete the old DB-stored connection after cutting over, don't just add the backend.

## 3. Pools and queues — protecting shared resources
- A **pool** caps concurrent task instances across DAGs that share a bottleneck (e.g. a `pool="source_db"` with 5 slots so no combination of DAGs opens more than 5 connections to a fragile upstream). Set via UI/CLI, referenced by `pool=` on the task.
- A **queue** (Celery-specific) routes tasks to specific worker groups (e.g. a `gpu` queue serviced only by GPU-equipped workers). Don't confuse pools (concurrency limit) with queues (routing).

## Verify
- [ ] No connection's password/extra field is readable by someone without both DB access and the Fernet key — ideally, secrets backend means the DB field is empty/absent.
- [ ] Worker count and executor match load: Celery workers aren't idling at 5% CPU 24/7 while KubernetesExecutor pod startup isn't dominating short-task runtime.
- [ ] A rotated credential in Vault/Secrets Manager takes effect on the next task run without an Airflow restart (confirms backend, not DB, is authoritative).
- [ ] A pool exists for every shared external bottleneck (source DB, rate-limited API) referenced by more than one DAG.

## Checked

2026-10-28. Confirmed: secrets search order and backend_kwargs on the secrets backend page; task-level executor= example on the executor page. Removed: SequentialExecutor (not in the current executor page), a fails-open claim, a version gate and example memory sizes.

Method: documentation only; no commands were run.
