---
id: computing-software.cloud-infrastructure-engineering.velero.schedule-owner-references-gitops
name: schedule-owner-references-gitops
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [useownerreferencesinbackup, gitops, argocd, schedule-owner, orphaned-backups]
level: advanced
status: docs-checked
description: "Understand the useOwnerReferencesInBackup side effects when deleting a Velero schedule, and keep ArgoCD from pruning backups."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Backups created by a schedule can carry an owner reference to the schedule. The reference documents this flag:

```
velero schedule create --use-owner-references-in-backup <backup-name>
```

It is useful in some GitOps scenarios, or where the Kubernetes resource tree is synchronised from other places.

Side effect: when the schedule is deleted, the Kubernetes garbage collector deletes the related Backup custom resources too (only the CRs; backup data and snapshots stay in object storage). Velero then syncs those backups back from object-store metadata, so the GC controller and Velero keep fighting over whether they should exist. If the schedule may be disabled while its backups remain useful, do not enable this option.

ArgoCD options to stop it pruning day-2 backups:
- Annotate the schedule so it is ignored. Downside: deleting the schedule from the manifest will not delete it; do that manually.

```yaml
annotations:
  argocd.argoproj.io/compare-options: IgnoreExtraneous
  argocd.argoproj.io/sync-options: Delete=false,Prune=false
```

- If ArgoCD is deployed by ArgoCD-Operator, set `spec.resourceExclusions` to exclude kinds `Backup` and `Restore` in apiGroup `velero.io` for clusters `"*"`.

## Checked

Checked 2026-11-08 against the Velero Backup Reference page ("Backup's OwnerReference with Schedule", read in full): the flag, GC side effect, and both ArgoCD options. Removed the `spec.useOwnerReferencesInBackup` YAML field name and the cron example, which the page does not show.

Method: documentation only; no commands were run.
