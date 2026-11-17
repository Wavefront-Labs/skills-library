---
id: computing-software.systems-network-administration.windows-server.stop-errors-and-memory-dump-analysis
name: stop-errors-and-memory-dump-analysis
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, boot-troubleshooting, winre, bugcheck, memory-dump, windbg, kernel-dump, analyze-v, crashdump-config]
level: advanced
status: docs-checked
description: "Handle stop errors (BSOD) on servers: crash dump type settings, page file sizing for complete dumps, minidump location and starting a WinDbg analysis."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/memory-dump-file-options
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/analyzing-a-kernel-mode-dump-file-with-windbg
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stop errors and memory dump analysis

## Make sure a dump is written
```powershell
Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\CrashControl' | Select CrashDumpEnabled,DumpFile,AutoReboot,MinidumpDir
```
CrashDumpEnabled values: 0 none, 1 complete, 2 kernel, 3 small (64 KB), 7 automatic;
1 with `FilterPages` = 1 is an active memory dump. The kernel dump is the most useful
for most purposes and is smaller than a complete dump.
- A complete dump needs a paging file on a local volume of at least all physical RAM
  plus 257 MB.
- A small dump needs a paging file of at least 2 MB on the boot volume.
- Keep free space on the dump volume at least the size of the dump; check the volume
  before relying on a dump.

## Collect
- Small dumps are listed in `%SystemRoot%\Minidump`, one new file per stop.
- Take the large dump file path from the `DumpFile` value above, not from memory.

## Analyse with WinDbg
Start WinDbg with the `-z` option and the dump file. For kernel or small dumps you
may need to set the executable image path to the files in memory at the crash. Begin
with `!analyze`, which performs automatic analysis of the dump. Symbols come from the
Microsoft symbol server (`https://msdl.microsoft.com/download/symbols`) into a local
cache folder. A third-party driver in the faulting stack is the usual culprit: update
or remove it.

## Verify
- [ ] Dump analysed, module identified, fix (driver/firmware update) applied, and no repeat stop.

## Checked
2026-10-28. Confirmed against "Memory dump file options for Windows" (CrashDumpEnabled values 0/1/2/3/7, FilterPages active dump, 257 MB, 2 MB small-dump page file, Minidump folder) and "Analyzing a kernel-mode dump file with WinDbg" (`-z`, executable image path, `!analyze`). Removed as unconfirmed: the "default" claim for automatic, DedicatedDumpFile, CrashOnCtrlScroll and NMI crash steps, the bugcheck code table, `!analyze -v` field names, MEMORY.DMP path, and the 30-day check.
Method: documentation only; no commands were run.
