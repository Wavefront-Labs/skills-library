---
id: computing-software.cloud-infrastructure-engineering.azure.vm-performance-diagnostics-perfinsights
name: vm-performance-diagnostics-perfinsights
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vm-troubleshooting, perfinsights, performance-diagnostics, disk-throttling, high-cpu]
level: practitioner
status: docs-checked
description: "Diagnose slow Azure VMs with Performance Diagnostics (PerfInsights): scenarios, running from portal or standalone, reading findings, and VM/disk throttling metrics."
sources: ["https://learn.microsoft.com/troubleshoot/azure/virtual-machines/windows/performance-diagnostics", "https://learn.microsoft.com/troubleshoot/azure/virtual-machines/windows/how-to-use-perfinsights", "https://learn.microsoft.com/azure/virtual-machines/disks-metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM performance diagnostics (PerfInsights)

**Goal:** turn "the VM is slow" into a specific bottleneck (CPU, memory, disk throttling, config) with evidence.

## Check platform throttling first (metrics)
| Metric | Throttled when |
|---|---|
| VM Cached IOPS / Bandwidth Consumed Percentage | Near 100 percent: the VM size's cached limit is being hit |
| VM Uncached IOPS / Bandwidth Consumed Percentage | Near 100 percent: the VM size's uncached limit is being hit |
| Data Disk and OS Disk IOPS Consumed Percentage | Near 100 percent: the provisioned disk IOPS limit is hit |
| Data Disk and OS Disk Bandwidth Consumed Percentage | Near 100 percent: the provisioned disk throughput limit is hit |
| Used Burst IO / BPS Credits Percentage (data and OS disk, VM uncached) | Accumulated burst used; emitted every five minutes |

## Run Performance Diagnostics
Performance diagnostics installs a VM extension that runs the PerfInsights tool (Windows and Linux) and stores insights and
reports in a storage account; the VM needs outbound network access to it. Modes: **continuous** (data collected every five
seconds, updates uploaded every five minutes, for high CPU, memory and disk usage) and **on-demand** (deeper data at a
single moment). On-demand scenarios:
- **Quick performance analysis**: basic overview of configuration and performance, event logs, disk configuration and network usage.
- **Performance analysis**: resource consumption, known issues, best practice analysis and diagnostic data collection.
- **Benchmarking**: runs a Diskspd benchmark (IOPS and MBPS) on all attached drives.
- **Advanced performance analysis**: choose traces to run in parallel (Performance Counter, Xperf, Network, StorPort).
Access needs differ for running, viewing and downloading reports (storage account keys or managed identity roles); check the
permissions table in the Learn article.

## Gotchas
- Benchmarking and advanced analysis can affect the system and should not run on a live production system; use a maintenance window.

## Verify
- [ ] Bottleneck identified with a metric and a finding; fix applied; the consumed-percentage metrics no longer sit near 100 percent.

## Checked
2026-10-28. Confirmed in Learn performance-diagnostics and disks-metrics: consumed-percentage and burst credit metric names, five second and five
minute collection, modes, on-demand scenarios, benchmark and advanced warnings, extension and storage account behaviour. Removed:
standalone PerfInsights.exe and perfinsights.py commands, extension names, CPU Credits Remaining and Available Memory Bytes rows,
the typical findings list, the data-consent gotcha, the 80 percent target.
Method: documentation only; no commands were run.
