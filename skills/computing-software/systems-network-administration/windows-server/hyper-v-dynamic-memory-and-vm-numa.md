---
id: computing-software.systems-network-administration.windows-server.hyper-v-dynamic-memory-and-vm-numa
name: hyper-v-dynamic-memory-and-vm-numa
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dynamic-memory, vm-numa, hyper-v, memory-buffer, numa-spanning, set-vmmemory]
level: practitioner
status: gated
description: "Configure Hyper-V VM memory: static vs dynamic memory, startup, minimum, maximum and buffer, virtual NUMA, NUMA spanning and when to use static RAM."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmmemory
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Hyper-V VM memory: dynamic memory and virtual NUMA

## Dynamic memory settings
```powershell
Set-VMMemory -VMName app01 -DynamicMemoryEnabled $true `
  -StartupBytes 4GB -MinimumBytes 2GB -MaximumBytes 16GB -Buffer 20 -Priority 50
Get-VMMemory app01
Get-VM app01 | Select-Object Name, MemoryAssigned, MemoryDemand, MemoryStatus
```
- **Startup** (`-StartupBytes`), **Minimum** (`-MinimumBytes`), **Maximum** (`-MaximumBytes`), **Buffer** (`-Buffer`, a
  percentage of headroom) and **Priority** (`-Priority`, who wins when the host is short) are `Set-VMMemory` parameters;
  read the cmdlet page for their exact meaning and limits.

## When to use static memory
- Applications whose vendor guidance says to use static memory (check each product's virtualization guidance).
- Latency-sensitive workloads where balloon/hot-add delays hurt.

## Virtual NUMA
Virtual NUMA settings interact with the memory mode; check Microsoft's Hyper-V virtual NUMA documentation for how dynamic memory affects it.
```powershell
Get-VMHostNumaNode                                   # physical nodes, memory, processors
Get-VMProcessor app01 | Select MaximumCountPerNumaNode, MaximumCountPerNumaSocket
Set-VMProcessor app01 -MaximumCountPerNumaNode 16
Set-VMMemory app01 -MaximumAmountPerNumaNodeBytes 64GB
```
- Keep the defaults unless you have a reason; keep cluster hosts' NUMA layouts alike.
- **NUMA spanning** is a host setting (`Set-VMHost -NumaSpanningEnabled`); read its page before changing it.

## Capacity planning
- Host reserve: leave memory for the parent partition and per-VM overhead.
- Watch the Dynamic Memory performance counters and each VM's `MemoryDemand`/`MemoryStatus`.
- Over-commit with dynamic memory carefully; paging inside guests is worse than giving them RAM.

## Verify
- [ ] VMs with vendor-mandated static memory use it; dynamic VMs show a healthy `MemoryStatus`.
- [ ] Virtual NUMA settings consistent across cluster hosts; no VM fails to start due to NUMA spanning.

## Checked
2026-10-28. Confirmed on the Learn Set-VMMemory page: -DynamicMemoryEnabled, -StartupBytes, -MinimumBytes, -MaximumBytes, -Buffer, -Priority
and -MaximumAmountPerNumaNodeBytes exist on Set-VMMemory. Removed as unconfirmed: runtime resize rules and Server 2016
gate, Exchange/SQL/SharePoint statements, dynamic memory and virtual NUMA interaction, NUMA spanning behaviour, performance
counter names and pressure threshold, live-migration NUMA statement. Get-VMMemory, Get-VMHostNumaNode and the
Set-VMProcessor NUMA parameters were not checked on their pages (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
