---
id: computing-software.systems-network-administration.zfs.zfs-receive-corrective
name: zfs-receive-corrective
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, receive, corrective, healing, corruption, scrub]
level: sme
status: docs-checked
description: "Repair corrupted ZFS data blocks from a healthy replica with zfs receive -c, understand its limits, and follow up with a scrub."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zfs-receive.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Corrective receive

```
zfs receive -c [-vn] filesystem|snapshot
```

A corrective receive repairs corrupted data blocks by using a stream as the healthy source.

```
zfs send pool/backup/data@a | zfs receive -c tank/data@a
```

## Limits

- Only data blocks present in the stream are healed. Metadata cannot be healed this way.
- `-n` and `-v` are accepted (`zfs receive -c [-vn]`).

## After repairing

The man page recommends running a scrub after healing to ensure all corruption was repaired:

```
zpool scrub tank
```

## Caution

The man page warns that with slowly failing hardware, periodically repairing the data will not prevent data loss when the hardware fails completely.

## Checked

2026-11-03. Confirmed against zfs-receive(8) `-c`: synopsis, data blocks only, scrub recommendation, failing-hardware warning. Removed the unsupported same-snapshot rule, the `zpool status -v` claim, the SMART/cabling advice and the replica note.
Method: documentation only; no commands were run.
