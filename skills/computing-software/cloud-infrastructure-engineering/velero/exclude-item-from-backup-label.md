---
id: computing-software.cloud-infrastructure-engineering.velero.exclude-item-from-backup-label
name: exclude-item-from-backup-label
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [exclude-from-backup, label, velero-io-exclude-from-backup, item-exclusion, kubectl-label]
level: intro
status: docs-checked
description: "Exclude a single resource from every Velero backup by labelling it velero.io/exclude-from-backup=true, even if selectors match it."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can exclude an individual item from backups even when it matches the resource, namespace or label selectors defined in the backup spec. Label the item:

```bash
kubectl label -n <ITEM_NAMESPACE> <RESOURCE>/<NAME> velero.io/exclude-from-backup=true
```

Example for a Secret that should never be captured:

```bash
kubectl label -n app secret/db-password velero.io/exclude-from-backup=true
```

The label wins over the include selectors. If you need exclusion by type or namespace instead of by object, use the exclude filters described on the resource filtering page.

## Checked

Checked 2026-11-08 against the Velero Backup Reference page ("Exclude Specific Items from Backup", read in full) and the Resource filtering page (`velero.io/exclude-from-backup=true` section, page read in full as raw markdown). Removed unsourced claims: cluster-scoped namespace-flag advice, the use-case list, the label-removal command and the schedule-template paragraph.

Method: documentation only; no commands were run.
