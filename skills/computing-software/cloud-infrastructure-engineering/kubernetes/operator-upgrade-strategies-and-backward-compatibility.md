---
id: computing-software.cloud-infrastructure-engineering.kubernetes.operator-upgrade-strategies-and-backward-compatibility
name: operator-upgrade-strategies-and-backward-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator-upgrade, operators, crd-versioning, storage-version-migration, olm, backward-compatibility, storageversionmigration]
level: advanced
status: docs-checked
description: "Ship operator upgrades without breaking existing custom resources: compatible CRD changes, storage version migration, leader handover, OLM upgrade graphs, and upgrade testing."
sources: ["https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/", "https://kubernetes.io/docs/tasks/manage-kubernetes-objects/storage-version-migration/", "https://olm.operatorframework.io/docs/concepts/olm-architecture/operator-catalog/creating-an-update-graph/", "https://olm.operatorframework.io/docs/concepts/crds/subscription/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Operator upgrade strategies

An operator upgrade changes three things at once: CRD schema, controller behaviour, and the
resources it manages. Users' CRs written months ago must keep working.

## API compatibility rules
- Within a version: only **additive, optional** fields with defaults. Never rename, remove,
  retype, or tighten validation on existing fields.
- Breaking changes need a **new version** (`v1beta1` -> `v1`), served side by side, with a
  conversion webhook if schemas differ (`strategy: Webhook`).
- Keep finalizer names, label keys and owned-resource names stable; a renamed finalizer
  orphans deletions, a renamed child resource gets recreated (data loss for PVC-backed apps).
- Status conditions: add new types; do not change the meaning of existing ones.

## Storage version migration (removing an old version)
1. Release N: serve v1beta1 and v1, **storage = v1**.
2. Rewrite every stored object to v1, either with a `StorageVersionMigration` resource
   (`storagemigration.k8s.io/v1`; the `StorageVersionMigrator` feature gate and API are enabled by default in
   the current docs, min server version v1.30) or by reading and writing each object (no-op update).
   After a successful migration the old version is removed from `status.storedVersions` for you.
3. With the manual option, remove `v1beta1` from `status.storedVersions` on the CRD yourself:
```bash
kubectl get crd widgets.example.com -o jsonpath='{.status.storedVersions}'
kubectl patch crd widgets.example.com --subresource=status --type=merge -p '{"status":{"storedVersions":["v1"]}}'
```
4. Release N+1: stop serving v1beta1 (`served: false`; clients still using it get errors, so flip it back
   if needed), confirm `storage: true` is on the new version and the old one is not in `status.storedVersions`,
   then remove the old version from `spec.versions` and drop its conversion support.
An old version cannot be dropped from the CRD until stored data has been migrated and it is removed from
`status.storedVersions`.

## Controller rollout
- CRDs first, then the controller Deployment (CRDs must accept new fields before the new
  controller writes them).
- Use leader election so only one instance reconciles at a time, with a Deployment strategy of `Recreate`
  or `RollingUpdate`. Old and new briefly coexist: the old one must tolerate unknown fields.
- The first reconcile after an upgrade touches every object: watch API load, throttle with
  `MaxConcurrentReconciles`, and avoid mass restarts of managed workloads (for example a hash-based rollout
  changing because a default was added).

## OLM packaging
- Channels (`stable`, `fast`), upgrade edges via `replaces`, `skips`, `skipRange: '>=1.2.0 <1.5.0'` on
  `olm.channel` entries in a file-based catalog.
- `installPlanApproval: Manual` in production Subscriptions so upgrades are reviewed.
- Validate the catalog graph with `opm validate`.

## Test the upgrade path, not just the new version
In CI: install release N on kind, create representative CRs (including old-version ones),
upgrade to N+1, assert CRs reconcile to Ready and managed resources are unchanged
(no unintended restarts). Also test rollback N+1 -> N before any storage version change.

## Verify
- [ ] `storedVersions` contains only served versions; no reconcile error spike after upgrade;
  managed workloads did not restart unexpectedly.

## Checked

Checked on 2026-10-26 against the Kubernetes website docs `custom-resource-definition-versioning.md` and `storage-version-migration.md` (`kubernetes/website`), and `operator-framework/olm-docs` (`creating-an-update-graph`, `file-based-catalogs`, `subscription`).
Confirmed: version removal steps and the `status.storedVersions` rule, the `kubectl patch ... --subresource='status'` command, `storagemigration.k8s.io/v1` `StorageVersionMigration` with automatic `storedVersions` cleanup, conversion strategy `Webhook`, `replaces`/`skips`/`skipRange` in `olm.channel` entries, `installPlanApproval: Manual`.
Wrong or stale in the draft: the migration API is no longer alpha or beta behind a gate; the old version leaves `storedVersions` automatically after a successful migration.

Method: documentation only; no commands were run.
