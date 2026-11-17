---
id: computing-software.systems-network-administration.linux.kernel-samepage-merging-ksm
name: kernel-samepage-merging-ksm
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ksm, kernel-samepage-merging, ksmtuned, memory-deduplication, kvm, overcommit]
level: advanced
status: docs-checked
description: "Use kernel samepage merging to deduplicate identical memory pages for KVM hosts: enabling, ksmtuned, reading /sys/kernel/mm/ksm counters, CPU cost and side-channel risks."
sources:
  - https://docs.kernel.org/admin-guide/mm/ksm.html
  - https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel samepage merging (KSM)

**What:** `ksmd` scans memory regions marked `MADV_MERGEABLE` (QEMU does this for guest RAM) and merges
identical pages copy-on-write. Many similar VMs (same OS) can share gigabytes.

## Control
```bash
cat /sys/kernel/mm/ksm/run                 # 0 off, 1 run, 2 stop and unmerge all
echo 1 > /sys/kernel/mm/ksm/run
echo 100 > /sys/kernel/mm/ksm/pages_to_scan ; echo 20 > /sys/kernel/mm/ksm/sleep_millisecs   # documented defaults
```
The documented defaults (100 pages, 20 ms) are "chosen for demonstration purposes"; tune them for your workload. A scan-time advisor (`advisor_mode`) can adjust `pages_to_scan` automatically.
Per-service opt-in for non-QEMU apps: systemd `MemoryKSM=yes` (systemd 254+).

## Is it worth it?
```bash
cd /sys/kernel/mm/ksm
echo "shared=$(cat pages_shared) sharing=$(cat pages_sharing) unshared=$(cat pages_unshared)"
# general_profit is the kernel's estimate of net saving (saved pages minus rmap bookkeeping)
```
High `pages_sharing/pages_shared` ratio = good dedup. High `pages_unshared` with little sharing = wasted CPU.

## Costs and risks
- `ksmd` CPU use (watch it in top) grows with scan rate.
- Merged pages are unmerged on write — memory can spike back if guests diverge; don't overcommit to the edge.
- Side channels: KSM enables cross-VM memory deduplication attacks; disable on multi-tenant hosts with untrusted guests.

## Disable
`echo 2 > /sys/kernel/mm/ksm/run` stops ksmd and unmerges all merged pages.

## Verify
- [ ] `pages_sharing` rises after VMs boot; host free memory improves without ksmd dominating CPU.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) and the systemd `systemd.exec(5)` source on 2026-10-26. Confirmed: `run` values 0/1/2 and their meaning, `pages_to_scan` default 100 and `sleep_millisecs` default 20, `general_profit`, `pages_shared`/`pages_sharing`/`pages_unshared`, MADV_MERGEABLE opt-in, `MemoryKSM=` added in systemd v254. Removed: `ksmtuned`/RHEL service names, the prctl version gate, the THP interaction claim and the libvirt element (not covered by the documentation read).

Method: documentation only; no commands were run.
