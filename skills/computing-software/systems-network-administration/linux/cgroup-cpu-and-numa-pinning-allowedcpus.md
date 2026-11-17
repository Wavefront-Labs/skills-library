---
id: computing-software.systems-network-administration.linux.cgroup-cpu-and-numa-pinning-allowedcpus
name: cgroup-cpu-and-numa-pinning-allowedcpus
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, allowedcpus, allowedmemorynodes, cpuset, cgroup-v2, systemd-resource-control, cpu-isolation, numa]
level: advanced
status: docs-checked
description: "Pin services or slices to CPUs and NUMA nodes with systemd AllowedCPUs/AllowedMemoryNodes (cgroup v2 cpuset), versus CPUAffinity and taskset, and verifying placement."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
  - https://docs.kernel.org/admin-guide/cgroup-v2.html#cpuset
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
  - https://docs.kernel.org/admin-guide/cgroup-v2.html
  - https://github.com/systemd/systemd/blob/main/man/systemd.resource-control.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU and memory-node pinning with AllowedCPUs

## Options compared
| Mechanism | Scope | Enforced on children / later threads? |
|---|---|---|
| `AllowedCPUs=` / `AllowedMemoryNodes=` (cgroup v2 cpuset controller) | unit or slice (whole cgroup) | cgroup-level restriction applied to every process in the unit |
| `CPUAffinity=` (systemd.exec) | CPU affinity of the executed processes | a process-level setting |
| `taskset -c` | one process | a process-level setting |

## Pin a service
```bash
systemctl set-property --runtime db.service AllowedCPUs=8-15 AllowedMemoryNodes=1   # test live
systemctl edit db.service      # persist:
#   [Service]
#   AllowedCPUs=8-15
#   AllowedMemoryNodes=1
```
## Keep housekeeping off workload CPUs
```bash
systemctl set-property system.slice AllowedCPUs=0-3
systemctl set-property user.slice  AllowedCPUs=0-3
systemctl set-property init.scope  AllowedCPUs=0-3
systemctl set-property workload.slice AllowedCPUs=4-31
```
(Isolating kernel threads and IRQs is separate: see the `isolcpus=`, `nohz_full=` and `irqaffinity=` kernel parameters.)

## Verify placement
```bash
cat /sys/fs/cgroup/system.slice/db.service/cpuset.cpus.effective
cat /sys/fs/cgroup/system.slice/db.service/cpuset.mems.effective
taskset -cp $(systemctl show -p MainPID --value db.service)
ps -eLo pid,tid,psr,comm | grep postgres      # psr = CPU each thread last ran on
```

## Gotchas
- Applies to the unified (v2) hierarchy; the settings control the cpuset controller.
- The CPUs a cgroup actually gets are those granted by its parent: compare `cpuset.cpus.effective` with what you requested.
- Hyperthread siblings: check the CPU topology (`lscpu -e`) before assigning CPU ranges.

## Verify
- [ ] `cpuset.cpus.effective` matches; under load, `mpstat -P ALL 1` shows activity only on the assigned CPUs.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (cgroup-v2 cpuset, kernel-parameters) and the systemd `systemd.resource-control`/`systemd.exec` man sources on 2026-10-26. Confirmed: `AllowedCPUs=` and `AllowedMemoryNodes=` control the cpuset controller in the unified hierarchy, `CPUAffinity=` is a systemd.exec process setting, `cpuset.cpus.effective` and `cpuset.mems.effective` files, `isolcpus=`, `nohz_full=`, `irqaffinity=` boot parameters. Removed: the claims that apps cannot widen the cgroup set and that the cpuset controller is enabled automatically, and the tuned cpu-partitioning reference.

Method: documentation only; no commands were run.
