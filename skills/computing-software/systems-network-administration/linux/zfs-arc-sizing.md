---
id: computing-software.systems-network-administration.linux.zfs-arc-sizing
name: zfs-arc-sizing
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, zfs, zfs-arc, zfs-arc-max, arcstat, l2arc, memory-tuning, openzfs]
level: advanced
status: docs-checked
description: "Size the ZFS ARC on Linux: zfs_arc_max/min module options, arcstat and arc_summary reading, interaction with page cache and VMs/databases, and L2ARC caveats."
sources:
  - https://openzfs.github.io/openzfs-docs/man/master/4/zfs.4.html
  - https://openzfs.github.io/openzfs-docs/Performance%20and%20Tuning/Workload%20Tuning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZFS ARC sizing

The ARC is ZFS's cache, separate from the Linux page cache. With `zfs_arc_max=0` the ARC limit is the larger of (all memory minus 1 GiB) and 5/8 of memory, per the current zfs(4) man page; the minimum settable value is 64 MiB.

## Observe
```bash
arc_summary | less                       # size, target, hit ratios, MRU/MFU
arcstat 5                                # read, hit%, miss%, arcsz, c (target)
cat /proc/spl/kstat/zfs/arcstats | grep -E '^(size|c_max|c_min|hits|misses) '
```
Very low hit rates mean the workload doesn't cache (streaming) or the ARC is too small.

## Set limits
```bash
echo $((16*1024**3)) > /sys/module/zfs/parameters/zfs_arc_max     # runtime, bytes
echo "options zfs zfs_arc_max=17179869184 zfs_arc_min=4294967296" > /etc/modprobe.d/zfs.conf
# root-on-ZFS: rebuild the initramfs (for example `dracut -f`) so the option applies at import
```
## Sizing guidance
- Dedicated file server: let ARC take most RAM.
- VM host: cap ARC so guests + host have headroom (RAM minus guest RAM minus host needs).
- Databases with their own cache (PostgreSQL shared_buffers, InnoDB buffer pool): cap ARC and consider
  `primarycache=metadata` on the data dataset to avoid double caching.
- If memory-pressure kills occur during bursts, lower the cap; `zfs_arc_sys_free` sets how much memory the ARC leaves free.

## L2ARC
Second-level cache on SSD: `zpool add tank cache /dev/nvme1n1`. Helps only when the working set is bigger than RAM but fits on the SSD and reads repeat.
The L2ARC is rebuilt on pool import (persistent) while `l2arc_rebuild_enabled=1`, the default.

## Verify
- [ ] `arcstat` shows `c` at the configured max after reboot; no memory-pressure OOMs; hit ratio acceptable.

## Checked

Checked 2026-10-27 against OpenZFS zfs(4), zfsprops(7) and zpool-add(8) man page sources (openzfs/zfs master, 2026-10-27). Confirmed: zfs_arc_max default rule and 64 MiB minimum, zfs_arc_min default, zfs_arc_sys_free, l2arc_rebuild_enabled default, primarycache=metadata value, zpool add cache usage. Removed or softened: 50% default claim (the documented default is larger), the 90% hit-ratio rule, the 4 GB headroom figure, the L2ARC header-RAM remark, the OpenZFS 2.0 version for persistent L2ARC.

Method: documentation only; no commands were run.
