---
id: computing-software.cloud-infrastructure-engineering.crossplane.operation-basics
name: operation-basics
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [operation, ops, function-pipeline, alpha, retry]
level: advanced
status: docs-checked
description: "Run a function pipeline once to completion with an Operation, including retries, credentials and required resources."
sources:
  - https://docs.crossplane.io/latest/operations/operation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An `Operation` is like a Kubernetes Job built on function pipelines. It is alpha: add `--enable-operations` to Crossplane's args.

```yaml
apiVersion: ops.crossplane.io/v1alpha1
kind: Operation
metadata:
  name: backup-database
spec:
  retryLimit: 10
  mode: Pipeline
  pipeline:
  - step: create-backup
    functionRef:
      name: function-database-backup
```

Differences from composition functions: operations get only required resources as input, may output any Kubernetes resources, and force-apply them without owner references.

Details:

- `retryLimit` defaults to 5. Each retry restarts the whole pipeline, with backoff 1s doubling to a 60s maximum. `status.failures` counts them; after the limit `Succeeded=False`.
- `credentials` on a step reference Secrets (`source: Secret`, `secretRef` with namespace, name, key).
- `requirements.requiredResources` preloads resources by `requirementName`, `apiVersion`, `kind`, `name`, `namespace`.
- Aggregate extra RBAC to Crossplane with a ClusterRole labelled `rbac.crossplane.io/aggregate-to-crossplane: "true"`.
- `--enable-function-response-cache` can cache repeated function calls.

Status conditions: `Synced`, `Succeeded`, `ValidPipeline`. The function must declare the `operation` capability.

Inspect runs with `kubectl get operations` and `kubectl describe operation NAME`; the `Succeeded` condition tells you whether the pipeline finished.

## Checked

2026-11-08: read the whole Crossplane Operations guide (raw source of docs.crossplane.io/latest/operations/operation). Confirmed the alpha flag `--enable-operations`, `ops.crossplane.io/v1alpha1` Operation shape, differences from composition functions, `retryLimit` default 5 and backoff 1s doubling to 60s, `status.failures`, `credentials`, `requirements.requiredResources` fields, the aggregate-to-crossplane ClusterRole label, `--enable-function-response-cache`, the three conditions and the `operation` capability.
Method: documentation only; no commands were run.
