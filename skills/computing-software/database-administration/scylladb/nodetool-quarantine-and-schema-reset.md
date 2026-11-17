---
id: computing-software.database-administration.scylladb.nodetool-quarantine-and-schema-reset
name: nodetool-quarantine-and-schema-reset
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, dropquarantinedsstables, resetlocalschema, sstable-corruption, schema-disagreement]
level: advanced
status: docs-checked
description: "nodetool dropquarantinedsstables (data resurrection risk, replace node instead) and nodetool resetlocalschema to fix schema version disagreement without a restart."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/dropquarantinedsstables.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/resetlocalschema.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool dropquarantinedsstables and resetlocalschema

**dropquarantinedsstables** deletes quarantined SSTables (those moved to a `quarantine` directory by a scrub in VALIDATE mode) from the given keyspace and tables, or from all keyspaces when none is given.

Warning from the docs: dropping them can resurrect deleted data regardless of consistency level and of the `repair` tombstone GC mode. The only supported way to rid a node of corrupt data is to replace the node; use this command only when no viable alternative remains. The command is rejected unless you pass the acknowledgement flag:

```
nodetool dropquarantinedsstables --i-accept-data-resurrection-risk
nodetool dropquarantinedsstables --i-accept-data-resurrection-risk mykeyspace mytable
```
Arguments: optional `<keyspace>` (default all) and optional `<table...>` (default all tables in the keyspace).

**resetlocalschema** reloads the in-memory schema objects from disk and recalculates the per-node and per-table schema versions. It can fix some schema version disagreements that would otherwise need a node restart.

```
nodetool resetlocalschema
```

It is not a way to hot-load schema from manually placed schema SSTables: if the schema on disk does not match the in-memory schema, the reload will likely fail.

## Checked

2026-11-04. Confirmed against dropquarantinedsstables.rst, resetlocalschema.rst and scrub.rst (quarantine directory created by VALIDATE mode): warning text, acknowledgement flag, arguments and defaults, resetlocalschema behaviour and limitation. Removed the advice about which node to run it on.

Method: documentation only; no commands were run.
