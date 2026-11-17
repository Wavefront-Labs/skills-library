---
id: computing-software.database-administration.dragonfly.dflycluster-slot-migration-status
name: dflycluster-slot-migration-status
category: computing-software
field: database-administration
product: dragonfly
tags: [slot-migration, dflycluster-slot-migration-status, rebalancing, cluster-mode]
level: advanced
status: docs-checked
description: "Check in-progress and finished hash slot migrations on a Dragonfly node with DFLYCLUSTER SLOT-MIGRATION-STATUS and read its states."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/cluster-management/dflycluster-slot-migration-status.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax:

```
DFLYCLUSTER SLOT-MIGRATION-STATUS [node_id]
```

With a `node_id` it shows migrations between the current node and that node; without it, all migrations on the node. ACL categories: `@admin`, `@slow`.

Each migration entry contains, in order:

1. direction: `in` or `out`
2. the `node_id` of the migration
3. state: `CONNECTING`, `SYNC`, `ERROR`, `FINISHED` or `FATAL`
4. number of keys for the selected slots on the current node
5. error status: `0` when no error, otherwise the last error description
6. slot ranges as a string

Example output:

```shell
dragonfly> DFLYCLUSTER SLOT-MIGRATION-STATUS
1) 1) "out"
   2) "133807dea9b616400e22587b99abd87a1cbf6473"
   3) "FINISHED"
   4) (integer) 4
   5) "0"
   6) "[3000, 9000]"
```

Meaning: the node finished migrating four keys in slots 3000 through 9000 out.

Poll on both source and target; treat `ERROR` or `FATAL` as needing the error text investigated. Dragonfly itself does not orchestrate migration; a control plane does.

## Checked

2026-11-04. Confirmed in the DFLYCLUSTER SLOT-MIGRATION-STATUS page (syntax, ACL categories, fields in order, states, example) and the Cluster Mode page (no control plane in the server). Nothing removed.

Method: documentation only; no commands were run.
