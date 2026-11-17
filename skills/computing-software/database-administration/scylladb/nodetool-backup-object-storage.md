---
id: computing-software.database-administration.scylladb.nodetool-backup-object-storage
name: nodetool-backup-object-storage
category: computing-software
field: database-administration
product: scylladb
tags: [nodetool, backup, object-storage, s3, cluster-backup, task-manager]
level: advanced
status: docs-checked
description: "nodetool backup and nodetool cluster backup to S3-compatible object storage: --endpoint, --bucket, --prefix, --location per DC, --move-files, --nowait and user_task_ttl."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/nodetool-commands/backup.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# nodetool backup to object storage

`nodetool backup` copies SSTables from a keyspace snapshot to a bucket in object storage. The endpoint must be configured in the ScyllaDB object storage configuration first.

Single node:
```
nodetool backup --endpoint s3.us-east-2.amazonaws.com --bucket bucket-foo --prefix foo/bar/baz \
  --keyspace ks --table table --snapshot ss --move-files
```
Options: `--keyspace`, `--table`, `--snapshot` (source), `--endpoint` (name of a configured endpoint), `--bucket`, `--prefix`, `--nowait`, `--move-files`.

Whole cluster, `nodetool cluster backup`:
```
nodetool cluster backup --location mydc,s3.us-east-2.amazonaws.com,bucket-foo,foo/bar/baz \
  --keyspaces ks --table table --snapshot ss --move-files
```
- `--keyspaces`: repeat per keyspace; default is all keyspaces.
- `--table`: one table or a comma-separated list; requires exactly one keyspace.
- `--snapshot`: if it does not exist it is taken first.
- `--location <dc>,<endpoint>,<bucket>[,<prefix>]`: repeat once per DC.

Common flags:
- `--move-files` moves instead of copies: local files are deleted after upload.
- `--nowait` returns immediately with a task ID; otherwise the command waits and relies on `user_task_ttl`.
- Status can be checked for `user_task_ttl` seconds after completion; set the TTL with `nodetool tasks user-ttl`.

The matching command is `nodetool restore`.

## Checked

2026-11-04: syntax, options, the cluster backup --location form and the user_task_ttl note confirmed against the ScyllaDB nodetool backup documentation page. Removed the disk-space and TTL-too-low claims that the page does not make for backup.

Method: documentation only; no commands were run.
