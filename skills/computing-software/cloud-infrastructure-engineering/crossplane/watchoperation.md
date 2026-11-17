---
id: computing-software.cloud-infrastructure-engineering.crossplane.watchoperation
name: watchoperation
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [watchoperation, operations, watch, trigger, labels]
level: advanced
status: docs-checked
description: "Trigger Operations when watched Kubernetes resources change using WatchOperation."
sources:
  - https://docs.crossplane.io/latest/operations/watchoperation/
  - https://docs.crossplane.io/latest/operations/operation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `WatchOperation` creates an Operation whenever a watched resource changes. It can watch any Kubernetes type, not only Crossplane ones. Alpha; requires `--enable-operations`.

```yaml
apiVersion: ops.crossplane.io/v1alpha1
kind: WatchOperation
metadata:
  name: config-validator
spec:
  watch:
    apiVersion: v1
    kind: ConfigMap
    namespace: production
    matchLabels:
      validate: "true"
  concurrencyPolicy: Allow
  operationTemplate:
    spec:
      mode: Pipeline
      pipeline:
      - step: validate
        functionRef:
          name: function-config-validator
```

Filter with `namespace` and `matchLabels`.

The changed resource is injected automatically as a required resource named `ops.crossplane.io/watched-resource`. In the Python SDK it appears in `req.required_resources` under that name; the function need not request it.

`concurrencyPolicy` works as for CronOperation: `Allow` (default), `Forbid`, `Replace`.

Typical uses: validate configuration after updates, back up before deletion, alert when resources fail.

Typical flow: a ConfigMap with the matching label changes, Crossplane creates an Operation, and the function receives that ConfigMap under `ops.crossplane.io/watched-resource`. Create a new Operation for each change event.

Inspect with `kubectl get watchoperations` and `kubectl get operations`. Combine with `retryLimit` in the template so flaky checks do not loop forever.

Operations run with Crossplane's service account. For kinds it cannot access by default, create a ClusterRole labelled `rbac.crossplane.io/aggregate-to-crossplane: "true"` so it aggregates into Crossplane's role (documented on the Operation page). If the WatchOperation is not creating Operations, check for the `Watching=True` condition and for events about watch establishment failures (`EstablishWatched`).

## Checked

2026-11-08: read the whole Crossplane Watch Operations guide and the Operation guide (raw sources of docs.crossplane.io/latest/operations/watchoperation and operation). Confirmed the manifest fields, namespace and `matchLabels` filtering, injection of the changed resource under `ops.crossplane.io/watched-resource` in `req.required_resources`, the concurrency policies, the `Watching` condition, the `EstablishWatched` event, `retryLimit` and the aggregate-to-crossplane ClusterRole label. Removed the claim that a missing ClusterRole stops the watch from starting (not stated); the RBAC advice is now attributed to the Operation page, which is added to sources.
Method: documentation only; no commands were run.
