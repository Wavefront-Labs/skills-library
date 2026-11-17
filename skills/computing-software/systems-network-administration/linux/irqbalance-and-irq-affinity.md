---
id: computing-software.systems-network-administration.linux.irqbalance-and-irq-affinity
name: irqbalance-and-irq-affinity
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, irqbalance, irq-affinity, smp-affinity, interrupts, rss, rps, numa, network-tuning, softirq, sysadmin]
level: practitioner
status: docs-checked
description: "Spread or pin hardware interrupts: read /proc/interrupts, configure irqbalance (banned CPUs, hints), set smp_affinity manually for NIC queues, and RPS for single-queue NICs."
sources:
  - https://docs.kernel.org/core-api/irq/irq-affinity.html
  - https://docs.kernel.org/networking/scaling.html
  - https://github.com/Irqbalance/irqbalance
  - https://docs.kernel.org/core-api/irq/irq-affinity.html
  - https://github.com/Irqbalance/irqbalance/blob/master/irqbalance.1
  - https://github.com/Irqbalance/irqbalance/blob/master/misc/irqbalance.env
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# irqbalance and IRQ affinity

**Goal:** stop one CPU drowning in interrupts (100 % `si`/`hi` in `top` on CPU0 while others
idle), keep NIC interrupts on the NIC's NUMA node, and isolate CPUs for latency work.

## 1. Look
```bash
watch -d -n1 "grep -E 'CPU|eth0|nvme|mlx' /proc/interrupts"   # per-CPU counts per IRQ line
mpstat -P ALL 1                      # %irq and %soft per CPU
cat /proc/softirqs                   # NET_RX imbalance
cat /sys/class/net/eth0/device/numa_node
ethtool -l eth0                      # combined/rx/tx channel (queue) counts
```

## 2. irqbalance (default answer)
```bash
systemctl enable --now irqbalance
irqbalance --oneshot --debug | less        # run once and exit, printing debug output
# /etc/sysconfig/irqbalance  (Debian: /etc/default/irqbalance)
IRQBALANCE_BANNED_CPULIST=2-7              # CPUs that get no IRQs on rebalance (older: IRQBALANCE_BANNED_CPUS bitmask)
IRQBALANCE_ARGS="--policyscript=/etc/irqbalance.d/policy.sh"   # extra daemon arguments, see irqbalance(1)
```
irqbalance distributes interrupts across CPUs based on load. Keep it for most servers; when you pin IRQs by hand, ban them
(`--banirq=<irqnum>` leaves a banned IRQ's affinity alone) or disable irqbalance.

## 3. Manual affinity
```bash
cat /proc/irq/45/smp_affinity_list        # e.g. 0-15
echo 4 > /proc/irq/45/smp_affinity_list   # pin IRQ 45 to CPU 4
echo 0f > /proc/irq/45/smp_affinity       # hex mask form (CPUs 0-3)
```
For multi-queue NICs, pin each queue's IRQ to a distinct core on the NIC's NUMA node
(look IRQ numbers up by name in `/proc/interrupts` each time). Persist manual settings with a oneshot systemd unit, since
IRQ numbers can change across reboots.

## 4. Single-queue NIC: RPS/XPS
RPS and RFS (`/sys/class/net/<dev>/queues/rx-<n>/rps_cpus`, `net.core.rps_sock_flow_entries`) spread receive processing across CPUs; see the kernel networking documentation (scaling) for the mask format and flow-table sizing.

## Gotchas
- Pinning every IRQ to one CPU caps interrupt-heavy throughput.
- `isolcpus=`/`nohz_full=` CPUs can still receive IRQs unless you ban them from irqbalance and set the `irqaffinity=` boot parameter (the default IRQ affinity mask).

## Verify
- [ ] `/proc/interrupts` counts increase on the intended CPUs only.
- [ ] Under load, `mpstat` shows %soft spread instead of one CPU at 100 %.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (core-api irq-affinity), the irqbalance `irqbalance(1)` and `irqbalance.env` sources, and kernel-parameters on 2026-10-26. Confirmed: `/proc/irq/<n>/smp_affinity` (bitmask) and `smp_affinity_list` (CPU list), `IRQBALANCE_BANNED_CPULIST` and the older `IRQBALANCE_BANNED_CPUS`, `IRQBALANCE_ARGS`, `--oneshot`, `--debug`, `--banirq`, `--policyscript`, `irqaffinity=`, `isolcpus=`, `nohz_full=`. Removed: 10-second interval claim, vendor script names, managed-IRQ EIO behaviour, `effective_affinity_list`, RPS mask and flow-entry values, VM and cloud-image claims.

Method: documentation only; no commands were run.
