---
id: computing-software.database-administration.elasticsearch.snapshot-restore-and-ilm
name: snapshot-restore-and-ilm
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, opensearch, snapshot, restore, index-lifecycle-management, ilm, rollover, snapshot-repository, slm, disaster-recovery, searchable-snapshots]
level: advanced
status: docs-checked
description: "Set up snapshot repositories and restore correctly, and use ILM to automate rollover, shrink, and retention instead of hand-rolled index deletion scripts."
sources:
  - https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore
  - https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore/create-snapshots
  - https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore/restore-snapshot
  - https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore/searchable-snapshots
  - https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/rollover
  - https://www.elastic.co/docs/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Elasticsearch snapshots, restore, and index lifecycle management

**Goal:** have a snapshot strategy that actually restores cleanly under
disaster-recovery pressure, and let ILM manage index age/size instead of a cron
job doing `DELETE` on a date-matched index name.

## 1. Snapshots are deduplicated and repository-bound
```
PUT _snapshot/my_repo
{ "type": "s3", "settings": { "bucket": "<bucket>" } }
PUT _snapshot/my_repo/<snapshot-name>
```
Snapshots are automatically deduplicated: segments are immutable, so a snapshot copies
only segments created since the repository's last snapshot. Each snapshot is still
logically independent: deleting a snapshot removes only segments used exclusively by it.
A snapshot is the only reliable and supported backup; copying node data directories is not.
**Do not modify anything inside the repository, or run processes that interfere with it**
(for example storage lifecycle rules deleting "old" objects): future snapshot or restore
operations may report corruption or appear to succeed while silently losing data. Delete
snapshots only through Elasticsearch.

## 2. Use SLM, not cron, to manage snapshot lifecycle
Snapshot Lifecycle Management (SLM) policies take snapshots on a schedule and can delete
snapshots by retention rules (`expire_after`, `min_count`, `max_count`), all through
Elasticsearch. The retention task runs on the `slm.retention_schedule` cluster setting, and
`POST _slm/_execute_retention` runs it immediately.

## 3. Restore mechanics
```
POST _snapshot/my_repo/<snapshot-name>/_restore
{ "indices": "logs-2026.10.*", "rename_pattern": "(.+)", "rename_replacement": "restored-$1" }
```
- You cannot restore an existing open index. Either delete it first (stop indexing
  meanwhile) or rename on restore as above, which is the way to compare existing data with
  historical data. Ensure capacity for both copies.
- An existing index can be restored only if closed and with the same number of primary shards.
- Restoring a single backing index of a data stream does not add it to any existing data stream.
- Do not assume an index restored under a new name is wired back into your read/write
  aliases or data streams; check after the restore.
- Use `index_settings` in the restore request to override settings such as
  `index.number_of_replicas`.

## 4. ILM phases: rollover and the initial index
```
PUT _ilm/policy/logs-policy
{ "policy": { "phases": {
  "hot":   { "actions": { "rollover": { "max_primary_shard_size": "50gb", "max_age": "7d" } } },
  "warm":  { "min_age": "7d",  "actions": { "shrink": { "number_of_shards": 1 }, "forcemerge": { "max_num_segments": 1 } } },
  "cold":  { "min_age": "30d", "actions": { "searchable_snapshot": { "snapshot_repository": "my_repo" } } },
  "delete":{ "min_age": "90d", "actions": { "delete": {} } }
}}}
```
- The rollover action belongs in the hot phase, runs when any condition is met, and an
  empty write index is not rolled over (even past `max_age`) unless the policy sets
  `min_docs: 0`.
- For new projects Elastic recommends data streams, which need no extra rollover
  configuration. The alias-based approach needs `index.lifecycle.rollover_alias` set to the
  alias and the index to be that alias's write index (`"is_write_index": true`), and
  requires bootstrapping the initial index yourself. A policy on an index outside that setup
  does not roll over.
- After rollover, `min_age` is counted from the rollover time, not the index creation date.
- `shrink` fails if the index already has one primary shard; `forcemerge` in the hot phase
  requires `rollover` in the policy.

## 5. Searchable snapshots for cold and frozen tiers
The `searchable_snapshot` action (phases hot, cold, frozen) converts an index into a
searchable snapshot. In cold it is fully mounted (shards fully cached in the cluster);
in frozen it is partially mounted, using a fixed-size shared cache on frozen-tier nodes and
fetching missing data from the repository, which makes some searches slower. Searchable
snapshot data is read-only. ILM's delete action removes the searchable snapshot by default
(`delete_searchable_snapshot`), but not if you delete the index manually before the delete
phase: then remove it with the delete snapshots API.

## Verify
- [ ] SLM, not a manual script, manages snapshot creation and pruning.
- [ ] A full restore into a renamed scratch index has actually been tested, not just "the snapshot completed."
- [ ] ILM-managed indices are confirmed attached to their rollover alias/data stream before relying on automatic phase transitions.
- [ ] Repository storage is never changed by anything other than Elasticsearch.
- [ ] Cold/frozen tier latency expectations were set before moving query-sensitive data there.

## Checked
2026-11-09. Confirmed against the Elastic docs-content pages (snapshot and restore, create
snapshots, restore snapshot, searchable snapshots, rollover, time-series-without-data-streams
tutorial) and the elasticsearch repo ILM action pages (rollover, shrink, forcemerge,
searchable-snapshot, delete): deduplication, SLM retention fields, restore rules, rollover
conditions and alias setup, action phases and field names. Removed or rewritten: the claim that
later snapshots fail to restore if an intermediate snapshot is deleted through Elasticsearch
(docs say each snapshot is logically independent); the claim that ILM policies and aliases are
not reapplied on restore (not stated); the claim that restore is incremental against local data;
"dramatically cheaper" and cold tier mounting without local copies (cold is fully mounted);
the old guide URLs and the `snap-2026-10-15` style names.
Method: documentation only; no commands were run.
