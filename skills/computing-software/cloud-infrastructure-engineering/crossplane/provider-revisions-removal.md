---
id: computing-software.cloud-infrastructure-engineering.crossplane.provider-revisions-removal
name: provider-revisions-removal
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [provider, providerrevision, upgrade, removal, conditions]
level: practitioner
status: docs-checked
description: "Upgrade a Provider through revisions, read package conditions, and remove a Provider safely."
sources:
  - https://docs.crossplane.io/latest/packages/providers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrade by changing the version in `spec.package` (apply a manifest or `kubectl edit providers`). Crossplane creates a new `ProviderRevision` so deprecated CRDs persist until you decide otherwise.

```shell
kubectl get providerrevisions
```

Only one revision is `Active`; by default one Inactive revision is kept (`revisionHistoryLimit`).

Provider conditions:

- `Installed`: True with `ActivePackageRevision`; False with `InactivePackageRevision`.
- `Healthy`: True with `HealthyPackageRevision` (normal); False with `UnhealthyPackageRevision`; Unknown with `UnknownPackageRevisionHealth`.

Stuck states: run `kubectl describe providerrevisions`.

Removing a Provider with `kubectl delete provider` before deleting its managed resources can abandon them. The external resources are not deleted, so you must delete them in your cloud console, and the MRs need their finalizers removed by hand. Delete the managed resources first.

Enabling automatic dependency downgrades (`packageManager.enableAutomaticDependencyDowngrade=true`, needs `--enable-dependency-version-upgrades`) can leave orphaned MRs, lose data from omitted CRD fields, or change storage versions.

Change `revisionHistoryLimit` to control how many inactive revisions Crossplane keeps (`0` disables storing revisions).

## Checked

2026-11-03. Confirmed against the Crossplane docs (Providers page, docs.crossplane.io/latest): the field names, values, defaults and behaviours stated above. Removed or reworded: the rollback claim.

Method: documentation only; no commands were run.
