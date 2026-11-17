---
id: computing-software.systems-network-administration.glusterfs.heal-tuning
name: heal-tuning
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, shd-max-threads, heal-count, shd-wait-qlength, self-heal]
level: advanced
status: docs-checked
description: "Diagnose and tune GlusterFS self-heal: heal-count and xattrop index checks, cluster.shd-max-threads and shd-wait-qlength for speed, and settings to reduce heal load."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-afr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heal tuning

Slow `heal info`: get an approximate pending count, or count the brick's xattrop index; a shrinking number means the backlog is clearing.

```
gluster volume heal $VOLNAME statistics heal-count
ls /brick/.glusterfs/indices/xattrop | wc -l
```

Heal start and end messages are in `/var/log/glusterfs/glustershd.log`.

Heal too slow (backlog shrinking slowly):

```
gluster volume set $VOLNAME cluster.shd-max-threads <N>
gluster volume set $VOLNAME cluster.shd-wait-qlength <N>
```

Defaults are 1 and 1024. Higher thread counts can overload bricks with weak storage.

Heal too aggressive: if `shd-max-threads` is already 1 and brick CPU is high with many RCHECKSUM FOPs in the volume profile, use full copies instead of rolling checksums (costs more bandwidth):

```
gluster volume set $VOLNAME cluster.data-self-heal-algorithm full
```

To keep client bandwidth for applications, disable client-side heals (recent versions already default to off):

```
gluster volume set $VOLNAME cluster.metadata-self-heal off
gluster volume set $VOLNAME cluster.data-self-heal off
gluster volume set $VOLNAME cluster.entry-self-heal off
```

## Checked

2026-11-04. Confirmed against the glusterdocs Troubleshooting AFR page: heal-count and xattrop index checks, glustershd.log, shd-max-threads and shd-wait-qlength with defaults 1 and 1024, the RCHECKSUM and data-self-heal-algorithm full advice with its bandwidth trade-off, and the three client-side heal options being off by default in recent versions. Nothing removed.

Method: documentation only; no commands were run.
