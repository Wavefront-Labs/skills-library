---
id: computing-software.database-administration.scylladb.nodetool-upgradesstables
name: nodetool-upgradesstables
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, upgradesstables, compression, encryption-at-rest, sstable-format]
level: practitioner
status: docs-checked
description: "nodetool upgradesstables: rewrite SSTables after compression or encryption changes, -a include-all, --jobs, keyspace and table targets, and when it is not needed."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/upgradesstables.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool upgradesstables

Rewrites SSTables of tables that are not on the latest format. It is not required when enabling the `mc` format or upgrading ScyllaDB: new SSTables are written in the new format at memtable flush or compaction, and old ones stay as they are. Use it when you change compression options, or encrypt or decrypt a table for encryption at rest, and want the rewrite now instead of waiting for compaction.

Syntax: `nodetool <generic options> upgradesstables [options] [keyspace [table ...]]`

- `--include-all-sstables` / `-a`: force upgrade of all SSTables, including those already in the new format.
- `--jobs <n>` / `-j <n>`: SSTables upgraded simultaneously; `0` uses all available compaction threads.
- `keyspace`: every table in it.
- keyspace followed by tables: just those tables (keyspace name first, then table names separated by spaces).
- `--`: separator between an option and its argument.

Examples with KeyspaceA (tableA, tableB old; tableE new):

```
nodetool upgradesstables KeyspaceA              # tableA and tableB only
nodetool upgradesstables KeyspaceA tableA
nodetool upgradesstables -a -- KeyspaceA        # forces tableE too
nodetool upgradesstables -a -- KeyspaceA KeyspaceB
```

## Checked

2026-11-04. Confirmed against nodetool-commands/upgradesstables.rst: purpose, mc format note, options -a and -j, keyspace and table targets, the -- separator, and all examples. Removed the unsupported advice to run node by node.

Method: documentation only; no commands were run.
