---
id: computing-software.digital-forensics-incident-response.volatility.analysing-crash-dumps-and-converting-memory-formats
name: analysing-crash-dumps-and-converting-memory-formats
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [crash-dump-analysis, memory-dmp, windbg, volatility3, memprocfs, format-conversion, memory-forensics, dfir]
level: advanced
status: draft
description: "Analyse Windows crash dumps (MEMORY.DMP, kernel and minidumps) in WinDbg and Volatility, and convert between raw, dmp, vmem and ELF core formats."
sources: ["https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/varieties-of-kernel-mode-dump-files", "https://github.com/ufrisk/MemProcFS", "https://volatility3.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Analysing crash dumps and converting memory formats

**Goal:** use crash dumps as memory evidence, and move images between formats so every tool
in the kit can read them.

## Dump types (what you can and cannot get)
| Type | Contents | Forensic value |
|---|---|---|
| Complete memory dump | all physical RAM | full memory analysis |
| Kernel memory dump | kernel space only | drivers, kernel objects, rootkits; no user process pages |
| Automatic / active dump (Win10+) | kernel (+ active user pages for active) | like kernel dump |
| Small (minidump, `\Windows\Minidump\*.dmp`) | stack, loaded modules, a few pages | crash cause and loaded driver list only |
A crash may itself be evidence: BYOVD driver loads, rootkit faults and LSASS tampering often
bugcheck.

## WinDbg essentials
```
.symfix ; .reload
!analyze -v            # bugcheck code, faulting module, stack
lm t n                 # loaded modules with timestamps; unknown drivers stand out
!process 0 0           # process list (complete/kernel dumps)
!drvobj <name> 2       # driver object and dispatch routines (hooked IRP handlers)
```

## Volatility and MemProcFS
- Volatility 3 reads Windows crash dump headers directly (`vol -f MEMORY.DMP windows.info`);
  `windows.crashinfo` prints the dump header (bugcheck, dump type).
- MemProcFS mounts `.dmp`, raw, `.vmem`, LiME and others: `MemProcFS.exe -device MEMORY.DMP`.

## Conversions
| From -> to | Tool |
|---|---|
| raw -> crash dump (for WinDbg) | Volatility 2 `raw2dmp -O out.dmp`; MemProcFS exposes a generated dump as `memory.dmp` in its virtual file system root |
| crash dump -> raw | Volatility 2 `imagecopy -O out.raw` |
| VMware `.vmsn/.vmss + .vmem` -> dmp/core | `vmss2core -W snap.vmsn snap.vmem` (Windows dump), `-M` macOS, plain for ELF core |
| EWF-compressed memory (`.E01`) -> raw | `ewfexport -t mem -f raw mem.E01` |
| LiME -> raw | Volatility reads LiME natively; no conversion usually needed |
Hash both input and output and record the tool version; conversions are a documented step in
the chain of custody, not a silent transformation.

## Gotchas
- A kernel dump will not answer user-process questions; say so in the report.
- Crash dumps can be disabled or overwritten; check `HKLM\SYSTEM\CurrentControlSet\Control\CrashControl`
  (`CrashDumpEnabled`, `DumpFile`) to know what should exist.

## Self-check
You know the dump type, what it cannot contain, and you can open the same evidence in at least
two tools with consistent results.
