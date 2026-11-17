---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.memory-pressure-and-paging
name: memory-pressure-and-paging
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, memory-pressure, paging, commit-charge, memory-leak, rammap, resource-exhaustion]
level: practitioner
status: draft
description: "Diagnose low-memory slowness: read Task Manager commit and cache figures, hard faults in Resource Monitor, resource-exhaustion events, leak hunting and pagefile sizing."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/introduction-to-the-page-file"
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/rammap"
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/poolmon"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# memory-pressure-and-paging

## Read the numbers (Task Manager > Performance > Memory)
- **In use** vs total: high in-use alone is fine; Windows uses free RAM for cache.
- **Committed x / y GB**: x near y (the commit limit = RAM + page file) means apps will fail
  to allocate; "Your system is low on memory" follows (Resource-Exhaustion-Detector event
  2004 in System log names the top consumers).
- **Paged / Non-paged pool**: non-paged over about 1-2 GB on a workstation suggests a driver
  leak.

## Is it actually paging?
Resource Monitor (`resmon`) > Memory: **Hard Faults/sec** sustained in the hundreds with
low available memory and disk busy = paging is the slowdown. Hard faults alone from file
mapping at app start are normal.

## Find the consumer
- Details tab, add columns "Commit size" and "Memory (private working set)"; sort.
- Leak: a process's Private Bytes rises steadily over hours without dropping (Perfmon over a
  day; see performance-monitor-counters-and-data-collector-sets).
- Driver pool leak: `poolmon` (WDK) sorted by bytes shows the pool tag; look up the tag's
  driver and update it.
- RAMMap shows where physical memory went (standby, driver locked, mapped files).

## Fix
- Close or update the leaking app; browser with dozens of tabs is the usual "leak".
- Leave the page file System managed; disabling it causes crashes and no dumps.
- Add RAM when committed regularly exceeds physical RAM for the real workload; 16 GB is a
  sane baseline for office workloads with Teams and a browser.

## Gotchas
- Memory compression shows as "Compressed" in the System process; not a leak.
- VMs with dynamic memory can look starved while the host is short.

## Verify
During normal work, commit stays well below the limit, hard faults/sec are low, no new
2004 events, and the user reports the slowdown gone.
