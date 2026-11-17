---
id: computing-software.database-administration.elasticsearch.path-data-path-repo-path-logs
name: path-data-path-repo-path-logs
category: computing-software
field: database-administration
product: elasticsearch
tags: [database-administration, elasticsearch, path-data, path-repo, path-logs, elasticsearch-setup, storage]
level: practitioner
status: docs-checked
description: "Set Elasticsearch path.data, path.logs and path.repo for production, avoid multiple data paths, register shared filesystem repositories, and move data safely."
sources:
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/path.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/fs-repository-settings.md
  - https://github.com/elastic/elasticsearch/blob/main/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# path.data / path.repo / path.logs

**Goal:** data and logs on the right volumes, outside the install directory so upgrades do not wipe them, and snapshot repositories allowed explicitly.

## Settings
```yaml
path.data: /var/lib/elasticsearch          # DEB/RPM/Docker write outside $ES_HOME; archive installs default to $ES_HOME/data
path.logs: /var/log/elasticsearch
path.repo: ["/mnt/es-snapshots"]           # required to register fs repositories
```
Archive (`.tar.gz`/`.zip`) installs default `data` and `logs` to subdirectories of `$ES_HOME`, where files risk deletion during an upgrade. Always set explicit paths outside it. Do not modify the data directory, run virus scanners on it, or take filesystem backups of it (there is no supported restore for those; use snapshots).

## Single data path
Multiple data paths (`path.data: [/d1, /d2]`) are deprecated since 7.13 and will be removed in a future release; Elasticsearch keeps each shard's data on one path. Use a single path on a filesystem spanning disks (RAID, LVM, Storage Spaces), or run more nodes with a path each. In a highly available cluster you can migrate without downtime using allocation filters; otherwise snapshot and restore into a new cluster.

## Shared filesystem snapshots
1. Mount the same NFS share at the same path on **every** master and data node.
2. Add it (or a parent directory) to `path.repo` on all of them (a static setting, so rolling-restart).
3. Register:
```json
PUT _snapshot/nfs_backups
{ "type": "fs", "settings": { "location": "/mnt/es-snapshots/prod" } }
```
4. `POST _snapshot/nfs_backups/_verify` checks every node can write.

## Moving data to a new disk
Add a new node with the new disk and drain the old one with an allocation filter, which needs no downtime; do not copy the data directory with filesystem tools.

## Gotchas
- Ownership: the `elasticsearch` user must own the directories; containers often fail with `AccessDeniedException`.
- Never let two nodes share the same `path.data`.
- Disk watermarks default to 85% (low), 90% (high) and 95% (flood stage), with headroom caps on large disks; monitor `GET _cat/allocation?v`.
- If you register the same `fs` repository with several clusters, only one should have write access.

## Verify
`GET _nodes/settings?filter_path=**.path` shows intended paths on each node; `_verify` on the repository succeeds.

## Checked

Checked 2026-10-25 against elastic/elasticsearch `main` docs (Stack 9.x). Confirmed: archive installs default `data`/`logs` under `$ES_HOME` and DEB/RPM/Docker do not; multiple data paths deprecated in 7.13 with migration guidance; no filesystem backups, no virus scanners; `path.repo` is static, must be on every master and data node, and `location` must be under it; `compress` default true; disk watermark defaults. Removed the unsupported `rsync` data-move procedure and the "per data path" watermark claim. The `_verify` endpoint and `_nodes/settings` filter_path were not re-read.

Method: documentation only; no commands were run.
