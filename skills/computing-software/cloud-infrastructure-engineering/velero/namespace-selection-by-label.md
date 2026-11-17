---
id: computing-software.cloud-infrastructure-engineering.velero.namespace-selection-by-label
name: namespace-selection-by-label
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [includednamespacesbylabel, excludednamespacesbylabel, labelselectorlogic, dynamic-namespaces, namespace-labels]
level: sme
status: docs-checked
description: "Pick backup namespaces dynamically by label with includedNamespacesByLabel and excludedNamespacesByLabel, including precedence and AND logic."
sources:
  - https://velero.io/docs/main/resource-filtering/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Inside `includeExcludePolicy` (backup only), two lists of Kubernetes label selector strings choose whole namespaces by their labels:

```yaml
version: v1
includeExcludePolicy:
  includedNamespacesByLabel:
    - "velero-backup-schedule=weekly"
    - "team=platform"
  excludedNamespacesByLabel:
    - "confidential=true"
```

`excludedNamespacesByLabel` always wins. By default list entries are OR-ed; `labelSelectorLogic: "AND"` requires a namespace to match every entry (one setting for both lists). A single entry like `"tier=critical,compliance=pci"` already expresses AND.

Precedence:
- `BackupSpec.IncludedNamespaces` empty: label matches replace the "all namespaces" default. No match means nothing selected.
- Explicit list set: label matches are unioned with it.
- Explicit `*` is preserved as is.
- `--selector` still filters individual resources only.

Selectors are evaluated once when the backup starts; resolved names are written into the Backup `spec.includedNamespaces`. No match shows the placeholder `[-]*`.

Limitations: not usable for Restore, not honoured in `--global-backup-volume-policies-configmap`, empty selector strings are rejected. Narrowing from all namespaces also stops cluster-scoped resources by default, so set `includeClusterResources: true` if you need CRDs or ClusterRoles.

## Checked

Checked 2026-11-08 against the Velero Resource filtering page (raw markdown, read in full), section Namespace selection by label with its precedence and limitations. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
