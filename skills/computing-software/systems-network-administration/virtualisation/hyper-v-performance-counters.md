---
id: computing-software.systems-network-administration.virtualisation.hyper-v-performance-counters
name: hyper-v-performance-counters
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-perfmon, hyper-v-counters, performance-monitoring, cpu-wait-time-per-dispatch, dynamic-memory-pressure, windows-server]
level: advanced
status: docs-checked
description: "Measure Hyper-V host and VM performance with the right counters: hypervisor logical and virtual processor run time, root VP time, memory balancer, network throughput."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/role/hyper-v-server/detecting-virtualized-environment-bottlenecks
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/role/hyper-v-server/configuration
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/role/hyper-v-server/memory-performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V performance counters

**Goal:** find real CPU, memory, storage and network bottlenecks on Hyper-V hosts. Always measure physical CPU use
with the Hyper-V Hypervisor Logical Processor counters: the CPU counters that Task Manager and Performance Monitor
report in the root and child partitions do not reflect actual physical CPU usage.

## CPU
| Counter | How Microsoft reads it |
|---|---|
| `\Hyper-V Hypervisor Logical Processor(*)\% Total Run Time` | `_Total` over 90%: the host is overloaded; add processing power or move VMs |
| `\Hyper-V Hypervisor Virtual Processor(*)\% Total Run Time` | over 90% on all of a VM's vCPUs: check the host is not overloaded, check the workload can use more vCPUs, then add vCPUs. Over 90% on only some: consider vRSS for receive-heavy network loads, virtual NUMA and more virtual disks for storage-heavy loads |
| `\Hyper-V Hypervisor Root Virtual Processor(*)\% Total Run Time` | over 90% on some root VPs, with `Processor(x)\% Interrupt Time` plus `% DPC Time` adding up to roughly the same value: enable VMQ on the network adapters |

## Memory
| Counter | Meaning |
|---|---|
| `\Hyper-V Dynamic Memory Balancer(*)\Available Memory` | memory the host can still assign; when it is low, stop starting more VMs or move some away |
| `\Memory\Available MBytes` | check on the host and inside each VM |

## Network
`\Hyper-V Virtual Network Adapter(*)\Bytes/sec`: at or above 250 MBps, Microsoft's guidance is
to add teamed network adapters in the VM, enable vRSS and use SR-IOV.

## Storage
Read the storage I/O performance and bottleneck pages in the Hyper-V performance-tuning section for the storage
counters and their guidance; compare virtual disk activity with the host's physical disk counters. List the counters
available on your host with `Get-Counter -ListSet 'Hyper-V*'`.

## Capture
```powershell
$c = '\Hyper-V Hypervisor Logical Processor(_Total)\% Total Run Time',
     '\Hyper-V Hypervisor Virtual Processor(*)\% Total Run Time',
     '\Hyper-V Dynamic Memory Balancer(*)\Available Memory'
Get-Counter -Counter $c -SampleInterval 15 -MaxSamples 240 | Export-Counter -Path hv-baseline.blg
```
Build a baseline when healthy; compare during incidents.

## Verify
Baseline file opens in Performance Monitor with all counters populated; alert thresholds come from baseline
percentiles, not guesses.

## Checked

Date checked: 2026-10-27. Documentation: "Detecting bottlenecks in a virtualized environment", "Hyper-V server configuration" and "Hyper-V memory performance" (windowsserverdocs main branch, Windows Server 2025).
Confirmed: counter names above and the 90% (logical, virtual and root processor) and 250 MBps (network adapter) guidance; the statement that Task Manager and root or child partition CPU counters do not show physical CPU use.

Method: documentation only; no commands were run.
