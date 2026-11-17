---
id: computing-software.data-engineering.apache-airflow.helm-chart-deployment
name: helm-chart-deployment
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-helm-chart, kubernetes, airflow-deployment, git-sync, values-yaml, external-database, pgbouncer, custom-image, keda]
level: advanced
status: gated
description: "Deploy Airflow with the official Helm chart: custom image, external Postgres + PgBouncer, git-sync vs baked DAGs, secrets, KEDA worker autoscaling and upgrades."
sources:
  - https://airflow.apache.org/docs/helm-chart/stable/index.html
  - https://airflow.apache.org/docs/helm-chart/stable/production-guide.html
  - https://airflow.apache.org/docs/helm-chart/stable/manage-dag-files.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying Airflow with the official Helm chart

**Goal:** a production Airflow on Kubernetes that is reproducible, upgradeable, and does not depend on the chart's bundled dev database.

## Install
```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow -n airflow --create-namespace \
  -f values.yaml --version <chart-version> --timeout 15m
```
Pin the chart version; read the chart changelog before bumping (chart and Airflow versions are separate).

## values.yaml essentials
```yaml
images:
  airflow: {repository: <REGISTRY>/airflow, tag: "3.0.6-acme.12"}   # FROM apache/airflow + providers/deps
executor: CeleryExecutor            # or KubernetesExecutor / "CeleryExecutor,KubernetesExecutor"
postgresql: {enabled: false}        # bundled DB is for testing only
data:
  metadataSecretName: airflow-metadata-db     # secret with key "connection": postgresql://...
pgbouncer: {enabled: true, maxClientConn: 200, metadataPoolSize: 20}
webserverSecretKeySecretName: airflow-webserver-secret   # stable key across pods (2.x)
fernetKeySecretName: airflow-fernet-key
dags:
  gitSync:
    enabled: true
    repo: git@github.com:acme/airflow-dags.git
    branch: main
    subPath: dags
    sshKeySecret: airflow-git-ssh
    period: 60s
workers:
  replicas: 2
  keda: {enabled: true, minReplicaCount: 1, maxReplicaCount: 20}   # scale Celery workers on queued tasks
logs:
  persistence: {enabled: false}     # use remote logging to object storage instead
config:
  logging: {remote_logging: "True", remote_base_log_folder: "s3://<BUCKET>/airflow-logs", remote_log_conn_id: aws_default}
```

## DAG delivery choices
| Method | Pros | Cons |
|---|---|---|
| Bake DAGs into the image | Immutable, versioned with deps | Rebuild + redeploy per DAG change |
| git-sync sidecar | Fast DAG updates | DAG code and image deps can drift |
| Shared volume (RWX PVC) | Simple | Slow on some storage, consistency issues |
Most teams: deps in the image, DAGs via git-sync, CI validates DAGs against the same image.

## Operations
- Migrations run as a Helm hook job (`migrateDatabaseJob`); with GitOps tools (Argo CD) set `useHelmHooks: false` and enable the job's Argo-friendly options per chart docs. (gated: unconfirmed, source is paywalled or blocked)
- Secrets (connections) via a secrets backend rather than env vars in values.
- Resource requests for scheduler (CPU-heavy with many DAGs) and dag-processor (Airflow 3 runs it as its own component).
- `helm rollback airflow <rev>` restores manifests, not the DB schema: back up the DB before upgrades that migrate.

## Verify
- [ ] `kubectl -n airflow get pods` all Ready; scheduler heartbeat healthy in UI.
- [ ] A DAG change in git appears within the git-sync period.
- [ ] Workers scale out under a burst of queued tasks and back in afterwards.

## Checked

2026-11-02

- Confirmed: The Airflow Helm chart index, production guide and manage-dag-files pages were fetched; KEDA autoscaling for CeleryExecutor is confirmed.
- Removed or gated: Values keys such as minReplicaCount/maxReplicaCount, the remote logging settings and the example image tag are not stated on the fetched pages; gated, confirm in the chart's values reference.

Method: documentation only; no commands were run.
