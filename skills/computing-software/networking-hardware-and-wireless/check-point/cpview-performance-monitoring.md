---
id: computing-software.networking-hardware-and-wireless.check-point.cpview-performance-monitoring
name: cpview-performance-monitoring
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, cpview, performance, cpu-utilization]
level: practitioner
status: draft
description: "Use CPView to monitor CPU, SecureXL, CoreXL, memory and connection rates on a Check Point gateway, including historical mode."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_PerformanceTuning_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CPView real-time performance monitor

```
cpview                          # interactive, expert or clish
cpview -t                       # (confirm) text/interval modes
cpview history on               # enable history collection
cpview -p "01-NOV-2025 14:20"   # (confirm) time travel in history mode
top -H ; mpstat -P ALL 2
```
- CPView menus: **Overview** (CPU, memory, throughput, connections per second), **SysInfo**, **Network** (interface errors, drops), **CPU** (per-core, top processes), **Advanced** > Firewall, SecureXL, CoreXL (queue lengths, per-instance connections), **Software-blade** counters.
- Use it to check for a single hot CoreXL instance (an elephant flow) versus evenly loaded cores, `fwd` high CPU, or high drops on the NIC.
- History: `cpview history on` stores samples (about a week) so you can look back at an incident with `[` / `]` or "H" mode in the interface; useful because you see before the problem.
- NIC drops/ring buffer: `ethtool -S eth1 | grep -i -E "drop|err|miss"`; `ethtool -g eth1` for ring sizes, and `ethtool -G eth1 rx 2048` to raise if safe.
- Gotcha: reading CPView when the box is already saturated slows other operations; prefer a short session. History mode is not enabled by default in older builds.
- Compare against SmartView Monitor for long-term trends.

Verify: CPView's Overview matches `top` (idle %), and after a tuning change per-instance load becomes even.
