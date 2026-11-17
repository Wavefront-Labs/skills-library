---
id: computing-software.systems-network-administration.windows-server.resource-monitor-and-task-manager-triage
name: resource-monitor-and-task-manager-triage
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, performance-monitoring, perfmon, resource-monitor, resmon, task-manager, live-triage, handle-search]
level: intro
status: draft
description: "Triage a slow server live with Resource Monitor and Task Manager: CPU wait chains, disk queue by file, network by process, memory hard faults and handle search."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-performance-problems-in-windows
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resource Monitor and Task Manager triage

First five minutes on a slow server. Open `resmon` (or Task Manager > Performance > Open
Resource Monitor).

## CPU tab
- Sort processes by Average CPU. Expand **Services** to see which service inside a
  svchost burns CPU.
- Right-click a hung process > **Analyze Wait Chain** shows which thread/process it waits
  on (deadlocks, a blocked network call).
- **Associated Handles** search box: find which process holds a file or registry key
  open (the "file in use" mystery).

## Memory tab
- Hard Faults/sec per process: sustained high values = paging, the real memory pressure
  signal (not "memory used").
- Bar: Hardware Reserved, In Use, Modified, Standby, Free. Little Standby+Free and high
  hard faults = genuinely short of RAM.

## Disk tab
- Disk Activity shows **files** being read/written per process with response time (ms).
  Response time over ~20 ms on SSD/SAN or a queue length that stays high points to
  storage.
- Storage section: Active Time and Disk Queue Length per physical disk.

## Network tab
- Bytes per process and per remote address; TCP connections with latency and packet loss;
  Listening Ports with firewall status.

## Task Manager extras
- Details tab: add columns (Command line, I/O reads/writes, Handles, Threads, GDI objects
  for leaks).
- Users tab on RDS hosts: per-session resource usage.
- Create dump file (Details > right-click) for a hung process to send to the vendor.

## Then
Capture evidence before restarting anything: a short perfmon log or WPR trace. Restarting
destroys the data you need for root cause.

## Checklist
- [ ] Culprit process/service and resource identified; evidence captured.
