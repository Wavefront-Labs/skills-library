---
id: computing-software.database-administration.scylladb.backup-native-cluster
name: backup-native-cluster
category: computing-software
field: database-administration
product: scylladb
tags: [backup, native-backup, cluster-backup, tablets, object-storage]
level: advanced
status: docs-checked
description: "Native ScyllaDB backup to S3 or GCS: cluster snapshot plus cluster backup per DC location, single-copy storage of repaired tablet data, bucket layout, retries and --move-files."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/backup.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Native backup (cluster-wide)

With native backup ScyllaDB itself uploads the SSTables of a snapshot to S3-compatible storage (AWS S3 or Google Cloud Storage). The upload is scheduled and throttled inside the node, and no external tool needs access to the data directory. Configure the object storage endpoint on the nodes first. Only SSTables are uploaded; back up the schema separately.

Cluster-wide, from any node:

```
nodetool cluster snapshot --tag mysnapshot mykeyspace
nodetool cluster backup --location mydc,s3.us-east-2.amazonaws.com,bucket-foo,backups/mysnapshot \
  --snapshot mysnapshot --keyspaces mykeyspace
```
- The cluster snapshot is taken on all nodes and recorded in the `system_distributed` keyspace. If the snapshot does not exist, `cluster backup` takes it, so the first command is optional.
- Repeat `--location` for each DC the keyspace replicates to; each node uploads its own SSTables to its DC location.
- A part-way failure can be rerun with the same parameters; already uploaded SSTables are skipped.
- With `--move-files`, uploaded SSTables are deleted locally, but `manifest.json` and `schema.cql` remain until the snapshot is cleared.

Designed for tablet keyspaces: repaired data is stored as a single copy. SSTables covered by a tablet last repair are uploaded from one replica; unrepaired data is uploaded from every replica. The manifest records skipped replicas so a restore repopulates all of them. Run `nodetool cluster repair` before snapshotting to maximise this saving.

Layout under each location prefix: SSTables in `sstables/`, manifests at `snapshots/<keyspace>/<table>/<snapshot>/manifest.json`. Per-node alternative: `nodetool backup` with a node-specific prefix.

## Checked

2026-11-04: native backup description, cluster-wide commands, repeated --location, retry behaviour, --move-files, single-copy storage of repaired tablet data and the bucket layout confirmed against the ScyllaDB backup procedure page.

Method: documentation only; no commands were run.
