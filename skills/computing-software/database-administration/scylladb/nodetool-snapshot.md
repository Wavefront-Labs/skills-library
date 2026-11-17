---
id: computing-software.database-administration.scylladb.nodetool-snapshot
name: nodetool-snapshot
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, snapshot, backup, hardlinks, ttl]
level: practitioner
status: docs-checked
description: "nodetool snapshot syntax and options: keyspace and table selection, -t tag, -sf skip flush, --ttl, cluster snapshot, and where hard-linked snapshots live on disk."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/snapshot.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/backup.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool snapshot

Creates a point-in-time snapshot of keyspaces or one table on the node you run it on. Prefix `cluster` (`nodetool cluster snapshot`) to snapshot on all nodes.

Options:
- `-t <tag>` / `--tag`: snapshot name (default is a timestamp such as `1564577645291`).
- `-cf` / `--column-family` / `--table <table>`: one table, only with exactly one keyspace; may be a table, materialized view or index (for an index use the backing view name).
- `-kc <list>` / `--kc.list`: comma-separated keyspaces.
- `-sf` / `--skip-flush`: do not flush memtables first, so unflushed data is not in the snapshot.
- `--ttl <ttl>`: lifetime with suffix `s` (default), `m`, `h` or `d`; missing or 0 means keep forever.
- Positional keyspaces; default is all.

```
nodetool snapshot mykeyspace
nodetool snapshot -kc mykeyspace,yourkeyspace
nodetool snapshot --table heartrate -t before-upgrade --ttl 7d mykeyspace
```

Location: `<data dir>/<keyspace>/<table>-<uuid>/snapshots/<tag>/`, containing hard links to the SSTable files plus `manifest.json`. Over time, as SSTables are compacted, the original files stay hard-linked from the snapshot directories, so snapshots hold an increasing amount of disk space.

## Checked

2026-11-04: syntax, options, defaults, examples and snapshot location confirmed against the ScyllaDB nodetool snapshot page; the growing disk usage note against the backup procedure page. Removed the clearsnapshot and listsnapshots mentions the pages do not cover.

Method: documentation only; no commands were run.
