---
id: computing-software.devops-ci-cd.gitlab-runner.runner-kubernetes-namespace-per-job
name: runner-kubernetes-namespace-per-job
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [namespace-per-job, kubernetes, isolation, clusterrole]
level: advanced
status: docs-checked
description: "Run each job in its own namespace and the RBAC it requires."
sources: ["https://docs.gitlab.com/runner/executors/kubernetes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Namespace per job

`namespace_per_job = true` isolates jobs in separate namespaces. When enabled, `namespace` and `namespace_overwrite_allowed` are ignored.

The runner creates, deletes and lists resources across namespaces, which a namespaced Role cannot grant. Use a `ClusterRole` and `ClusterRoleBinding`, and include the `namespace` permission that the docs say is needed only for this mode.

## Checked

2026-11-03. Confirmed against namespace_per_job behaviour and RBAC notes on the Kubernetes executor page. Removed unsourced use-case and cleanup text.

Method: documentation only; no commands were run.
