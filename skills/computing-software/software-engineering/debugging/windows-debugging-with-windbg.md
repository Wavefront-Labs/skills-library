---
id: computing-software.software-engineering.debugging.windows-debugging-with-windbg
name: windows-debugging-with-windbg
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, windows, windbg, crash-dumps, visual-studio-debugger, symbols, time-travel-debugging]
level: advanced
status: docs-checked
description: "Debug Windows crashes and hangs: capture dumps with ProcDump, open them in Visual Studio, and record with WinDbg Time Travel Debugging."
sources: ["https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/", "https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/time-travel-debugging-overview", "https://learn.microsoft.com/en-us/sysinternals/downloads/procdump", "https://learn.microsoft.com/en-us/visualstudio/debugger/using-dump-files"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows debugging with WinDbg / Visual Studio

## Capture a dump with ProcDump (Sysinternals)
ProcDump monitors for CPU spikes, hung windows, unhandled exceptions and performance-counter thresholds. Dump
types: `-mm` Mini (default), `-ma` Full (all memory), `-mt` Triage, `-mp` MiniPlus, `-mk` also a kernel dump.
Examples from the ProcDump page:
```
procdump -ma 4572                  # full dump of PID 4572
procdump -ma -e w3wp.exe           # full dump on a 2nd chance (unhandled) exception
procdump -ma -e 1 w3wp.exe         # 1st or 2nd chance exceptions
procdump -h hang.exe               # mini dump when a window is unresponsive for more than 5 seconds
procdump -n 3 -s 5 -c 20 consume   # up to 3 dumps when CPU exceeds 20% for 5 seconds
procdump -ma -i <dumpfolder>           # install as the (AeDebug) postmortem debugger; -u uninstalls
```
- `-s` is consecutive seconds before the dump is written (default 10); `-n` is the number of dumps.
- `-u` makes CPU relative to a single core; `-r` dumps using a clone to reduce the outage
  (Windows 8.1+ uses PSS); `-accepteula` accepts the license automatically.
- The default file name is `PROCESSNAME_YYMMDD_HHMMSS.dmp`.
- `-mp` dumps CLR processes as Full (`-ma`).

## Open a dump in Visual Studio
- Dumps are snapshots mostly used for machines you cannot access. A dump with heap includes memory and variable
  values; one without heap needs binaries that exactly match those running at dump time.
- File > Open > File, pick the `.dmp`; the Minidump File Summary offers Set symbol paths, Debug with Managed
  Only / Mixed / Native Only, and Run Diagnostic Analysis. To save one while stopped in the debugger:
  Debug > Save Dump As (Minidump, or Minidump with Heap, the default).
- Full debugging needs the matching `.exe`, `.pdb` files and source for the build. A 64-bit dump needs 64-bit
  Visual Studio. It cannot debug the older full user-mode dump format. Kernel-mode dumps and SOS.dll need the
  Debugging Tools for Windows from the WDK.
- Optimised code is confusing in dumps (inlining changes call stacks, variable lifetimes change).

## Time Travel Debugging (TTD)
TTD records a process trace and replays it forwards and backwards in WinDbg.
- Run the debugger elevated (More > Run as Administrator) to record. A `TTD.exe` command-line recorder also exists.
- The trace (`.run`) can reach several gigabytes within minutes; an index file (`.idx`, typically twice the
  trace size) is created when recording stops or a trace opens; `!tt.index` rebuilds it.
- Typical recording slowdown is about 10x-20x.
- Limits: user mode only, read-only playback, cannot record protected processes such as PPL, and anti-virus or
  Electron-based apps can interfere.
- Traces can contain personal or security-related data (file paths, registry, memory); take care sharing them.
- TTD adds debugger data model objects queried with LINQ, and the SOS extension (64-bit) supports managed code.

## Checked
2026-11-09. Confirmed against the ProcDump v12.02 page, the Visual Studio "Dump files" page and the Time Travel
Debugging overview. Removed as not stated in the cited pages: the WinDbg command table (`!analyze`, `.ecxr`,
`~*k`, `!locks`, `!heap`, SOS commands, `bp`), symbol path commands and `msdl` URL, `_NT_SYMBOL_PATH`, WER
LocalDumps registry values, Task Manager and `dotnet-dump` steps, `msvsmon` remote debugging, backwards-step
commands and the `dx` TTD example.
Method: documentation only; no commands were run.
