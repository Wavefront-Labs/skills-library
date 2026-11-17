---
id: computing-software.systems-network-administration.linux.page-cache-buff-cache-and-drop-caches
name: page-cache-buff-cache-and-drop-caches
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, memory, free, free-memory, buff-cache, page-cache, drop-caches, meminfo, memavailable, dirty-pages, vmtouch, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Read free and /proc/meminfo correctly: used vs buff/cache vs available, how the page cache behaves, when (rarely) to drop caches, and spotting real memory pressure."
sources:
  - https://docs.kernel.org/filesystems/proc.html#meminfo
  - https://docs.kernel.org/admin-guide/sysctl/vm.html#drop-caches
  - https://github.com/util-linux/util-linux/blob/master/misc-utils/fincore.1.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# free, buff/cache and the page cache

**Goal:** stop panicking over "free: 200 MB", know how much memory is really available, and
know what the page cache is doing for you.

## 1. Reading free
```bash
free -h
#               total   used   free  shared  buff/cache  available
# Mem:           31Gi   9.1Gi  412Mi  1.2Gi       21Gi       20Gi
```
- **free** = completely unused RAM. Low is normal and good — idle RAM is wasted RAM.
- **buff/cache** = page cache (file contents) + buffers + reclaimable slab as reported by `free`.
- **available** = the kernel's estimate of memory available for new workloads without swapping (`MemAvailable` in `/proc/meminfo`). Prefer it over free for alerting.
- **shared** = tmpfs/shm memory (`Shmem`), which stays in memory (or swap) while files exist.

## 2. /proc/meminfo lines worth knowing
```bash
grep -E 'MemAvailable|^Cached|Buffers|Dirty|Writeback|Shmem|SReclaimable|SUnreclaim|AnonPages|Mapped|Active\(file\)|Inactive\(file\)' /proc/meminfo
```
`Dirty`/`Writeback` large → writes waiting for disk (see `vm.dirty_ratio`). `Shmem` large →
tmpfs or shared memory (check `df -h -t tmpfs`, `ipcs -m`). `SUnreclaim` large → kernel slab
leak (see slab skill).

## 3. What the page cache does
Reads populate it; repeat reads come from RAM. Writes land there first and are flushed later.
Under pressure the kernel evicts clean cache pages first (LRU active/inactive lists).
Check which files are cached: `fincore <file>` (util-linux). Reading a file (`cat file > /dev/null`) populates the cache.

## 4. Dropping caches (benchmarks only)
```bash
sync; echo 1 > /proc/sys/vm/drop_caches    # page cache
sync; echo 2 > /proc/sys/vm/drop_caches    # reclaimable slab (dentries, inodes)
sync; echo 3 > /proc/sys/vm/drop_caches    # both
```
Non-destructive (dirty pages aren't dropped — hence `sync` first) but it makes every
subsequent read go to disk: production latency spikes. It never "fixes" a memory problem;
if `available` is low the memory is used by processes, tmpfs or unreclaimable slab, not cache.

## 5. Real pressure signals
sustained swap-in/out in `vmstat 1`; non-zero and rising `some`/`full` averages in `/proc/pressure/memory`; the OOM killer in `journalctl -k`.

## Gotchas
- Containers: `free` reports system-wide memory; read `memory.current`/`memory.max` in the cgroup for per-container usage.
- Monitoring "free" instead of "available" generates false alerts on healthy hosts.

## Verify
- [ ] Your alert uses MemAvailable (or PSI), not MemFree.
- [ ] After dropping caches in a test, `buff/cache` falls and `free` rises, confirming the cache was reclaimable.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (sysctl/vm drop_caches, filesystems/proc meminfo) on 2026-10-26 and the util-linux `fincore` man source. Confirmed: `drop_caches` values 1/2/3 and meanings, non-destructive and `sync` first, informational log line, `MemAvailable`, `SReclaimable`/`SUnreclaim`, `Shmem` fields. Removed: procps version claim, `vmtouch`, `sar`, ZFS ARC, and percentage alert thresholds that no documentation covers.

Method: documentation only; no commands were run.
