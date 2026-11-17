---
id: computing-software.systems-network-administration.linux.lvm-cache-and-writecache
name: lvm-cache-and-writecache
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, lvm, lvm-cache, dm-cache, dm-writecache, ssd-cache, cachepool, cache-mode, writethrough, writeback, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Put an SSD/NVMe cache in front of slow LVs with lvmcache (dm-cache) or dm-writecache: create, choose writethrough vs writeback, monitor hit rates, and detach safely."
sources:
  - https://github.com/lvmteam/lvm2/blob/main/man/lvmcache.7_main
  - https://github.com/lvmteam/lvm2/blob/main/man/lvconvert.8_pregen
  - https://github.com/lvmteam/lvm2/blob/main/lib/report/columns.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LVM cache (dm-cache / dm-writecache)

**Goal:** accelerate a large HDD-backed LV with a small fast device, without losing data if
the cache device dies.

## 1. Two kinds
- **cache** (dm-cache): caches hot blocks for reads and (optionally) writes. Modes:
  `writethrough` (default; writes go to both — cache loss is harmless) or `writeback`
  (writes acknowledged from SSD — cache loss = data loss unless the cache is mirrored).
- **writecache** (dm-writecache): speeds up writes only. Data read from the main LV is not
  stored in the cache, only newly written data.

## 2. Create
Both PVs must be in the same VG.
```bash
vgextend vg0 /dev/nvme0n1p1
# A: cachevol (simple; cache data and metadata share one fast LV)
lvcreate -n fast -L 100G vg0 /dev/nvme0n1p1
lvconvert --type cache --cachevol fast --cachemode writethrough vg0/data
# B: cache pool (separate data+metadata sub-LVs)
lvcreate --type cache-pool -n cpool -L 100G vg0 /dev/nvme0n1p1
lvconvert --type cache --cachepool cpool vg0/data
# writecache
lvconvert --type writecache --cachevol fast vg0/data
```

## 3. Monitor and tune
```bash
lvs -a -o name,size,segtype,cache_mode,devices vg0
lvs -o name,cache_read_hits,cache_read_misses,cache_write_hits,cache_write_misses,cache_dirty_blocks vg0/data
lvchange --cachemode writeback vg0/data          # switch mode (think twice)
lvchange --cachepolicy smq vg0/data              # smq is the default policy
```
Low read hit ratio after warm-up = working set larger than cache, or a sequential/streaming
workload (caches don't help backups and scans).

## 4. Remove / replace
```bash
lvconvert --splitcache vg0/data      # flush dirty blocks, detach, keep cache LV
lvconvert --uncache vg0/data         # flush, detach and delete cache LV
```
Always detach before removing the SSD: both commands flush the cache first.

## Gotchas
- Writeback on a single unmirrored SSD is a data-loss risk; build the fast LV as RAID1 (`lvcreate --type raid1 -m 1 ... /dev/ssd1 /dev/ssd2`) or use writethrough.
- Flushing a large dirty writeback cache on `--uncache` can take a long time.
- bcache is a different, non-LVM mechanism; don't mix advice.

## Verify
- [ ] `lvs -a` shows `segtype cache`/`writecache` with the SSD in devices.
- [ ] Read hit counters grow under a repeated workload; latency (`iostat -x`) drops.
- [ ] `--splitcache` test on a lab LV completes and data is intact.

## Checked

Checked against the lvm2 main branch man pages (lvmcache(7), lvconvert(8) pregen, lvchange(8)), lib/report/columns.h and WHATS_NEW, repository last pushed 2026-10-09.
Confirmed: writethrough is the default cache mode and writeback is the alternative; smq is the default policy; `--cachevol`, `--cachepool`, `--splitcache` (flush, detach, keep the fast LV) and `--uncache` (flush, detach, delete it); the RAID1 fast-LV example; writecache stores only newly written data.
Fixed: the lvs report field is `cache_mode` (not `cachemode`). Removed unconfirmed claims: online conversion, the `--uncache --force` dead-SSD recovery, the initramfs advice, and that reads of recently written data hit the writecache.

Method: documentation only; no commands were run.
