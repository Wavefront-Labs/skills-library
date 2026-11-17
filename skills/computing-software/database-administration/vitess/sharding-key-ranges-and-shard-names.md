---
id: computing-software.database-administration.vitess.sharding-key-ranges-and-shard-names
name: sharding-key-ranges-and-shard-names
category: computing-software
field: database-administration
product: vitess
tags: [sharding, key-ranges, shard-names, keyspace-id, partition, generateshardranges]
level: practitioner
status: docs-checked
description: "Read and design Vitess shard names and key ranges: hex range notation, full partitions, left-justification, and which operation fits which need."
sources:
  - https://vitess.io/docs/25.0/reference/features/sharding/
  - https://vitess.io/docs/25.0/concepts/shard/
  - https://vitess.io/docs/25.0/concepts/keyspace-id/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Vitess shard name is its key range in hexadecimal, `start-end`, where start is inclusive and end exclusive. The names are left-justified and right-padded with zeros, so `-80` equals `00-80` equals `0000-8000`. A plain `-` is the full range; `-80` means everything below 0x80 and `80-` means everything at or above it. `80-FF` is not `80-`: `80-FF` equals `8000-FF00`, so a keyspace ID of `FFFF` falls outside it. An unsharded keyspace has one shard named `0` (sometimes `-`).

The keyspace ID is computed from a column through a vindex. A `xxhash` vindex yields an unsigned 64-bit value, so anything below `0x8000000000000000` lands in `-80`. A key range is consecutive keyspace IDs; a partition is a set of ranges covering all space, with one shard having an empty start and one having an empty end. `-40`, `40-80`, `80-c0`, `c0-` is a valid full partition, and shards need not be equal in size (for example `-80`, `80-c0`, `c0-dc00`, `dc00-dc80`, `dc80-`).

Generate ranges for N shards with `vtctldclient GenerateShardRanges`.

Which action fits which need:
- more read capacity: add replicas or split shards.
- more write capacity: split shards.
- reclaim resources: merge shards or keyspaces.
- more geo-diversity: add cells and replicas.
- a hot tablet: replicas for reads, splits for writes.

Horizontal sharding splits or merges shards; vertical sharding moves tables to another keyspace. Sharding is orthogonal to MySQL replication.

## Checked

2026-11-08. Read in full: Sharding, Shard and Keyspace ID pages (vitess.io docs 25.0, via the website repo markdown). Confirmed: naming rules and the 80-FF caveat, xxhash example and unsharded shard name (Shard page); key range, partition and full-partition definitions, the examples, the requirement and action table and GenerateShardRanges (Sharding page); keyspace ID role (Keyspace ID page). Nothing removed.

Method: documentation only; no commands were run.
