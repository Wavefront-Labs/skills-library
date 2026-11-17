---
id: computing-software.systems-network-administration.zfs.zpool-iostat-latency
name: zpool-iostat-latency
category: computing-software
field: systems-network-administration
product: zfs
tags: [zfs, zpool, iostat, latency, histograms, queues, performance]
level: advanced
status: docs-checked
description: "Measure ZFS pool and vdev I/O with zpool iostat: intervals, per-vdev output, latency columns -l, queues -q, histograms -w and -r, and scripts."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/8/zpool-iostat.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zpool iostat

```
zpool iostat [[[-c SCRIPT] [-lq]] | -rw] [-T u|d] [-ghHLnpPvy] [pool...|[pool vdev...]|vdev...] [interval [count]]
```

`interval` repeats every N seconds; `count` stops after N reports. The first report is the average since boot, unless you pass `-y`. K/M/G are base 1024; `-p` gives raw values.

```
zpool iostat -v tank 5
zpool iostat -ly tank 10
zpool iostat -w tank
```

## Options

- `-v`: per-vdev rows below pool totals.
- `-l`: average latencies: `total_wait`, `disk_wait`, `syncq_wait`, `asyncq_wait`, `scrub`, `rebuild`, `trim`.
- `-q`: active queue lengths, pending and active, for sync, async, scrub, trim and rebuild queues.
- `-w`: latency histograms. `-r`: request size histograms (individual `ind` and aggregated `agg`), useful for checking aggregation.
- `-H`: scripted output. `-n`: headers once. `-T u|d`: timestamps. `-g`, `-L`, `-P`: GUIDs and path forms.
- `-c SCRIPT`: run scripts from `~/.zpool.d` or `/etc/zfs/zpool.d` per vdev and add columns; implies `-v`.

## Script environment

Scripts see `VDEV_PATH`, `VDEV_UPATH` and `VDEV_ENC_SYSFS_PATH`. `ZPOOL_SCRIPTS_PATH` overrides the search path, and `ZPOOL_SCRIPTS_AS_ROOT` lets privileged users run `-c`.

## Checked

2026-11-03. Pages read: zpool-iostat(8).

Confirmed: synopsis, interval and count, since-boot first report, -y, base-1024 units, -p, -v, -l and -q columns, -w, -r, -n, -c script behaviour and paths, environment variables.

Removed or corrected: the unsourced remark that a high disk_wait is the first suspect.

Method: documentation only; no commands were run.
