---
id: computing-software.cloud-infrastructure-engineering.crossplane.mr-annotations-finalizers
name: mr-annotations-finalizers
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [managed-resource, paused, poll-interval, finalizer, conditions]
level: practitioner
status: docs-checked
description: "Pause, tune polling and force reconcile of an MR with annotations, and read its finalizer and conditions."
sources:
  - https://docs.crossplane.io/latest/managed-resources/managed-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Annotations on a managed resource:

- `crossplane.io/paused: "true"` stops reconciliation; only the value `"true"` pauses. A paused MR cannot be deleted, even with `kubectl delete`, until you remove the annotation.
- `crossplane.io/poll-interval` overrides `--poll-interval` per MR (`30m`, `1h`, `24h`). Invalid durations fall back to the default; values below `--min-poll-interval` (default `1s`) are raised to it.
- `crossplane.io/reconcile-requested-at` triggers a reconcile when its value changes.

```shell
kubectl annotate instance my-rds-instance \
  crossplane.io/reconcile-requested-at="$(date -u +%Y-%m-%dT%H:%M:%SZ)" --overwrite
kubectl get instance my-rds-instance -o jsonpath='{.status.lastHandledReconcileAt}'
```

Crossplane adds a finalizer so the MR object stays until the external resource is fully deleted.

Condition reasons for `Ready`: `Available`, `Creating`, `Deleting`. `Synced` False with reason `ReconcilePaused` means the pause annotation is set. View them with `kubectl describe <managed resource>`.

To unpause, remove the annotation.

## Checked

2026-11-03. Confirmed against the Crossplane docs (Managed Resources page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the finalizer-removal advice and the kubectl get managed quick check (not on the page).

Method: documentation only; no commands were run.
