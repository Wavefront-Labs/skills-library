---
id: computing-software.general-digital-literacy.basic-troubleshooting.reliability-monitor-and-crash-logs
name: reliability-monitor-and-crash-logs
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-method, reliability-monitor, event-viewer, crash-logs, console-app]
level: intro
status: draft
description: "Use Windows Reliability Monitor and Event Viewer or the Mac Console app to see which app or driver crashed and when, and turn the error into a searchable clue."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/use-reliability-monitor
  - https://support.apple.com/guide/console/welcome/mac
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reliability Monitor and crash logs

## Windows Reliability Monitor (start here)
- Start › type **reliability** › *View reliability history* (or `perfmon /rel`).
- A day-by-day chart: red ✕ = critical events (app stopped working, Windows failed to shut down, BSOD), blue ⓘ = installs and updates.
- Click a day › double-click an event › **View technical details**: *Faulting application name*, *Faulting module* (e.g. `nvlddmkm.sys` = NVIDIA driver, `ntdll.dll` = generic), exception code.
- Pattern-spotting: crashes that start the day after an update or driver install point at it. Uninstall or roll back that item.

## Event Viewer (more detail)
- `eventvwr.msc` › Windows Logs › **System** and **Application**; filter Current Log by *Critical, Error*.
- Useful IDs: **41** Kernel-Power (lost power or hard hang), **6008** unexpected shutdown, **1001** BugCheck (blue screen, with stop code), **1000** Application Error.
- Many red errors are normal noise; focus on ones that match the time of your problem.

## Mac: Console app
- Applications › Utilities › **Console** › *Crash Reports* (app crashes), *Log Reports*, and *Diagnostic Reports* (`.panic` files for kernel panics).
- System Settings › Privacy & Security › Analytics & Improvements › **Analytics Data** lists the same files.

## Turn it into action
- Search the faulting module or event ID with the app name. Update or reinstall the app or driver named; check the vendor's known issues.
- Copy the details into a support request instead of "it keeps crashing".

## Verify
- [ ] After the fix, Reliability Monitor shows no new red ✕ for that app for a week.
