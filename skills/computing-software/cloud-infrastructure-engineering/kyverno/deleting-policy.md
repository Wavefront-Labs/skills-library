---
id: computing-software.cloud-infrastructure-engineering.kyverno.deleting-policy
name: deleting-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [deletingpolicy, schedule, cron, deletionpropagationpolicy, cleanup-controller, conditions]
level: practitioner
status: docs-checked
description: "Write Kyverno DeletingPolicy: cron schedule, matchConstraints, CEL conditions, deletion propagation, cleanup-controller RBAC and the audit event."
sources:
  - https://kyverno.io/docs/policy-types/deleting-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`DeletingPolicy` (stable as of v1.19) deletes matching resources on a schedule. It is cluster-scoped; `NamespacedDeletingPolicy` is limited to its own namespace. Standard Kyverno CEL libraries work; user CEL libraries do not.

Fields:
- `schedule`: standard cron, 1-minute minimum granularity, e.g. `'0 1 * * *'` for daily at 1 AM.
- `matchConstraints.resourceRules`: `apiGroups`, `apiVersions`, `resources`, `operations`, `scope` (e.g. `'Namespaced'`); `matchConstraints.namespaceSelector` with `matchLabels`.
- `conditions[]`: `name` and CEL `expression` selecting which matched resources are deleted, e.g. `has(object.metadata.labels.old) && object.metadata.labels.old == 'true'`.
- `variables[]`: `name` and `expression`.
- `matchPolicy`: `Exact` or `Equivalent` (recommended).
- `deletionPropagationPolicy`: `Orphan`, `Background` or `Foreground` (cascading before the owner is removed).

RBAC: the cleanup controller needs `get`, `list`, `watch`, `delete` on the targets. Core resources may lack default permissions on Minikube and Kind; deployments and networkpolicies always need explicit RBAC (a ClusterRole and ClusterRoleBinding).

Audit: each deletion emits an event with `reason: PolicyApplied` and `reportingComponent: kyverno-cleanup`; list with `kubectl get events --field-selector reason=PolicyApplied -A`.

This is destructive. Try it in staging, keep selectors and conditions strict, be careful with `*` wildcards, and validate CEL with the Kyverno CLI before enabling.

## Checked

Checked 2026-11-08 against the Kyverno DeletingPolicy page (read in full): stable in v1.19, scope variants, schedule, matchPolicy, deletionPropagationPolicy, the example fields, CEL library note, RBAC verbs, event fields and the cautions. Removed the unstated claim that all conditions must be true.

Method: documentation only; no commands were run.
