---
id: computing-software.systems-network-administration.virtualisation.vsan-performance-service-and-proactive-tests
name: vsan-performance-service-and-proactive-tests
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan-performance-diagnostics, vsan-performance-service, vsan-iotop, hcibench, vsan, vmware, vsphere]
level: advanced
status: draft
description: "Use the vSAN performance service, performance diagnostics, I/O Insight and proactive tests or HCIBench to find latency sources and validate a vSAN cluster."
sources:
  - https://flings.vmware.com/hcibench
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSAN performance service and proactive tests

**Goal:** know whether vSAN is the bottleneck and where (VM, host, disk, network).

## Turn on the performance service
Cluster -> Configure -> vSAN -> Services -> Performance service: Enabled (stats object stored on vSAN with a policy you choose). Enable *verbose mode* only while troubleshooting; *network diagnostic mode* briefly.

## Read the stats
Cluster -> Monitor -> vSAN -> Performance, tabs:
- **VM**: IOPS, throughput, latency per VM/virtual disk.
- **Backend**: resync and recovery traffic vs front-end; high backend latency with resync = rebuild impact.
- **Disks**: per disk group cache/capacity latency, write buffer fill, destaging (OSA). A full write buffer with slow destage means capacity tier too slow.
- **Physical adapters/host network**: packet loss, TCP retransmits. Any loss on the vSAN vmk is serious.

## Performance diagnostics
Monitor -> vSAN -> Performance diagnostics: pick a goal (max IOPS, max throughput, min latency) and time range; it gives findings with KB links. Requires CEIP.

## I/O Insight / vsantop
- I/O Insight (VM -> Monitor -> vSAN -> I/O Insight) traces a VM's I/O size, randomness and read/write mix for a window.
- Host shell: `vsantop` (esxtop-like) for live vSAN metrics.

## Proactive tests and HCIBench
- Cluster -> Monitor -> vSAN -> Proactive tests: *VM creation test* (functional), *network performance test* (multicast/unicast throughput between hosts).
- HCIBench (fling OVA): deploys worker VMs, drives fio/vdbench profiles, and reports IOPS/latency. Run before go-live and after major changes; clean up workers after.

## Gotchas
- Benchmarks on a production cluster steal I/O from VMs; run in a maintenance window.
- Compare the same block size and outstanding I/O; a 4K random read number is not comparable to a 256K sequential write one.

## Verify
Baseline report saved; production latencies compared against it during incidents.
