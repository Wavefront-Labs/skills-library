---
id: computing-software.systems-network-administration.linux.numa-placement-numactl-numastat
name: numa-placement-numactl-numastat
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, numactl, numastat, numa, lscpu, interleave, cpu-affinity, numa-balancing]
level: advanced
status: docs-checked
description: "Diagnose and control NUMA placement: lscpu/numactl --hardware topology, numastat per-process misses, binding or interleaving with numactl, and automatic NUMA balancing."
sources:
  - https://github.com/numactl/numactl/blob/master/numactl.8
  - https://github.com/numactl/numactl/blob/master/numastat.8
  - https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/sysctl/kernel.rst
  - https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/sysctl/vm.rst
  - https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml
  - https://github.com/systemd/systemd/blob/main/man/systemd.resource-control.xml
  - https://github.com/libvirt/libvirt/blob/master/docs/formatdomain.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NUMA placement

**When it matters:** multi-socket servers (and other machines that expose several NUMA nodes) running
databases, JVMs, VMs, where memory on a remote node costs more to reach (see the distance matrix from `numactl --hardware`).

## Topology
```bash
lscpu | grep -i numa                      # NUMA node0 CPU(s): 0-23,48-71
numactl --hardware                        # nodes, CPUs, memory per node, distance matrix
cat /sys/class/net/eth0/device/numa_node  # which node a NIC/NVMe hangs off
```
## Is placement bad?
```bash
numastat -c                               # system-wide numa_hit / numa_miss / other_node
numastat -p $(pgrep -o mysqld)            # per-process memory per node
```
Most memory on one node while the process runs on CPUs of another → misses.

## Control
```bash
numactl --cpunodebind=0 --membind=0 ./app          # strict: memory only from node 0
numactl --cpunodebind=1 --preferred=1 ./app        # prefer, fall back
numactl --interleave=all ./app                     # spread pages across all nodes
```
systemd: `NUMAPolicy=bind`, `NUMAMask=0`, `CPUAffinity=0-23` (or `AllowedCPUs=` / `AllowedMemoryNodes=` with cgroups).
KVM: `virsh numatune`, `<numatune>` / `vcpupin` in domain XML.

## Automatic NUMA balancing
`sysctl kernel.numa_balancing`: enables or disables automatic page-fault based NUMA balancing, which moves memory to the
nodes that access it often. `numactl --balancing` can enable it for one command. Pinned workloads may prefer it off.

## Gotchas
- `--membind` restricts allocations to the listed nodes, so a node smaller than the working set cannot spill to others.
- `vm.zone_reclaim_mode` is described in the kernel's vm sysctl documentation; read it before changing it.

## Verify
- [ ] `numastat -p` shows the process's memory on the same node as its CPUs; numa_miss stops growing.

## Checked

2026-10-26. numactl repository (last commit 2026-10-22): numactl --hardware, --cpunodebind, --membind, --preferred, --interleave, --balancing; numastat -c, -p and the numa_hit, numa_miss, other_node counters. Kernel sysctl documentation: kernel.numa_balancing description and vm.zone_reclaim_mode entry. systemd.exec: NUMAPolicy=, NUMAMask=, CPUAffinity=; systemd.resource-control: AllowedCPUs=, AllowedMemoryNodes=; libvirt domain XML: numatune and vcpupin. Removed the 1.5-2x slowdown figure, EPYC NPS remark, hwloc and /proc/vmstat lines, database interleave recommendations and the reclaim-storm and OOM claims, which were not confirmed. lscpu(1) reports NUMA information; the PCI numa_node attribute is in the kernel ABI documentation.

Method: documentation only; no commands were run.
