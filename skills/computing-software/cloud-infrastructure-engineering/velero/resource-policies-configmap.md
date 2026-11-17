---
id: computing-software.cloud-infrastructure-engineering.velero.resource-policies-configmap
name: resource-policies-configmap
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [resource-policies, resource-policies-configmap, resourcepolicy, volumepolicies, namespacedfilterpolicies]
level: advanced
status: docs-checked
description: "Create a resource policies ConfigMap and reference it from a Velero backup or restore, with the sections each operation supports."
sources:
  - https://velero.io/docs/main/resource-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resource policies define fine-grained filters and volume rules in a ConfigMap.

Step 1: create the ConfigMap in the Velero namespace from a YAML file (the file must start with `version: v1`):

```bash
kubectl create cm <configmap-name> --from-file <yaml-file> -n velero
```

Step 2: reference it.

```bash
velero backup create <backup-name> --resource-policies-configmap <configmap-name>
velero restore create <restore-name> --from-backup <backup-name> --resource-policies-configmap <configmap-name>
```

Or in the spec of a Backup, Restore or Schedule template:

```yaml
spec:
  resourcePolicy:
    kind: ConfigMap
    name: <configmap-name>
```

These combine with the normal include and exclude options.

Sections and where they apply:
- `namespacedFilterPolicies` and `clusterScopedFilterPolicy`: backup and restore.
- `volumePolicies`: backup only; actions `skip`, `snapshot`, `fs-backup`, `custom`.
- `includeExcludePolicy` (including `includedNamespacesByLabel`, `excludedNamespacesByLabel`, `labelSelectorLogic`): backup only.

A ConfigMap that holds backup-only sections is rejected when used for a restore.

Keep the ConfigMap in the same namespace as Velero and give it a descriptive name per purpose, such as one for volume rules and one for filters. Edits take effect for backups created afterwards; backups already taken keep the policy they ran with, so re-test after every change.

## Checked

2026-11-03. Read against the Velero docs (main): https://velero.io/docs/main/resource-filtering/. Confirmed the commands, flags, field names, defaults and limits stated above against those pages. Nothing was removed.

Method: documentation only; no commands were run.
