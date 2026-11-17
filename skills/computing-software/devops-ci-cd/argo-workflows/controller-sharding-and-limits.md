---
id: computing-software.devops-ci-cd.argo-workflows.controller-sharding-and-limits
name: controller-sharding-and-limits
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [instance-id, resource-rate-limit, namespaced-install, max-recursion, semaphore-limit-cache]
level: advanced
status: docs-checked
description: "Limit pod creation rate with resourceRateLimit, shard with --namespaced or instanceID, and tune recursion depth and semaphore ConfigMap caching."
sources: ["https://argo-workflows.readthedocs.io/en/latest/scaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharding, pod rate limit and recursion
Pod creation rate: pods are expensive for the API server. In the controller ConfigMap:

```yaml
resourceRateLimit: |
  limit: 10
  burst: 25
```
`limit` is the average pod requests per second and `burst` the amount allowed before the limit applies (keep burst above limit). It applies only to Pods, not to ConfigMaps or PVCs.

Sharding:
- One install per namespace with the `--namespaced` flag.
- Instance IDs: set `instanceID: i1` in `workflow-controller-configmap`. The CLI then needs `argo --instanceid i1 submit my-wf.yaml`. Declaratively, label resources with `workflows.argoproj.io/controller-instanceid: i1`. In a WorkflowTemplate it helps to repeat the label under `spec.templateDefaults.metadata.labels`.

Recursion: the controller stops templates calling themselves past a default depth of 100 calls. Disable with the controller environment variable `DISABLE_MAX_RECURSION=true`.

Semaphore caching: by default the ConfigMap behind a semaphore is reloaded each time a workflow is queued. If queuing is slow, set `semaphoreLimitCacheSeconds` in the controller ConfigMap; changes to the semaphore limit are then not picked up immediately.

For extreme sizes see the separate massive scale page.

## Checked
2026-11-08. Confirmed against the Argo Workflows Scaling page: `resourceRateLimit` limit and burst and the Pods-only scope, `--namespaced`, `instanceID`, the `--instanceid` CLI flag and the controller-instanceid label, `templateDefaults` labels, the default recursion depth of 100 and `DISABLE_MAX_RECURSION`, and `semaphoreLimitCacheSeconds`. Nothing removed.
Method: documentation only; no commands were run.
