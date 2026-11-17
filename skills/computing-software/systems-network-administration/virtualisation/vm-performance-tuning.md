---
id: computing-software.systems-network-administration.virtualisation.vm-performance-tuning
name: vm-performance-tuning
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [virtualisation, virtualization, performance-tuning, vm-performance, right-sizing, cpu-ready, rdy, co-stop, cstp, esxtop, resxtop, numa, vnuma, cores-per-socket, memory-ballooning, host-swapping, memory-overcommit, davg, kavg, gavg, storage-latency, pvscsi, paravirtual-scsi, vmxnet3, virtio, virtio-scsi, multiqueue, kvm, qemu, cpu-pinning, hugepages, hyper-v, perfmon, power-management, vsphere, proxmox]
level: advanced
status: draft
description: "Find and fix VM slowness: CPU ready/co-stop maths, right-sizing vCPUs, NUMA fit, ballooning vs swapping, DAVG/KAVG storage latency, paravirtual drivers, power policy, KVM/Hyper-V equivalents."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere.html
  - https://www.linux-kvm.org/page/Tuning_KVM
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/role/hyper-v-server/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VM performance tuning — measure contention at the host, then fix the cause

**Goal:** when a VM is "slow", prove whether it is starved by the hypervisor (CPU, memory,
storage or network contention) or just busy inside the guest, and fix the right layer.
Thresholds below are widely used rules of thumb, not vendor limits; baseline your own
environment.

## 0. Guest or host?
Guest tools (Task Manager, `top`) cannot see contention: a starved vCPU just looks idle or
slow. Always pair guest metrics with host metrics for the same minute. If the guest shows
100% CPU and the host shows no ready time, the VM needs more resources or the app needs
tuning; if the guest is moderate and the host shows high ready, the host is the problem.

## 1. CPU
On ESXi use `esxtop` (`c` for CPU view, `e` to expand a VM into its vCPUs):
- **%RDY** — time a vCPU was ready to run but had no physical core. Worry above ~5% per
  vCPU sustained, act above ~10%. In esxtop the VM row sums all vCPUs, so divide by vCPU
  count.
- vCenter charts show **CPU Ready in milliseconds** per sample. Convert:
  `%ready = ready_ms / (interval_s × 1000) × 100`; the real-time interval is 20 s, so
  1,000 ms = 5% (summed across vCPUs).
- **%CSTP** (co-stop) above ~3% means a wide VM is waiting to schedule its vCPUs together.
  The fix is usually **fewer vCPUs**.
- **%MLMTD** non-zero = a CPU limit is set. Remove limits unless intentional.

Right-sizing: oversized VMs are the most common cause of ready time. Start at 2 vCPUs,
grow on measured guest demand. Check the host's vCPU:pCore ratio; above ~4:1 on busy
clusters expect contention (workload-dependent).

## 2. NUMA
- Keep a VM's vCPUs and memory within one physical NUMA node where possible (e.g. on a
  2 × 16-core host, ≤16 vCPUs and less than one socket's RAM).
- Wide VMs: let vSphere build vNUMA (default since 6.5 auto-sizes); leave cores-per-socket
  at the default unless guest licensing needs a socket count, and then match the
  physical topology.
- Hot-add CPU disables vNUMA on many versions; do not enable it on large VMs.
- KVM: `numactl --hardware` on the host, pin with `<numatune>` and `<vcpupin>` in libvirt
  XML for latency-sensitive VMs.

## 3. Memory
esxtop `m` view:
- **MCTLSZ** (balloon size) > 0: host under pressure, guest is paging internally. Tolerable
  briefly.
- **SWCUR / SWR/s** (host swap) > 0: serious, every swapped page read is a disk I/O.
  Add host RAM, migrate VMs, or reduce overcommit.
- Consumed memory ≠ demand; a guest that touched all its RAM once keeps it consumed. Size
  on **active** memory plus guest-reported working set.
- Reservations stop ballooning/swapping for critical VMs but reduce cluster flexibility and
  HA slot sizes. Use sparingly.
- Ballooning needs guest tools/the balloon driver installed; without it the host swaps
  straight away.

## 4. Storage
esxtop `u` (device) or `v` (VM disk):
- **DAVG** — latency at the array/fabric. Sustained > ~20 ms for general VMs (lower for
  databases) = array or path problem.
- **KAVG** — time queued in the hypervisor. > ~2 ms means the queue depth is too small or
  saturated.
- **GAVG** = DAVG + KAVG, what the guest sees.
- Use **paravirtual controllers**: PVSCSI (vSphere) or virtio-scsi (KVM), and spread busy
  disks across up to 4 controllers. NVMe controllers on supported versions.
- KVM: `cache=none` and `io=native` (or io_uring on newer QEMU) for databases; IO threads
  for busy disks.
- Hyper-V: perfmon `Hyper-V Virtual Storage Device\Latency`.

## 5. Network
- **VMXNET3** (vSphere), **virtio-net** with multiqueue (`queues=N` matching vCPUs) on KVM,
  synthetic adapters on Hyper-V. Avoid emulated e1000/legacy adapters.
- Enable RSS in Windows guests; check esxtop `n` for `%DRPRX` (receive drops: guest not
  draining its ring; increase ring size or vCPUs).

## 6. Power and firmware
Set the host BIOS to "OS Controlled" or "Performance" and the hypervisor policy to
High Performance for latency-sensitive clusters. Balanced C-states add wake-up latency
that shows as jitter, not as utilisation.

## Verify
- [ ] Host and guest metrics captured for the same window before any change.
- [ ] Per-vCPU ready < ~5% and co-stop < ~3% after right-sizing.
- [ ] No host swapping; ballooning explained.
- [ ] DAVG and KAVG within your baseline; paravirtual controllers and NICs in use.
- [ ] Large VMs fit a NUMA node or have a correct vNUMA layout.
- [ ] Improvement measured at the application (response time), not just counters.
