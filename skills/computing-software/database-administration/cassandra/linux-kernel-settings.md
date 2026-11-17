---
id: computing-software.database-administration.cassandra.linux-kernel-settings
name: linux-kernel-settings
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, vm-max-map-count, readahead, xfs-filesystem, os-tuning, swap-off, ulimits, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Host preparation"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux kernel and filesystem settings

Goal: prepare hosts.
- Read ahead: the production guide recommends 64KB for spinning disks and 4KB for SSD, set with `blockdev`.
- Raise `memlock` and `vm.max_map_count` if you hit `Map failed` errors; the Debian package does this for you.
- Check effective limits in `/proc/<pid>/limits`.
Verify: `/proc/<pid>/limits` shows the raised limits.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: read-ahead values (production guide), Map failed FAQ with /proc/<pid>/limits and vm.max_map_count.
Removed: swap, specific vm.max_map_count/nofile/nproc numbers, XFS/ext4, chrony and THP advice.
Method: documentation only; no commands were run.
