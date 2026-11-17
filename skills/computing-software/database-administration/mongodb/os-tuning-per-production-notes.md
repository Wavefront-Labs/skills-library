---
id: computing-software.database-administration.mongodb.os-tuning-per-production-notes
name: os-tuning-per-production-notes
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-production-notes, numa-mongodb, mongodb-ulimit, transparent-huge-pages, xfs, readahead, swappiness]
level: practitioner
status: docs-checked
description: "Apply the MongoDB production notes on Linux: XFS, ulimits, THP setting by version, NUMA interleave, readahead, swappiness, and clock sync, then check startup warnings."
sources:
  - https://www.mongodb.com/docs/manual/administration/production-notes/
  - https://www.mongodb.com/docs/manual/reference/ulimit/
  - https://www.mongodb.com/docs/manual/administration/tcmalloc-performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OS tuning per the MongoDB production notes

## Filesystem
- **XFS** is strongly recommended for data-bearing nodes to avoid performance issues that can occur with ext4 and WiredTiger.
- Turn off `atime` (mount with `noatime`) on the volume holding the database files. The manual also describes separating components onto different storage devices.
- Readahead: set it between 8 and 32 regardless of media type (disk access is mostly random, so higher values give little benefit and can hurt) unless testing shows a repeatable benefit from a higher value.

## ulimits (recommended values)
```ini
# /etc/systemd/system/mongod.service.d/limits.conf
[Service]
LimitNOFILE=64000
LimitNPROC=64000
LimitFSIZE=infinity
LimitCPU=infinity
LimitAS=infinity
LimitMEMLOCK=infinity
```
The manual's recommended ulimit settings are unlimited for file size, CPU time, virtual memory, locked-in-memory size and memory size, and 64000 for processes (`-u`) and open files (`-n`); with an open-files limit under 64000 MongoDB logs a startup warning, and low limits can cause failed connections and loss of service under heavy use.

## Transparent Huge Pages
- MongoDB **8.0**: **enable** Transparent Huge Pages; 8.0 uses an upgraded TCMalloc that performs better with THP enabled (follow the manual's enable-THP procedure).
- MongoDB **7.0 and earlier**: **disable** THP; these versions perform better with typical 4096-byte pages (see the manual's disable-THP procedure).
Check the current mode with `cat /sys/kernel/mm/transparent_hugepage/enabled`.

## NUMA
MongoDB checks NUMA settings at startup on Linux and warns if the configuration may degrade performance. Disable NUMA in the BIOS if possible; otherwise disable zone reclaim and interleave memory, and make sure `numad` is not enabled:
```bash
echo 0 | sudo tee /proc/sys/vm/zone_reclaim_mode
# ExecStart=/usr/bin/numactl --interleave=all /usr/bin/mongod --config /etc/mongod.conf
```

## Memory and swap
- `vm.swappiness` of 1 (swap only to avoid out-of-memory) or 0 depending on your cluster; on RHEL/CentOS also set `vm.force_cgroup_v2_swappiness` to 1 so the value overrides the cgroup default of 60.
- The default WiredTiger cache is the larger of 50% of (RAM - 1 GB) or 0.256 GB; the manual advises against raising it above the default.

## Other
- Time synchronisation (NTP) on every member, since time-dependent operations rely on it.
- `net.ipv4.tcp_keepalive_time = 120`: if the TCP keepalive value is greater than your firewall's idle timeout, connections can be dropped.

## Verify
`db.adminCommand({ getLog: "startupWarnings" })` shows no OS warnings (for example open-files limit under 64000 or NUMA); `cat /proc/$(pidof mongod)/limits` shows the configured limits.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: XFS strongly recommended, noatime, readahead 8 to 32, recommended ulimits (unlimited file size, CPU time, virtual memory, locked memory, memory size; 64000 open files and processes) and the 64000 open-files startup warning, THP enabled for 8.0 and disabled for 7.0 and earlier, NUMA startup check with zone_reclaim_mode 0 and numactl --interleave=all and numad off, vm.swappiness 1 or 0 with vm.force_cgroup_v2_swappiness on RHEL/CentOS, default WiredTiger cache (larger of 50% of RAM minus 1 GB or 0.256 GB), tcp_keepalive_time 120, NTP. Removed unconfirmed claims (ext4 stall explanation, readahead sector arithmetic and startup warning, container cache advice, somaxconn, tuned profiles, 8.0 THP mode details).

Method: documentation only; no commands were run.
