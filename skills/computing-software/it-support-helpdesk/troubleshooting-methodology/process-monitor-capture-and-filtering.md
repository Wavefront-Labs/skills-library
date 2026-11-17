---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.process-monitor-capture-and-filtering
name: process-monitor-capture-and-filtering
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, evidence-gathering, log-analysis, procmon, process-monitor, sysinternals, access-denied, name-not-found, boot-logging, pml]
level: advanced
status: draft
description: "Use Sysinternals Process Monitor to find the file, registry key or permission behind an app failure: capture, filters, ACCESS DENIED hunting, boot logging, and sharing PML files."
sources:
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/procmon"
  - "https://learn.microsoft.com/en-us/sysinternals/"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/application-hang-or-crash"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# process-monitor-capture-and-filtering

Goal: when an app fails with a vague error, see exactly which file,
registry key or network call it tried and what result it got.

## Capture
1. Run `Procmon64.exe` as admin (or `procmon /AcceptEula` from a share).
2. Capture starts immediately — Ctrl+E toggles; Ctrl+X clears. Start
   clean, reproduce the problem once, stop capture. Captures grow by
   hundreds of thousands of events per minute.
3. Options → **Drop Filtered Events** for long captures to save memory;
   or use a backing file (File → Backing Files).

## Filter (Ctrl+L)
- `Process Name is app.exe` → Include (add child processes too).
- Hide noise: Procmon itself, System, Explorer unless relevant.
- Result filters that find problems:
  - `Result is ACCESS DENIED` — permissions (standard user app needing
    admin).
  - `Result is NAME NOT FOUND` / `PATH NOT FOUND` — missing file/key (many
    are normal probing — look at those right before the error).
  - `Result is SHARING VIOLATION` — file locked by another process.
- Tools → **Process Tree** shows launch chain; **Count Occurrences** finds
  hot paths.
- Find the error moment: note the clock time when the error dialog
  appeared, jump there (Ctrl+F for the error text sometimes appears in a
  WriteFile to a log).

## Boot logging
Options → Enable Boot Logging captures from early boot (logon scripts,
startup delays, services). Reboot, run Procmon after logon to save the log.

## Share
File → Save → PML (all or filtered events) — send to L3/vendors; it
contains paths/usernames, handle as sensitive.

## Typical findings
- App writes to `Program Files` or HKLM as standard user → grant narrow
  permission or fix install.
- DLL loaded from an unexpected path (old version in app folder).
- AV/DLP filter (`fltmgr` stacks) causing delays — check Duration column.

## Gotchas
- Leaving Procmon running fills memory and slows the machine — stop
  capture.
- Don't change permissions broadly based on one ACCESS DENIED; confirm it
  correlates with the failure.

## Verify
After applying the fix suggested by the capture, a new capture shows the
operation SUCCESS and the app works.
