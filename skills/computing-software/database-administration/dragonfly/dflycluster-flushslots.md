---
id: computing-software.database-administration.dragonfly.dflycluster-flushslots
name: dflycluster-flushslots
category: computing-software
field: database-administration
product: dragonfly
tags: [dflycluster-flushslots, slot-flush, cluster-mode, dragonfly]
level: advanced
status: docs-checked
description: "Delete every key in a range of hash slots on one Dragonfly cluster node with DFLYCLUSTER FLUSHSLOTS, including its asynchronous semantics."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/command-reference/cluster-management/dflycluster-flushslots.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Syntax:

```
DFLYCLUSTER FLUSHSLOTS start_slot end_slot [start_slot end_slot ...]
```

Deletes all keys belonging to the given slot ranges on the node you run it on. Time complexity is O(N) where N is the total number of keys in the selected slots. ACL categories: `@slow`, `@admin`. It replies `OK` and never fails.

Behaviour:

- The delete is asynchronous.
- It only deletes keys that existed when the command was invoked; keys created during the asynchronous flush are unaffected.
- It acts on this node only, not the whole cluster.

Related flag: `--cluster_flush_decommit_memory` (default false) decommits memory after flushing slots.

Safety steps before running:

1. Confirm the slot ranges with `DFLYCLUSTER GETSLOTINFO`.
2. Confirm no migration involving them is in progress (`DFLYCLUSTER SLOT-MIGRATION-STATUS`).
3. Run on the admin port of the correct node.

## Checked

2026-11-04. Confirmed in the DFLYCLUSTER FLUSHSLOTS page (syntax, complexity, ACL categories, never fails, keys present at invocation, asynchronous flush) and the flags page (`cluster_flush_decommit_memory`, default false). Removed the FLUSHALL comparison, which the pages do not support (the compatibility page lists FLUSHALL as missing its ASYNC option).

Method: documentation only; no commands were run.
