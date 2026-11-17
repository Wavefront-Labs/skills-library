---
id: computing-software.devops-ci-cd.helm.storage-backends-and-driver
name: storage-backends-and-driver
category: computing-software
field: devops-ci-cd
product: helm
tags: [storage-backend, helm-driver, secrets, configmaps, sql, memory, release-records, max-history]
level: advanced
status: docs-checked
description: "Where Helm stores release records: HELM_DRIVER secret, configmap, memory or sql, and capping history with --history-max."
sources:
  - "https://helm.sh/docs/topics/advanced/"
  - "https://helm.sh/docs/helm/helm/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default Helm stores release information in Secrets in the namespace of the release. `HELM_DRIVER` selects the backend:

- `secret` (default): release information is stored in Secrets in the release's namespace.
- `configmap`: the same data in ConfigMaps.
- `memory`: listed as a `HELM_DRIVER` value in the `helm` reference.
- `sql`: records in a PostgreSQL database; the connection string comes from `HELM_DRIVER_SQL_CONNECTION_STRING`. Only PostgreSQL is supported; the docs recommend a production-ready database and permission management mirroring Kubernetes RBAC.

Choose a non-default driver by exporting `HELM_DRIVER` (accepted values: `configmap`, `secret`, `memory`, `sql`).

Each upgrade creates a new revision record. Cap them with `helm upgrade --history-max N` (default 10; 0 means no limit) or the environment variable `HELM_MAX_HISTORY`.

`helm uninstall --keep-history` retains the release history, and such releases show in `helm list --uninstalled`.

Switching from the default backend to ConfigMap or SQL needs a manual migration; `kubectl get secret --all-namespaces -l "owner=helm"` retrieves release information.

Because records are namespaced, always pass `-n`/`--namespace` (or `HELM_NAMESPACE`) when inspecting a release.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/topics/advanced/ (storage backends: Secrets default, ConfigMap, SQL PostgreSQL only, manual migration) and https://helm.sh/docs/helm/helm/ (HELM_DRIVER values, HELM_DRIVER_SQL_CONNECTION_STRING, HELM_MAX_HISTORY, HELM_NAMESPACE), helm upgrade (--history-max, default 10). Removed: the Secret naming scheme, the 1 MiB record-size claim, the memory driver description and the `helm rollback` claim (not on the pages).
Method: documentation only; no commands were run.

