---
id: computing-software.cloud-infrastructure-engineering.velero.cluster-scoped-resource-filters
name: cluster-scoped-resource-filters
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [include-cluster-resources, include-cluster-scoped-resources, exclude-namespace-scoped-resources, scoped-filters, cluster-resources]
level: advanced
status: docs-checked
description: "Choose cluster-scoped inclusion with --include-cluster-resources true, false or auto, and use the four scoped include and exclude flags."
sources:
  - https://velero.io/docs/main/resource-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--include-cluster-resources` takes three values:
- `true`: all cluster-scoped resources included.
- `false`: none included.
- unset (nil, "auto"): included when backing up or restoring all namespaces (effective default true); not included when namespace filtering is used (effective default false). Related cluster-scoped items such as the PV behind an included PVC may still be captured by a custom action unless you set `false`.

```bash
velero backup create NAME --include-namespaces ns1 --include-cluster-resources=true
velero restore create --from-backup NAME --include-cluster-resources=false
```

The newer scoped flags are backup only (not restore) and take `resource.group` lists, with `*` for all:

```bash
--include-cluster-scoped-resources="storageclasses,clusterroles"
--exclude-cluster-scoped-resources="*"
--include-namespace-scoped-resources="deployments.apps,configmaps"
--exclude-namespace-scoped-resources="*"
```

Constraint: the include and exclude flags for cluster-scoped and namespace-scoped resources cannot work with `--include-resources`, `--exclude-resources` or `--include-cluster-resources` (and `--include-resources` / `--exclude-resources` cannot work with them). Pick one family per backup.

## Checked

Checked 2026-11-08 against the Velero Resource filtering page (raw markdown, read in full): the three values of `--include-cluster-resources` and their defaults, the four scoped flags, their backup-only scope and the incompatibility lists. Removed unsourced claims: the validation-failure wording, the use-case sentence, and the describe-based advice.

Method: documentation only; no commands were run.
