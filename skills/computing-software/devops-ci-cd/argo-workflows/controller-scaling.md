---
id: computing-software.devops-ci-cd.argo-workflows.controller-scaling
name: controller-scaling
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [controller-scaling, workflow-workers, qps-burst, client-side-throttling, informer-cache]
level: advanced
status: docs-checked
description: "Scale the workflow controller with resource requests, worker flags and Kubernetes client qps and burst limits, since it cannot be scaled horizontally."
sources: ["https://argo-workflows.readthedocs.io/en/latest/scaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaling the controller vertically
The controller cannot scale horizontally; a hot standby exists only for high availability. Scale it vertically.

Resources: raise CPU and memory requests when it hits them. At scale memory is dominated by informer caches holding every live Workflow, Pod and related object. Since v4.1 it strips `metadata.managedFields` before caching, so compare heap profiles across versions with that in mind.

Concurrency flags, given enough CPU cores:
- `--workflow-workers` when many Workflows are not reconciled fast enough
- `--workflow-ttl-workers` when `TTLStrategy` deletion is too slow
- `--pod-cleanup-workers` when `PodGC` is too slow
- `--cron-workflow-workers` when CronWorkflows fire late

Client-side throttling: log lines such as `Waited for 7.09s due to client-side throttling, not priority and fairness` (or a shorter `Waited for ... request:GET ...` warning, possibly for any custom resource) show the Kubernetes client limiter is delaying calls. Raise `--qps` (default 20, average queries per second) and `--burst` (default 30, allowance before qps is enforced; keep burst above qps):

```yaml
args:
  - --qps=50
  - --burst=75
```

Higher values load the API server harder. Judge with cluster-wide observability; there is no universal value.

## Checked
2026-11-03. Confirmed against the Argo Workflows Scaling page: no horizontal scaling, informer cache memory and the v4.1 managedFields change, the four worker flags, the throttling log messages, the --qps (20) and --burst (30) defaults and the example values. Nothing removed.
Method: documentation only; no commands were run.
