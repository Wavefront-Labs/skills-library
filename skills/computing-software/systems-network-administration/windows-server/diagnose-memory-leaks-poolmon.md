---
id: computing-software.systems-network-administration.windows-server.diagnose-memory-leaks-poolmon
name: diagnose-memory-leaks-poolmon
category: computing-software
field: systems-network-administration
product: windows-server
tags: [performance-monitoring, poolmon, memory-leak, handle-leak, performance-counters]
level: advanced
status: docs-checked
description: "Find kernel memory leaks on Windows Server with PoolMon: watch paged and nonpaged pool allocations by pool tag and map tags to components with pooltag.txt."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/poolmon
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Diagnosing memory leaks

## Kernel pool leak with poolmon
PoolMon (`poolmon.exe`), the Memory Pool Monitor, displays data about memory allocations from the system paged and nonpaged
kernel pools, grouped by pool tag. It can show the names of the Windows components and commonly used drivers that
assign each tag, using `pooltag.txt` installed with PoolMon and the Debugging Tools for Windows. Watch which tag keeps
growing, identify the owning component or driver, then update or remove it.

## Verify
- [ ] After the fix, the counter is flat over a full business cycle.

## Checked

2026-10-28. Confirmed against: PoolMon page (paged and nonpaged pool data grouped by tag, pooltag.txt, Debugging Tools for Windows). Removed (not confirmable from the cited pages): performance counter list, event 2019/2020, Get-Process/Get-Counter examples, user-mode handle/dump advice, poolmon -b switch and keys, findstr driver search, mitigation advice.

Method: documentation only; no commands were run.
