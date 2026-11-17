---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-kubernetes-backend
name: woodpecker-kubernetes-backend
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [kubernetes-backend, pvc, namespace]
level: advanced
status: docs-checked
description: "Understand the Woodpecker Kubernetes backend: pods, PVC, namespaces, storage and headless services."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/backends/kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker Kubernetes backend basics

The Kubernetes backend runs steps as standalone Pods. A temporary PVC is created for the pipeline's lifetime to transfer files between steps. Per workflow, a headless service is created and steps get the matching subdomain, so any step can reach another by step name on any port.

Agent settings (`WOODPECKER_BACKEND_K8S_` prefix):

- `NAMESPACE` (default `woodpecker`): where Pods are created.
- `NAMESPACE_PER_ORGANIZATION` (false): each organization gets `{NAMESPACE}-{organization-id}`, created automatically and never deleted.
- `CLUSTER_DOMAIN` (`cluster.local`).
- `VOLUME_SIZE` (`10G`), `STORAGE_CLASS`, and `STORAGE_RWX` (true; false uses RWO).
- `PULL_SECRET_NAMES`: Kubernetes secrets for private images, from the namespace.
- `PRIORITY_CLASS`, `STOP_TIMEOUT` (20 seconds).
- `PERMISSION_INIT_IMAGE` (`busybox:stable-musl`).
- `SECCTX_NONROOT` (false) requires non-root containers.
- `USER_NAMESPACES` (false): run in a dedicated user namespace (`hostUsers: false`).
- `ALLOW_NATIVE_SECRETS` (false): lets steps reference existing Kubernetes secrets.

Pods carry labels such as `woodpecker-ci.org/repo-id`, `woodpecker-ci.org/branch` and `woodpecker-ci.org/task-uuid`, useful for network policies. CRI-O users need `workspace: {base: /woodpecker, path: /}` at the top of each workflow.

Set `KUBERNETES_SERVICE_HOST` on the agent if it runs outside the cluster.

## Checked

2026-11-03. Read the Woodpecker Kubernetes backend page and confirmed the K8S backend variables and defaults (namespace, per-organization namespace format, cluster domain, storage, stop timeout of 20 seconds), pod labels and the CRI-O workspace tip. Nothing removed. 

Method: documentation only; no commands were run.
