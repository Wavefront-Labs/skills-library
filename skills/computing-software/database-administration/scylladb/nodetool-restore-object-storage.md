---
id: computing-software.database-administration.scylladb.nodetool-restore-object-storage
name: nodetool-restore-object-storage
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, restore, object-storage, load-and-stream, scope, backup]
level: advanced
status: docs-checked
description: "nodetool restore from object storage: endpoint, bucket, prefix, TOC component keys, --scope node/rack/dc/all, --sstables-file-list, --primary-replica-only, full restore planning."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/restore.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool restore from object storage

Loads SSTables from a bucket into a keyspace and table. It always runs as a background task, and the status is kept for `user_task_ttl` (set with `nodetool tasks user-ttl`). Without `--nowait` the command waits and returns the final status, which fails to report if the TTL is too low (0); with `--nowait` it prints a task ID to monitor or cancel via `nodetool tasks`.

```
nodetool restore --endpoint s3.us-east-2.amazonaws.com --bucket bucket-foo --prefix ks/cf/24601 \
  --keyspace ks --table cf \
  scylla/ks/cf/34/me-3gdq_0bki_2dy4w2gqj6hoso4mw1-big-TOC.txt
```

Options:
- `--endpoint`, `--bucket`, `--prefix`: where the backup lives (endpoint must be configured).
- `--keyspace`, `--table`: destination.
- `--scope`: where the data is loaded: `node`, `rack`, `dc` or `all` (default, everywhere in the cluster).
- `--primary-replica-only`: stream only to the primary replica; a repair is needed afterwards.
- `--sstables-file-list <file>`: newline-separated TOC keys; can be combined with positional TOC keys (duplicates are not removed).
- Positional `<sstables>`: TOC component keys relative to the prefix.

Planning a full restore: combine `--scope` with the right SSTable list per node. At one extreme a single node receives every SSTable with scope `all`; at the other each node restores only its own SSTables with scope `node`. Rack and DC scopes sit in between.

## Checked

2026-11-04: task behaviour, options, scope values and the full-restore planning note confirmed against the ScyllaDB nodetool restore documentation page.

Method: documentation only; no commands were run.
