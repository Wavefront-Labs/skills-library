---
id: computing-software.database-administration.scylladb.nodetool-drain-and-compact
name: nodetool-drain-and-compact
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, drain, compact, major-compaction, maintenance]
level: practitioner
status: docs-checked
description: "nodetool drain (flush and stop listening, restart required) vs flush, and nodetool compact major compaction semantics, unsupported options, and why to avoid it in production."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/drain.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/compact.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool drain and nodetool compact

**drain** flushes all memtables to SSTables and makes ScyllaDB stop listening for client and node connections. The process must be restarted afterwards. Run it before upgrading a node or other maintenance. If you only want memtables on disk, use `nodetool flush` instead.

```
nodetool drain
```

**compact** forces a major compaction:

```
nodetool compact
nodetool compact keyspace1
nodetool compact keyspace1 standard1
```

Behaviour:
- No arguments: all keyspaces and tables.
- With a keyspace, all its tables; with table names, only those.
- For each table, all SSTables are merged into a single SSTable per shard.

Not implemented in ScyllaDB (present in the Cassandra tool): `-st`/`--start-token`, `-et`/`--end-token`, `--user-defined`, `--split-output`.

Major compactions are not recommended for production: they can exhaust CPU, IO and disk and raise cost. Let the table compaction strategy run minor compactions automatically. Related controls: `nodetool setcompactionthroughput`, `disableautocompaction` and `compactionstats`.

## Checked

2026-11-04. Confirmed against drain.rst and compact.rst: drain behaviour and restart, flush alternative, compact examples, scope, single SSTable per shard, the four unimplemented options, the caution against major compaction. The related commands setcompactionthroughput, disableautocompaction and compactionstats exist as pages in the nodetool-commands directory. Removed the claim that flush leaves the node serving.

Method: documentation only; no commands were run.
