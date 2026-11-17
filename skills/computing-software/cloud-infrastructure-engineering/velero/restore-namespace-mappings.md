---
id: computing-software.cloud-infrastructure-engineering.velero.restore-namespace-mappings
name: restore-namespace-mappings
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [namespace-mappings, restore-create, from-backup, claimref, namespace-remap]
level: intro
status: docs-checked
description: "Restore resources into different namespaces with --namespace-mappings old:new and know how PV claimRef is remapped."
sources:
  - https://velero.io/docs/main/restore-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Restore into different namespaces with `--namespace-mappings`:

```bash
velero restore create <RESTORE_NAME> \
  --from-backup <BACKUP_NAME> \
  --namespace-mappings old-ns-1:new-ns-1,old-ns-2:new-ns-2
```

Mappings are comma-separated `old:new` pairs.

What Velero changes:
- Before creating a resource it makes sure the target namespace exists, and creates it if it does not.
- It updates the namespace of each resource to the mapped one.
- For a PersistentVolume it rewrites `Spec.ClaimRef.Namespace` from the old to the new namespace.
- If the PV already exists on the target cluster and its claim namespace is remapped, Velero restores it under a new name, `velero-clone-` plus a random UUID, and keeps the original name in the annotation `velero.io/original-pv-name`.

Resources restored get the labels `velero.io/backup-name` and `velero.io/restore-name`, which helps you identify what a restore created.

If you restore a PV's PVC into its original namespace without remapping and the PVC already exists there, the PV creation fails with an `Already Exist` error from the Kubernetes API server.

## Checked

Checked 2026-11-08 against the Velero Restore Reference page ("Restoring into a different namespace", the restore workflow and "Persistent Volume Rename", read in full). Removed unsourced claims: "several mappings in a single restore" wording beyond the shown example, the same-cluster cloning remark and the typical-use paragraph.

Method: documentation only; no commands were run.
