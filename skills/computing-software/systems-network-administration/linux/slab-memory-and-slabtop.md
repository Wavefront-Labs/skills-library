---
id: computing-software.systems-network-administration.linux.slab-memory-and-slabtop
name: slab-memory-and-slabtop
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, memory, slab, slabtop, sunreclaim, sreclaimable, dentry-cache, kmalloc, kernel-memory-leak, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Explain memory used by the kernel itself: read slab usage with slabtop and /proc/slabinfo, tell reclaimable dentry/inode caches from unreclaimable leaks, and what to do about each."
sources:
  - https://man7.org/linux/man-pages/man1/slabtop.1.html
  - https://man7.org/linux/man-pages/man5/slabinfo.5.html
  - https://docs.kernel.org/admin-guide/sysctl/vm.html
  - https://docs.kernel.org/admin-guide/mm/slab.html
  - https://docs.kernel.org/admin-guide/sysctl/vm.html
  - https://gitlab.com/procps-ng/procps/-/blob/master/man/slabtop.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel slab memory and slabtop

**Goal:** when processes' RSS doesn't add up to "used" memory, find what the kernel is holding
and decide whether it's harmless cache or a leak.

## 1. How big is slab
```bash
grep -E '^(Slab|SReclaimable|SUnreclaim)' /proc/meminfo
```
`SReclaimable` (dentries, inodes, some buffers) is given back under pressure — like page cache.
`SUnreclaim` growing over days with no load change = kernel/driver leak.

## 2. Which caches
```bash
slabtop -o -s c | head -20          # one-shot, sorted by cache size
slabtop -s c                        # interactive
```
Map the biggest cache names to their subsystem. `dentry` and the `*_inode_cache` caches hold directory and inode objects (reclaimable, see `vm.vfs_cache_pressure`); a cache that grows without bound under steady load points at the subsystem or driver that owns it.

## 3. Act
- Reclaimable dentry/inode bloat (millions of negative dentries from apps probing
  nonexistent paths): harmless unless it pushes out useful cache; raising `vm.vfs_cache_pressure`
  above its default makes the kernel favour reclaiming directory and inode caches. One-off:
  `echo 2 > /proc/sys/vm/drop_caches` (reclaimable slab objects).
- Unreclaimable growth: note the cache, `slabtop` time series, kernel version, loaded modules
  (`lsmod`), then search the distro bug tracker; often fixed by a kernel/driver update.
  Enable `slab_debug` (legacy name `slub_debug`) only on test systems: it turns on full debugging for all slabs.
- `nf_conntrack` large: review `net.netfilter.nf_conntrack_max` and what traffic is tracked.

## Gotchas
- Slabs of similar size can be merged; boot with `slab_nomerge` to keep caches distinct (test only).
- Kernel slab memory is not part of any process's RSS; per-cgroup slab usage appears as `slab` in the cgroup's `memory.stat`.

## Verify
- [ ] `SReclaimable + SUnreclaim` ≈ `Slab` and explains the "missing" memory.
- [ ] For a suspected leak, a daily `slabtop -o` snapshot shows the same cache climbing under steady load.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (proc meminfo, sysctl/vm, kernel-parameters, admin-guide/mm/slab, cgroup-v2) and the procps `slabtop(1)` man page on 2026-10-26. Confirmed: `Slab`/`SReclaimable`/`SUnreclaim` fields, `slabtop -o` and `-s c` (sort by cache size), `vfs_cache_pressure` scope, `drop_caches` value 2, `slab_nomerge`, `slab_debug` with `slub_debug` as legacy name, `slab` in memory.stat. Removed: the cache-name meaning table, the `/proc/slabinfo` awk pipeline, `notrack`.

Method: documentation only; no commands were run.
