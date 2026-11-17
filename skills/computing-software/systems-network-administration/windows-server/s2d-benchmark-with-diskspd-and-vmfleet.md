---
id: computing-software.systems-network-administration.windows-server.s2d-benchmark-with-diskspd-and-vmfleet
name: s2d-benchmark-with-diskspd-and-vmfleet
category: computing-software
field: systems-network-administration
product: windows-server
tags: [storage-spaces-direct, s2d, diskspd, vmfleet, storage-performance]
level: advanced
status: docs-checked
description: "Benchmark Storage Spaces Direct and other Windows storage with DiskSpd and VMFleet: DiskSpd options, warm-up, cache effects and reading results."
sources:
  - https://github.com/microsoft/diskspd/blob/master/CmdLineParser/CmdLineParser.cpp
  - https://github.com/microsoft/diskspd/tree/master/Frameworks/VMFleet
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/use-csv-cache
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmarking with DiskSpd and VMFleet

Benchmark before production so you know what "normal" is, and to catch misconfigured networking (RDMA off) or cache.

## DiskSpd on one volume
```cmd
diskspd.exe -c100G -d120 -W30 -r -w30 -b4K -t8 -o32 -Sh -L -D <TEST_DIR>\io.dat
```
- `-c100G` creates a 100 GiB test file (larger than the cache to see the backend), `-d120` duration in seconds (default 10), `-W30` warm-up seconds (default 5).
- `-r` random, `-w30` 30% writes, `-b4K` block size, `-t8` threads per file, `-o32` outstanding IO per thread.
- `-Sh` is equivalent to `-Suw` (no software caching, write-through), `-L` measures latency statistics, `-D` captures per-thread IOPS statistics at an interval (default 1000 ms).

## Reading output
Total IO/s, MiB/s and the latency statistics that `-L` adds. Rising latency at higher queue depth means you are past the
knee; reduce `-o` until latency is acceptable to find the usable maximum.

## VMFleet for clusters
VMFleet deploys many small VMs on each node, each running DiskSpd against its own VHDX, to load all nodes and CSVs at
once:
```powershell
# import the VMFleet module from the diskspd repository (Frameworks/VMFleet)
Import-Module VMFleet
New-Fleet -BaseVHD <BASE_VHDX> -VMs 10 -AdminPass <pwd> -ConnectUser <user> -ConnectPass <pwd>
Start-FleetSweep -b 4 -t 2 -o 16 -w 30 -d 300
Watch-FleetCluster            # live IOPS/latency per node
```
Use `Watch-FleetCluster` to see live per-node load.

## Gotchas
- Never run on volumes with production data; DiskSpd writes the test file.
- S2D cache: short tests hit cache only; long runs and big files show capacity tier behaviour.
- The CSV in-memory read cache can make DiskSpd and VMFleet results worse than with it disabled.

## Verify
- [ ] Results recorded per profile with config (firmware, drivers, cache) as the baseline.

## Checked

Confirmed 2026-10-25 against the DiskSpd command-line parser source (microsoft/diskspd, last commit 2026-09-04): -c, -d (default 10 s), -W (default 5 s), -r, -w, -b, -t, -o, -Sh (equivalent to -Suw), -L (latency statistics), -D (interval in milliseconds, default 1000); and the VMFleet module source (version 2.1.0.0): New-Fleet (BaseVHD, VMs, AdminPass, ConnectUser, ConnectPass), Start-FleetSweep (b, t, o, w, d), Watch-FleetCluster exported. The CSV read cache caveat comes from the Windows Server docs (use-csv-cache). Removed the unconfirmed workload profile sizes, Install-Module VMFleet, percentile claims and Performance Monitor counter advice, and replaced the sources entries with the repository sources.

Method: documentation only; no commands were run.
