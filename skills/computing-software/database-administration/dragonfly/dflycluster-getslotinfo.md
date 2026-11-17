---
id: computing-software.database-administration.dragonfly.dflycluster-getslotinfo
name: dflycluster-getslotinfo
category: computing-software
field: database-administration
product: dragonfly
tags: [dflycluster-getslotinfo, slot-info, key-count, tiered-bytes, dragonfly]
level: advanced
status: docs-checked
description: "Inspect key counts, reads, writes and memory per hash slot on a Dragonfly cluster node with DFLYCLUSTER GETSLOTINFO."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/cluster-management/dflycluster-getslotinfo.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax:

```
DFLYCLUSTER GETSLOTINFO SLOTS slot [slot ...]
```

Time complexity is O(N) in the number of slots given. ACL categories: `@admin`, `@slow`. It reports on the current node.

The reply is a nested list, one entry per slot, with:

- the slot number
- `key_count`
- `total_reads`
- `total_writes`
- `memory_bytes`

When a slot has data offloaded to SSD tiering, the entry also includes `tiered_bytes`, the bytes the slot holds on disk. The field is omitted for slots with no offloaded data.

Example:

```shell
dragonfly> DFLYCLUSTER GETSLOTINFO SLOTS 1 12
1) 1) (integer) 1
   2) "key_count"
   3) (integer) 1
   ...
```

Use it to see which slots are heavy before planning a rebalance or checking the effect of a migration.

## Checked

2026-11-04. Confirmed in the DFLYCLUSTER GETSLOTINFO page (syntax, complexity, ACL categories, example fields, `tiered_bytes`). Nothing removed apart from the admin-port-of-the-owner wording.

Method: documentation only; no commands were run.
