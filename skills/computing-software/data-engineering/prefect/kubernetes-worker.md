---
id: computing-software.data-engineering.prefect.kubernetes-worker
name: kubernetes-worker
category: computing-software
field: data-engineering
product: prefect
tags: [kubernetes, helm, rbac, worker, work-pool]
level: advanced
status: docs-checked
description: "Deploy a Prefect Kubernetes worker with the prefect-worker Helm chart, configure the work pool and job template variables, and grant RBAC."
sources:
  - https://docs.prefect.io/v3/how-to-guides/deployment_infra/kubernetes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run flow runs as Kubernetes jobs.

Install the worker (Cloud):

```bash
helm repo add prefect https://prefecthq.github.io/prefect-helm
helm repo update
kubectl create namespace prefect
kubectl create secret generic prefect-api-key \
  --namespace=prefect --from-literal=key=your-prefect-cloud-api-key
helm install prefect-worker prefect/prefect-worker --namespace=prefect -f values.yaml
```

`values.yaml` keys: `worker.cloudApiConfig.accountId`, `worker.cloudApiConfig.workspaceId`, `worker.config.workPool`.

Work pool of type Kubernetes: namespace (default `default`), image (defaults to `prefecthq/prefect:3-latest`, overridable via `job_variables`), image pull policy (with `IfNotPresent` use unique tags), Finished Job TTL, Backoff Limit (default 0), Pod Watch Timeout Seconds. Template variables take effect only when referenced in `job_configuration` as `{{ variable_name }}`.

`PREFECT_FLOW_RUN_EXECUTE_SIGTERM_BEHAVIOR` accepts `reschedule`, `relinquish` or `crash`.

RBAC: Role `prefect-worker` in `prefect`: pods get/watch/list, pods/log get, batch jobs get/list/watch/create/delete, bound to ServiceAccount `prefect-worker`. Secrets permissions are only needed for `PREFECT_INTEGRATIONS_KUBERNETES_WORKER_CREATE_SECRET_FOR_API_KEY=true` or `..._STORE_ENV_AS_SECRET=true`. The observer is namespace-scoped via `PREFECT_INTEGRATIONS_KUBERNETES_OBSERVER_NAMESPACES`, cluster-wide when unset (needs a ClusterRole), disabled with `PREFECT_INTEGRATIONS_KUBERNETES_OBSERVER_ENABLED=false`.

```bash
kubectl auth can-i create jobs --as=system:serviceaccount:prefect:prefect-worker -n prefect
```

## Checked

2026-11-09. Confirmed: Kubernetes deployment page (docs.prefect.io/v3/how-to-guides/deployment_infra/kubernetes): Helm commands, values.yaml keys under worker, work pool options and defaults, SIGTERM behaviour values, template variable rule, RBAC Role rules, secrets permissions, observer settings, kubectl auth can-i. Nothing removed.

Method: documentation only; no commands were run.
