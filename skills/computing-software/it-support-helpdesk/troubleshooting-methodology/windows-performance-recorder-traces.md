---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.windows-performance-recorder-traces
name: windows-performance-recorder-traces
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, windows-performance-recorder, wpr, wpa, etw, boot-trace, performance]
level: practitioner
status: draft
description: "Capture and read Windows Performance Recorder traces: wpr profiles and commands, boot traces, opening in WPA with symbols, and the graphs that explain CPU, disk and hangs."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder"
  - "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/wpr-command-line-options"
  - "https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# windows-performance-recorder-traces

WPR (inbox on Windows 10/11) records ETW events; WPA (Windows ADK / Microsoft Store)
analyses them. Use it when Perfmon says "CPU/disk is busy" but not why, or for hangs and
slow boots.

## Capture a repro (elevated)
```cmd
wpr -start GeneralProfile -start CPU -start DiskIO -filemode
:: reproduce the problem, ideally under 60 seconds
wpr -stop "%TEMP%\slow.etl" "App freezes when saving"
wpr -cancel   :: if you need to abandon
```
- `-filemode` writes to disk instead of memory; use it for longer captures.
- Keep captures short; traces grow by hundreds of MB per minute.

## Boot and logon
```cmd
wpr -boottrace -addboot GeneralProfile -filemode
:: reboot, sign in, wait for desktop to settle
wpr -boottrace -stopboot "%TEMP%\boot.etl"
```

## Reading it in WPA
1. Configure symbol paths (Trace > Configure Symbol Paths, include
   `srv*https://msdl.microsoft.com/download/symbols`) and Load Symbols.
2. Graph Explorer:
   - **Computation > CPU Usage (Sampled)**: group by Process, then Stack to find the hot
     function and module (AV filter drivers, a bad add-in).
   - **CPU Usage (Precise)**: waits and who readied a thread, for hangs.
   - **Storage > Disk Usage**: which process and file drove I/O.
   - **System Activity > Regions of Interest / Generic Events** for boot phases.
3. Zoom to the time the user marked; the stop comment helps you find it.

## Gotchas
- Traces contain process names, file paths and possibly user data; handle accordingly.
- Without symbols stacks show only module names; still useful for spotting third-party
  drivers.
- Antivirus and EDR minifilters often top Disk and CPU stacks; check exclusions before
  blaming them.

## Verify
The trace shows the problem window, the responsible process/driver is identified with a
stack, and the fix removes that pattern in a second trace.
