---
id: computing-software.cloud-infrastructure-engineering.velero.include-exclude-policy
name: include-exclude-policy
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [includeexcludepolicy, includedclusterscopedresources, reusable-filters, failedvalidation, excludednamespacescopedresources]
level: advanced
status: docs-checked
description: "Reuse scoped include and exclude filters across backups with includeExcludePolicy, and how backup spec filters override it."
sources:
  - https://velero.io/docs/main/resource-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`includeExcludePolicy` stores scoped include/exclude filters in a resource policies ConfigMap so many backups can share them. Backup only.

```yaml
version: v1
includeExcludePolicy:
  includedClusterScopedResources:
    - "crd"
  excludedClusterScopedResources: []
  includedNamespaceScopedResources: []
  excludedNamespaceScopedResources:
    - "configmap"
    - "event"
```

Using it:

```bash
velero backup create NAME --resource-policies-configmap my-policy --include-namespaces my-workload-ns
```

That backs up everything in `my-workload-ns` except configmaps and events, plus all CRDs.

Limits:
- It does not work with `--include-resources`, `--exclude-resources` or `--include-cluster-resources`. Combining them makes the backup fail with status `FailedValidation`.
- Entries cannot be `*`; list specific resources only.

It does combine with the scoped flags. Filters in the Backup spec have higher priority, so:

```bash
velero backup create NAME --resource-policies-configmap my-policy \
  --include-namespace-scoped-resources "*" --include-cluster-scoped-resources apiservices \
  --include-namespaces my-workload-ns
```

includes configmaps and events (the spec overrides the policy) plus CRDs and apiservices.

## Checked

Checked 2026-11-08 against the Velero Resource filtering page (raw markdown, read in full), sections IncludeExcludePolicy, its limitations and the comparison with Backup Spec filters. Removed the unsourced paragraph about team configuration, Git and Schedules.

Method: documentation only; no commands were run.
