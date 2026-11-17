---
id: computing-software.systems-network-administration.virtualisation.proxmox-ceph-rados-bench-osd-performance
name: proxmox-ceph-rados-bench-osd-performance
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [rados-bench, ceph, benchmark, proxmox, storage-performance]
level: advanced
status: docs-checked
description: "Benchmark Proxmox VE Ceph with rados bench, ceph tell osd bench and fio on RBD, interpret the numbers and clean up test pools safely."
sources:
  - https://docs.ceph.com/en/latest/man/8/rados/
  - https://www.proxmox.com/en/downloads/proxmox-virtual-environment/documentation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rados bench and OSD performance

**Goal:** a baseline for cluster throughput and latency before production, and a way to spot slow OSDs.

## Test pool
```bash
pveceph pool create benchpool --pg_autoscale_mode on   # --add_storages defaults to 0
```

## rados bench
```bash
rados bench -p benchpool 60 write -b 4M -t 16 --no-cleanup   # bandwidth and latency for 4 MB writes
rados bench -p benchpool 60 seq -t 16                        # sequential reads of what was written
rados bench -p benchpool 60 rand -t 16                       # random reads
rados bench -p benchpool 30 write -b 4096 -t 64 --no-cleanup # small-block view
rados -p benchpool cleanup
```
`bench <seconds> <mode>` modes are write, seq and rand; `-t` is concurrent operations (default 16), and `-b` applies to write mode only. `seq` needs a prior `write --no-cleanup` run on the same host, or object names will not match. Use `--run-name <label>` when benchmarking from several clients, and `rados cleanup [--run-name <name>] [--prefix <prefix>]` to remove the objects (default run name `benchmark_last_metadata`). Running several clients at once finds the cluster limit rather than one client's limit.

## Per-OSD
```bash
ceph tell osd.<id> bench [TOTAL_BYTES] [BYTES_PER_WRITE] [OBJ_SIZE] [NUM_OBJS]   # for example: ceph tell osd.0 bench 12288000 4096 4194304 100
ceph tell osd.<id> cache drop    # drop the OSD cache before a bench run
```
Compare OSDs of the same device class: an OSD far below its peers deserves a look at that disk, its controller mode and its network.

## fio inside a VM (what guests see)
```bash
fio --name=randrw --filename=/dev/sdb --direct=1 --rw=randrw --bs=4k --iodepth=32 --numjobs=4 --runtime=60 --time_based --group_reporting
```

## Cleanup
```bash
ceph config set mon mon_allow_pool_delete true     # default is false; only if pool deletion is refused
pveceph pool destroy benchpool                      # --remove_storages / --force are optional flags
ceph config set mon mon_allow_pool_delete false
```
Leftover bench objects in a pool (names starting with `bench`) also consume capacity if the pool is kept.

## Interpreting
- 4M write bandwidth capped near one NIC's speed points at the network (check the cluster network).
- High 4K latency with idle CPUs points at the OSD devices; compare per-OSD `bench` results.

## Checked

2026-10-26. Documentation checked: Ceph docs and option definitions (src/common/options) on ceph/ceph master (last commit 2026-10-25), pveceph(1) man page for PVE 9.2.13 and the pveceph.adoc source. Confirmed: rados bench modes, -b write-only, -t default 16, --no-cleanup, --run-name, cleanup options and default run name (rados man page), ceph tell osd.N bench arguments and cache drop (mClock reference), pveceph pool create/destroy options and defaults, mon_allow_pool_delete default false. The fio options (name, filename, direct, rw=randrw, bs, iodepth, numjobs, runtime, time_based, group_reporting) were checked against the fio HOWTO on axboe/fio. Removed the unconfirmed 1 GB per-OSD default, ceph osd perf, drop_caches advice and the benchmark-paper pointer.

Method: documentation only; no commands were run.
