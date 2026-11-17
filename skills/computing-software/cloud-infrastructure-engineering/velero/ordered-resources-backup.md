---
id: computing-software.cloud-infrastructure-engineering.velero.ordered-resources-backup
name: ordered-resources-backup
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [ordered-resources, backup-order, orderedresources, backup-create, statefulsets]
level: advanced
status: docs-checked
description: "Back up specific resource kinds in a defined order with --ordered-resources, including its namespace/name and semicolon syntax."
sources:
  - https://velero.io/docs/main/backup-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `--ordered-resources` to back up resources of a given kind in a fixed order. The value is a mapping of Kind to an ordered list of resource names.

Syntax rules from the reference:
- The Kind name is plural (`pods`, `statefulsets`, `persistentvolumes`).
- Names within a Kind are separated by commas and written `namespace/resourcename`.
- Cluster-scoped resources use the bare resource name.
- Key-value pairs in the mapping are separated by semicolons.

Examples:

```bash
velero backup create backupName --include-cluster-resources=true --ordered-resources 'pods=ns1/pod1,ns1/pod2;persistentvolumes=pv4,pv8' --include-namespaces=ns1

velero backup create backupName --ordered-resources 'statefulsets=ns1/sts1,ns1/sts0' --include-namespaces=ns1
```

Quote the whole value, as in the examples, so the shell does not treat the semicolon as a command separator.

## Checked

Checked 2026-11-08 against the Velero Backup Reference page ("Specify Backup Orders of Resources of Specific Kind", read in full): option name, syntax rules and both example commands. Removed unsourced claims: the `orderedResources` YAML map example, the claim that other Kinds keep the default order, the use-case sentence and the describe verification step.

Method: documentation only; no commands were run.
