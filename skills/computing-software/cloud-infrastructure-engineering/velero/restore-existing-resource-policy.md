---
id: computing-software.cloud-infrastructure-engineering.velero.restore-existing-resource-policy
name: restore-existing-resource-policy
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [existing-resource-policy, restore-update, non-destructive, serviceaccount-merge, restore-flags]
level: practitioner
status: docs-checked
description: "Control what a Velero restore does when a resource already exists, using --existing-resource-policy none or update."
sources:
  - https://velero.io/docs/main/restore-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a restore is non-destructive: if a resource already exists on the target cluster (as determined by the API on create), Velero skips it and changes nothing.

The exception is ServiceAccounts. Velero merges the backed-up ServiceAccount into the existing one: Secrets and ImagePullSecrets are appended, and missing labels and annotations are added while existing ones stay.

Change the behaviour per restore with `--existing-resource-policy`. Values: `none` (default) and `update`.

```bash
velero restore create --from-backup NAME --existing-resource-policy=update
```

With `update`, Velero tries to make the existing resource match the backup:
- If the existing resource equals the backed-up one, Velero adds labels `velero.io/backup-name` and `velero.io/restore-name`. If that patch fails it records a restore error and moves on.
- If it differs, Velero first patches the resource to match the backup, then adds the two labels. If the patch fails it records a restore warning and still tries to add the labels; if the label patch fails too, it logs a restore error and continues.

`update` is best effort and applies to Kubernetes resource data such as the spec. For PVCs it does not restore data into the PV; use the separate existing volume data policy for that. The policy can also be set in a Restore object.

## Checked

Checked 2026-11-08 against the Velero Restore Reference page ("Restore existing resource policy", read in full). Removed the unsourced `velero restore describe` advice and added the documented best-effort and PVC notes.

Method: documentation only; no commands were run.
