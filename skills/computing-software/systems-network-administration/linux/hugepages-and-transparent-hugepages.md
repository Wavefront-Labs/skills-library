---
id: computing-software.systems-network-administration.linux.hugepages-and-transparent-hugepages
name: hugepages-and-transparent-hugepages
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, memory, hugepages, transparent-hugepages, thp, hugetlbfs, nr-hugepages, khugepaged, database-tuning, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Configure static huge pages for databases/VMs (nr_hugepages, hugetlbfs, boot-time reservation) and set Transparent Huge Pages to always/madvise/never per workload advice."
sources:
  - https://docs.kernel.org/admin-guide/mm/hugetlbpage.html
  - https://docs.kernel.org/admin-guide/mm/transhuge.html
  - https://www.postgresql.org/docs/current/kernel-resources.html#LINUX-HUGE-PAGES
  - https://github.com/redhat-performance/tuned/blob/master/tuned/plugins/plugin_vm.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Huge pages and Transparent Huge Pages

**Goal:** cut TLB misses for large-memory workloads (databases, JVMs, KVM guests) with
explicit huge pages, and avoid the latency spikes THP can cause for some databases.

## 1. Static (explicit) huge pages
```bash
grep -i huge /proc/meminfo          # HugePages_Total/Free/Rsvd, Hugepagesize (2048 kB on x86)
sysctl -w vm.nr_hugepages=4096      # 8 GiB of 2 MiB pages, now
echo 'vm.nr_hugepages = 4096' > /etc/sysctl.d/80-hugepages.conf
sysctl -w vm.hugetlb_shm_group=$(getent group dba | cut -d: -f3)   # gid allowed to use shm hugetlb
```
Allocation at runtime can fall short on fragmented memory (`HugePages_Total` less than asked).
Reserve at boot for reliability, also needed for 1 GiB pages:
`default_hugepagesz=1G hugepagesz=1G hugepages=16` on the kernel command line.
Per NUMA node: `/sys/devices/system/node/node[0-9]*/hugepages/` (one `hugepages-<size>kB` directory per size).
Mount for apps that use files: `mount -t hugetlbfs -o gid=dba,mode=1770 none /dev/hugepages`.

Sizing: PostgreSQL `huge_pages = on` needs enough pages for its shared memory (see the PostgreSQL kernel-resources page); size the pool to the application's documented need.
Static huge pages are taken from RAM whether used or not.

## 2. Transparent Huge Pages
```bash
cat /sys/kernel/mm/transparent_hugepage/enabled   # [always] madvise never
cat /sys/kernel/mm/transparent_hugepage/defrag
grep AnonHugePages /proc/meminfo
```
- `always`: kernel promotes anonymous memory automatically (khugepaged); good for many JVM
  and HPC loads, can cause latency spikes and memory bloat for some DBs.
- `madvise`: only regions apps request via `madvise(MADV_HUGEPAGE)` — sensible default.
- `never`: disables THP; some database vendors advise it, so check your database's current documentation.
Persist: kernel arg `transparent_hugepage=madvise` (or `always`/`never`), or a tuned profile
(`[vm] transparent_hugepages=never`), or a oneshot systemd unit that writes the sysfs files.
The default comes from the kernel build and distribution; read the sysfs file instead of assuming.

## Gotchas
- Setting nr_hugepages too high starves everything else → immediate OOM. Leave headroom.
- App configured for huge pages but not enough reserved: PostgreSQL with `huge_pages=on` fails to start, while `try` falls back.
- THP `defrag=always` can stall allocating tasks in direct reclaim/compaction; the documented alternatives include `defer`, `defer+madvise` and `madvise`.

## Verify
- [ ] `HugePages_Total` equals the target after reboot; after app start `HugePages_Free` drops by the expected amount.
- [ ] `cat /sys/kernel/mm/transparent_hugepage/enabled` shows the chosen mode after reboot.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) on 2026-10-26. Confirmed: `default_hugepagesz`/`hugepagesz`/`hugepages` boot parameters, `vm.hugetlb_shm_group`, hugetlbfs mount options (`uid`, `gid`, `mode`, `pagesize`, `size`), per-node sysfs location, THP `enabled` values and `transparent_hugepage=` boot parameter, `defer+madvise` defrag mode, tuned `[vm] transparent_hugepages` option (tuned source). Removed: distribution default and vendor-advice claims, Postgres query name, containers claim.

Method: documentation only; no commands were run.
