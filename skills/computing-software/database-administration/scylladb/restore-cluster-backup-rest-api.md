---
id: computing-software.database-administration.scylladb.restore-cluster-backup-rest-api
name: restore-cluster-backup-rest-api
category: computing-software
field: database-administration
product: scylladb
tags: [restore, cluster-backup, tablets, rest-api, storage-service]
level: advanced
status: docs-checked
description: "Restore a nodetool cluster backup into a tablet table via POST /storage_service/tablets/restore: query params, per-DC JSON body with manifests, monitoring with nodetool tasks."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/backup-restore/restore.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Restore a cluster backup (REST API)

For backups made with `nodetool cluster backup` into a tablet-based table. It runs as a topology operation: each tablet replica downloads the SSTables of its tablets directly from object storage and attaches them, so no data streams between nodes. Data stored as a single repaired copy is restored to every replica it was taken from.

Requirements:
- The object storage endpoint is configured on the nodes.
- The destination table exists and uses tablets (a vnode table fails). Recreate keyspace and table from the schema backup, since the backup holds only SSTables and manifests.
- No nodetool command exists yet, so use the REST API.

Request: `POST /storage_service/tablets/restore` with query parameters `keyspace`, `table`, `snapshot`, and a JSON array body with one entry per DC the keyspace replicates to:

```
curl -X POST -H 'Content-Type: application/json' \
  'http://<node>:10000/storage_service/tablets/restore?keyspace=mykeyspace&table=team_roster&snapshot=mysnapshot' \
  -d '[{"datacenter":"mydc","endpoint":"s3.us-east-2.amazonaws.com","bucket":"bucket-foo",
        "prefix":"backups/mysnapshot",
        "manifests":["snapshots/mykeyspace/team_roster/mysnapshot/manifest.json"]}]'
```
`manifests` are paths relative to the prefix. The call returns a task ID.

Monitor with `nodetool tasks wait <task ID>` or `nodetool tasks status <task ID>`.

A replica that is down cannot restore its tablets, so the restore fails instead of waiting. Bring the node back or remove it from the cluster, then run the restore again.

## Checked

2026-11-09. Confirmed the endpoint path, query parameters, per-datacenter body fields, example, task monitoring and down-replica behaviour against the ScyllaDB restore procedure page (all sections read).

Method: docs-checked 2026-11-09 against the ScyllaDB docs page operating-scylla/procedures/backup-restore/restore.rst
