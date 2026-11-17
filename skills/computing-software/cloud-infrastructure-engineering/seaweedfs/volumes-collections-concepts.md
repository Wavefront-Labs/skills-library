---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.volumes-collections-concepts
name: volumes-collections-concepts
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [architecture, raft, volume, collection, master]
level: intro
status: docs-checked
description: "Understand SeaweedFS building blocks: masters (Raft), volume servers, filer, S3, volumes and collections, and why many buckets can exhaust disk."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# volumes collections concepts

Components:
- Master: cluster of 1, 3 or n/2+1 (always odd); a Raft-elected leader assigns file ids and picks volumes. Keep the count small.
- Volume server: packs many objects into large volume files and heartbeats to the leader. Replication is per volume, not per file.
- Filer (optional): paths over HTTP or FUSE.
- S3 (optional): AWS-style buckets.

Volume: one file holding many small files. The master sets the maximum size to 30GB by default (`-volumeSizeLimitMB`). Each volume has its own TTL and replication.

Collection: a group of volumes. TTL and replication belong to each volume, not the collection, so one collection can mix them. Deleting a collection just removes its volumes, which is fast. With S3, each bucket is a dedicated collection, so deleting a bucket is fast too.

Gotcha: a collection needs several volumes, and with 30GB each you can run out of disk quickly. Reduce the size, e.g. `weed master -volumeSizeLimitMB=1024` (or 512).

At volume server start it creates 8 volumes by default (`-max`).

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Components (raw markdown, read in full). An unconfirmed `collection.list` verification step was removed.
