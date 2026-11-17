---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.ec-bitrot-checksum-scrub
name: ec-bitrot-checksum-scrub
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [ec-scrub, crc32c, parity, bitrot, ecsum]
level: advanced
status: docs-checked
description: "Detect silent corruption in erasure-coded volumes with the .ecsum checksum sidecar and ec.scrub -mode checksum; flags and safe rebuild behaviour."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/EC-Bitrot-Detection
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ec bitrot checksum scrub

Problem: parity shards (.ec10-.ec13) are never read in normal serving, so a rotten parity shard stays unnoticed until reconstruction silently produces wrong data.

Fix: an optional sidecar `<volume>.ecsum` stores a CRC32C per block (default 16 MiB) of every shard, about 11 KB for a 30 GB volume. It is written during the single EC encode pass and travels with the shards. A missing sidecar means the feature is off; older binaries ignore it.

Volume server flags:
- `-ec.bitrotChecksum` (default true)
- `-ec.bitrotBlockSizeMB` (default 16, power of two)

```bash
weed volume -dir=/path/to/data -ec.bitrotChecksum -ec.bitrotBlockSizeMB=16
```
Scrub in `weed shell`:
```
ec.scrub -mode checksum
ec.scrub -mode checksum -volumeId 7 -node 127.0.0.1:8080
```
Flagged shards are arbitrated by Reed-Solomon reconstruction, so a stale sidecar block cannot condemn a healthy shard. During rebuild, corrupt input shards are excluded and regenerated. A malformed sidecar makes rebuild fail closed unless you pass `-unsafeIgnoreSidecar`. Volumes encoded earlier get a sidecar automatically on rebuild when one server can reach all shards.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki page EC Bitrot Detection (raw markdown, read in full).
