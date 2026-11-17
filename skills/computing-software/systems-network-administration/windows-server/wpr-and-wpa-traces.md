---
id: computing-software.systems-network-administration.windows-server.wpr-and-wpa-traces
name: wpr-and-wpa-traces
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, performance-monitoring, perfmon, wpr, wpa, windows-performance-toolkit, etw, xperf, cpu-sampling]
level: advanced
status: docs-checked
description: "Record ETW traces with Windows Performance Recorder (wpr): list profiles, start and stop, file vs memory mode, boot traces, then open the .etl in WPA."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-recorder
  - https://learn.microsoft.com/en-us/windows-hardware/test/wpt/wpr-command-line-options
  - https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Performance Recorder and Analyzer

WPR records ETW traces to an `.etl` file; Windows Performance Analyzer (WPA) opens them. Analyse on a
workstation rather than on the server.

## Record
```
wpr -profiles                                  # enumerate profile names and descriptions
wpr -start GeneralProfile -filemode
# reproduce the problem
wpr -status                                    # show the active recording
wpr -stop <path>\slow.etl "problem description"
wpr -cancel                                    # abort the recording
```
- The default recording mode is memory. `-filemode` records to an unbounded file that grows until it
  fills the disk, so watch free space and keep captures short.
- `-start` takes one or more profiles, e.g. `wpr -start CPU` (verbose CPU profile in memory mode) or
  `wpr -start CPU.light -filemode`. Run `wpr -profiles` for the profiles on this machine.
- Boot traces: `wpr -boottrace -addboot <profile>` sets the autologger for the next boot (it does not start
  a trace immediately); after the reboot, `wpr -boottrace -stopboot <file>` removes the autologger, stops
  the boot recording and merges it into the file. `-cancelboot` removes the autologger without saving.
- `-exportprofile` writes a built-in profile to a `.wprp` file for customisation.

## Analyse in WPA
Open the `.etl` in WPA, configure symbol paths (Trace > Configure Symbol Paths) with a local cache and the
Microsoft symbol server `https://msdl.microsoft.com/download/symbols`, then load symbols before reading stacks.

## Verify
- [ ] Trace stops cleanly and opens in WPA with symbols resolved.

## Checked
2026-10-28. Confirmed against the Learn page "WPR command-line options" (`-profiles`, `-start`, `-stop`, `-cancel`, `-status`, `-filemode`, memory default, `-boottrace -addboot/-stopboot/-cancelboot`, `-exportprofile`, example profiles CPU and CPU.light). Removed as unconfirmed: the Windows Server version claim, the list of profile names, circular-buffer wording, the WPA graph guidance, Regions of Interest, `DisablePagingExecutive` and trace-size comments.
Method: documentation only; no commands were run.
