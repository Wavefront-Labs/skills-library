---
id: computing-software.search-and-information-retrieval.elasticsearch-opensearch.snapshot-create-restore
name: snapshot-create-restore
category: computing-software
field: search-and-information-retrieval
product: elasticsearch-opensearch
tags: [search-and-information-retrieval, elasticsearch-opensearch, elasticsearch, opensearch, snapshot-create-restore]
level: practitioner
status: docs-checked
description: "Take OpenSearch snapshots of indices or data streams and restore them with rename patterns, index_settings overrides and global state control."
sources:
  - https://docs.opensearch.org/latest/api-reference/snapshots/create-snapshot/
  - https://docs.opensearch.org/latest/api-reference/snapshots/restore-snapshot/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create and restore snapshots

**Goal:** back up and recover. Checked against the OpenSearch pages; Elasticsearch uses the same `_snapshot` paths but its pages were not checked.
- Create: `PUT _snapshot/<REPOSITORY>/<SNAPSHOT>` (or `POST`) with an optional body `{"indices":"logs-*,-logs-2016","ignore_unavailable":true,"include_global_state":false,"partial":false,"metadata":{"reason":"pre-upgrade"}}`. The name must be unique in the repository; date math names need URL encoding.
- `wait_for_completion` defaults to `false`: the call returns `{"accepted": true}` once the snapshot starts (it can still take a while in a large repository).
- Snapshots are incremental: only index files not already in the repository are copied. Indexing and search continue, and documents indexed after the start are not included.
- Defaults: all open indexes and data streams, including hidden ones; closed indexes only if named in `indices`. `include_global_state` defaults to `true` on create (persistent cluster settings, index templates, legacy templates, ingest pipelines; not transient settings or repositories). `partial` defaults to `false`, so a missing primary shard fails the snapshot. `metadata` must be under 1,024 bytes.
- Restore: `POST _snapshot/<REPOSITORY>/<SNAPSHOT>/_restore` with `{"indices":"logs-1","rename_pattern":"(.+)","rename_replacement":"restored-$1","include_aliases":false}`. `wait_for_completion` also defaults to `false`.
- An open index with the same name must be closed, deleted or renamed first. A closed index can be restored over only if it has the same shard count; the restore reopens it.
- `include_global_state` defaults to `false` on restore; when `true`, snapshot cluster-state items replace existing items of the same names. ISM policies live in an index, not cluster state, so they are not restored this way.
- `index_settings` (for example `{"index.number_of_replicas":0}`) overrides settings; `ignore_index_settings` resets listed ones to defaults. Some settings, such as `index.number_of_shards`, cannot be changed during a restore, and `index.number_of_replicas` cannot be excluded.
- `storage_type`: `local` (default) or `remote_snapshot`, which needs at least one node with the `warm` role.
- Renaming a data stream renames its backing indexes; make sure an index template matches the new name or it cannot roll over.

## Verify
- [ ] Restored index `_count` equals the original; run restore drills regularly.

## Checked

Checked 2026-11-08 against the OpenSearch Create Snapshot API and Restore Snapshot API pages. Confirmed: every parameter, default and restriction above. Removed: the `_status` monitoring call (not on these pages) and the page-root sources.

Method: documentation only; no commands were run.
