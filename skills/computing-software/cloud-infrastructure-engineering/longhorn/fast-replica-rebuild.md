---
id: computing-software.cloud-infrastructure-engineering.longhorn.fast-replica-rebuild
name: fast-replica-rebuild
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [fast-replica-rebuild, rebuild, checksum, snapshot-data-integrity, replicas]
level: advanced
status: docs-checked
description: "Enable Longhorn fast replica rebuilding with fast-replica-rebuild-enabled, which needs snapshot-data-integrity enabled or fast-check, and how it skips unchanged snapshots."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/rebuilding/fast-replica-rebuilding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shorten replica rebuild time on large volumes.

Setting: `fast-replica-rebuild-enabled` (global). The page states no default.

Requirement: `snapshot-data-integrity` must be `enabled` or `fast-check`.

How it works: with data integrity enabled or `fast-check`, Longhorn records each snapshot disk file's change timestamp and checksum. Rebuilding skips syncing a snapshot disk file when both hold:
- the file's current change timestamp matches the recorded value
- the local and remote copies have the same checksum

Legacy rebuilding instead hashes every data block in every snapshot file and compares it with the remote block's checksum. That is I/O and compute intensive, especially for large volumes or many snapshots.

Steps:
1. Set `snapshot-data-integrity` to `enabled` or `fast-check`.
2. Turn on `fast-replica-rebuild-enabled`.
3. Rebuilds of volumes whose snapshot files have recorded checksums use the fast path.

Background (concepts page): a rebuild adds a blank replica in write-only mode, syncs it, switches it to read-write, then removes the faulty replica.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/rebuilding/fast-replica-rebuilding/

No claim needed changing.

Method: documentation only; no commands were run.
