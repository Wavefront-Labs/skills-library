---
id: computing-software.cloud-infrastructure-engineering.velero.repository-maintenance-jobs
name: repository-maintenance-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [repository-maintenance, maintenance-job, repo-maintenance-job-configmap, keep-latest-maintenance-jobs, loadaffinity]
level: advanced
status: docs-checked
description: "Configure Velero repository maintenance jobs: ConfigMap keys, per-repository overrides, retention count, frequency and history."
sources:
  - https://velero.io/docs/main/repository-maintenance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since 1.14 Velero runs repository maintenance as separate Kubernetes jobs in the install namespace instead of inside the server pod. Jobs have no resource limit by default.

From 1.15 a ConfigMap, passed with `velero server --repo-maintenance-job-configmap` (or `velero install --repo-maintenance-job-configmap=<name>`), configures them. It is a map of JSON values:
- `global`: applies to every repository without its own key.
- `<volume namespace>-<BSL name>-<type>`: one repository, for example `test-default-kopia` (type is `kopia`).

Each value can hold `podResources` (`cpuRequest`, `cpuLimit`, `memoryRequest`, `memoryLimit`, `ephemeralStorageRequest`, `ephemeralStorageLimit`), `keepLatestMaintenanceJobs`, and `loadAffinity`. Only the first element of the `loadAffinity` array is used. `priorityClassName` and `tolerations` are read only from `global`.

Install flags: `--keep-latest-maintenance-jobs <NUM>` (default 3 per repository) and `--default-repo-maintain-frequency <DURATION>` (Kopia default 1 hour).

History: `kubectl -n velero describe backuprepository NAME` shows `Last Maintenance Time` and the 3 most recent entries in `Recent Maintenance` with result and error message.

Jobs inherit the log level, nodeSelector, service account, image, environment and priority class of the server, but only a short list of labels, annotations and tolerations. Jobs do not run for a BSL set to read-only.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/repository-maintenance/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
