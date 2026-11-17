---
id: computing-software.systems-network-administration.glusterfs.volume-profile
name: volume-profile
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, profile, volume-profile, latency, io-stats]
level: practitioner
status: docs-checked
description: "Profile a GlusterFS volume with gluster volume profile start, info and stop to see per-brick, per-FOP latency and block-size histograms; client-side io-stats dump."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Monitoring-Workload.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Performance-Testing.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-afr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume profile

```
gluster volume profile VOLNAME start
gluster volume profile VOLNAME info
gluster volume profile VOLNAME stop
```

- `start` begins collecting per-brick, per-FOP I/O statistics. Volume info then also shows `diagnostics.count-fop-hits` and `diagnostics.latency-measurement` set to on.
- `info` shows cumulative stats per brick: a read and write block-size histogram, a per-FOP table of latency and call counts, and totals for duration and bytes read and written. Repeat it periodically to see change over time.
- `stop` ends profiling when no longer needed.

Server-side profiling measures volume-wide throughput and server latency, but not network or client latency.

Client-side profiling (what the application asks of Gluster, including replication latency):

```
gluster volume profile your-volume start
setfattr -n trusted.io-stats-dump -v io-stats-pre.txt /your/mountpoint
```

The dump is written to `/var/run/gluster/io-stats-pre.txt` on the client.

Many RCHECKSUM FOPs in the profile point at self-heal checksum work (see heal-tuning). For hot files use volume-top.

## Checked

2026-11-04. Confirmed against the glusterdocs Monitoring Workload, Performance Testing and Troubleshooting AFR pages: profile start, info and stop, the count-fop-hits and latency-measurement options, the info output contents, periodic info, the server-side limits, the client-side trusted.io-stats-dump steps and output path, and the RCHECKSUM remark. Nothing removed.

Method: documentation only; no commands were run.
