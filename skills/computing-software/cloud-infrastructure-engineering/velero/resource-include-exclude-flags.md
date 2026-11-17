---
id: computing-software.cloud-infrastructure-engineering.velero.resource-include-exclude-flags
name: resource-include-exclude-flags
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [include-resources, exclude-resources, include-namespaces, resource-filtering, resource-group]
level: practitioner
status: docs-checked
description: "Filter a Velero backup or restore by namespace and resource type with the include and exclude flags, including the wildcard rules."
sources:
  - https://velero.io/docs/main/resource-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With no filters, Velero includes everything. Includes mean only the listed items are used; excludes remove items.

- `--include-namespaces`: default `*`. Accepts globs. `velero backup create NAME --include-namespaces ns1`.
- `--exclude-namespaces`: `velero backup create NAME --exclude-namespaces kube-system`.
- `--include-resources`: formatted `resource.group`, for example `storageclasses.storage.k8s.io`; `*` means all.
- `--exclude-resources`: `velero backup create NAME --exclude-resources secrets,rolebindings`.

Restore accepts the same flags: `velero restore create --from-backup NAME --include-resources deployments,configmaps`.

Rules:
- If a wildcard and a specific resource are both included, the wildcard takes precedence.
- Wildcard excludes are ignored.
- `--include-resources` and `--exclude-resources` cannot be combined with `--include-cluster-scoped-resources`, `--exclude-cluster-scoped-resources`, `--include-namespace-scoped-resources` or `--exclude-namespace-scoped-resources`.
- A resource labelled `velero.io/exclude-from-backup=true` is excluded even when it matches a selector.

Combine them to narrow:

```bash
velero backup create NAME --include-resources deployments --include-namespaces ns1
```

## Checked

Checked 2026-11-08 against the Velero Resource filtering page (raw markdown, read in full): Includes, Excludes and the `velero.io/exclude-from-backup=true` sections. Removed the unsourced closing advice paragraph.

Method: documentation only; no commands were run.
