---
id: computing-software.systems-network-administration.linux.find-processes-using-swap
name: find-processes-using-swap
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vmswap, swap-usage, smem, proc-status, swap, memory-pressure]
level: practitioner
status: docs-checked
description: "Identify which processes are swapped out and whether swapping is actually hurting: VmSwap per process, smem -s swap, cgroup swap accounting, and vmstat si/so rates."
sources:
  - https://www.kernel.org/doc/html/latest/filesystems/proc.html
  - https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
  - https://www.kernel.org/doc/html/latest/accounting/psi.html
  - https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html
  - https://github.com/procps-ng/procps/blob/master/man/vmstat.8
  - https://github.com/systemd/systemd/blob/main/man/systemd.resource-control.xml
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/swapon.8.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Who is using swap?

## Per process
```bash
for f in /proc/[0-9]*/status; do
  awk '/^Name:/{n=$2} /^Pid:/{p=$2} /^VmSwap:/{if($2>0) print $2" kB", p, n}' "$f" 2>/dev/null
done | sort -rn | head -15
```
## Per service (cgroup v2)
```bash
for d in /sys/fs/cgroup/system.slice/*.service; do
  printf '%s %s\n' "$(cat $d/memory.swap.current 2>/dev/null)" "${d##*/}"
done | sort -rn | head
systemd-cgtop -m                    # memory per control group
```
## Is swap usage a problem?
Swap **used** isn't bad — idle pages pushed out. Swap **activity** is:
```bash
vmstat 1 10        # si/so columns: memory swapped in from / to disk per second; sustained non-zero values under load = thrashing
cat /proc/pressure/memory   # PSI: 'some' and 'full' lines with avg10/avg60/avg300 stall percentages
```
## Actions
- Get a process's pages back proactively: restart it, or `swapoff -a && swapon -a` (only with enough free RAM: swapoff must move every page back).
- `vm.swappiness` (0-200) sets the relative I/O cost of swapping versus file paging; cap a service's swap with `MemorySwapMax=`.
- Real fix for thrashing: more RAM or less memory demand.

## Verify
- [ ] You can name the top swap consumers, and si/so rates confirm whether they matter.

## Checked

2026-10-26. Linux kernel documentation (master): VmSwap field in /proc/PID/status, cgroup v2 memory.swap.current and memory.swap.max, PSI /proc/pressure/memory format, vm.swappiness range 0-200 and meaning. procps vmstat(8): si and so definitions. systemd.resource-control: MemorySwapMax=. util-linux swapoff(8) disables swap on listed or all devices. Removed smem, top SWAP column and sar -W lines, which were not checked.

Method: documentation only; no commands were run.
