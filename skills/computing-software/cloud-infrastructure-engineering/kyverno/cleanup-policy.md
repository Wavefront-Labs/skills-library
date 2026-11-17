---
id: computing-software.cloud-infrastructure-engineering.kyverno.cleanup-policy
name: cleanup-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [cleanuppolicy, clustercleanuppolicy, ttl-label, cleanup-controller, schedule, propagation-policy]
level: practitioner
status: docs-checked
description: "Use deprecated Kyverno CleanupPolicy and the cleanup.kyverno.io/ttl label: schedule, match limits, RBAC for the cleanup controller and TTL formats."
sources:
  - https://kyverno.io/docs/policy-types/cleanup-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`CleanupPolicy` (namespaced) and `ClusterCleanupPolicy` are deprecated as of v1.19 and slated for removal in v1.20; the replacement is DeletingPolicy.

Fields: `match`/`exclude` (same block structure), optional `conditions`, optional context variables, `schedule` (cron string) and optional `deletionPropagationPolicy` (`Foreground`, `Background`, `Orphan`; API server default if unset). Reference the target as `target.*`, e.g. `{{ target.spec.replicas }}`.

Restrictions: `subjects`, `Roles` and `ClusterRoles` are not allowed in `match`/`exclude` (that data exists only at admission). `operations[]` is accepted but ignored; only the schedule triggers cleanup.

RBAC: the cleanup controller needs explicit permission for each resource type it deletes. Kyverno checks this when the policy is installed and reports what is missing. The docs' example ClusterRole `kyverno:cleanup-pods` grants `get`, `watch`, `list`, `delete` on pods; adjust it to your deployment.

TTL label `cleanup.kyverno.io/ttl` works without any cleanup policy and applies to any resource Kyverno can delete. Value is an absolute ISO 8601 time (`2023-10-04`) or a duration relative to when the label is first observed (`5m`, `4h`, `1d`); unrecognised formats warn. Granularity is the cleanup controller flag `ttlReconciliationInterval` (default `1m`). Set the annotation `cleanup.kyverno.io/propagation-policy` to choose propagation for TTL deletions.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
