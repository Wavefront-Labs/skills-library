---
id: computing-software.digital-forensics-incident-response.evidence-handling.collecting-hiberfil-pagefile-and-crash-dumps
name: collecting-hiberfil-pagefile-and-crash-dumps
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [hiberfil, pagefile, swapfile, crash-dump, memory-acquisition, alternative-memory-sources, dfir]
level: practitioner
status: docs-checked
description: "Collect alternative memory sources on Windows: crash dump types, their default locations and registry settings, and the paging-file location key."
sources: ["https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/memory-dump-file-options", "https://volatility3.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collecting hiberfil, pagefile and crash dumps

**Goal:** recover memory evidence when no live RAM capture exists, or to extend one in time.

## Crash dump types (Microsoft)
Windows can write: complete, kernel, small (64 KB) and active memory dumps.
- **Complete:** records all of system memory at the crash; may contain data from processes that were running. Needs a paging file on a local volume large enough for all physical RAM plus 257 MB. A new complete or kernel dump overwrites the previous one under the conditions the page lists.
- **Kernel:** kernel memory only; excludes unallocated memory and memory allocated to user-mode programs.
- **Small:** the smallest useful set (stop message and parameters, loaded drivers, processor context, the EPROCESS and ETHREAD of the process and thread that stopped, kernel-mode call stack). A new file is created each time, named with the date (for example `Mini022900-01.dmp`), and a list is kept in the `%SystemRoot%\Minidump` folder.
- Registry, under `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\CrashControl`: `CrashDumpEnabled` (0x0 none, 0x1 complete, 0x2 kernel, 0x3 small, 0x7 automatic; 0x1 with `FilterPages` 0x1 is active), `DumpFile` (default `%SystemRoot%\Memory.dmp`), `MinidumpDir` (`%SystemRoot%\Minidump`) and `Overwrite`. Record these settings, as they decide what exists.
- Complete and kernel dumps can be loaded with the Windows debugger.

## Paging files
A relocated paging file is configured under `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PagingFiles` (the page names this value). Check it on the system or in the SYSTEM hive of an image.

## Collecting
These files are in use on a live system and normal copy fails; a raw NTFS reader can copy them (see the skill on copying locked files; the RawCopy README lists pagefile.sys and hiberfil.sys as examples). From an image, extract the files with your forensic suite.

## Analysis
Volatility 3's documentation lists crash dump layers in its framework, so crash dumps can be opened as memory images; confirm format support for your version before relying on it.

## Verify
Record file timestamps and sizes before collection and hash after. A crash dump reflects the time of the crash, so date findings accordingly.

## Checked
Confirmed against Microsoft's memory dump file options page (dump types, sizes, behaviour, small-dump file naming and folder, CrashControl registry values, PagingFiles) and the Volatility 3 documentation index (crash layer module listed). Removed unconfirmed content: hiberfil.sys, pagefile.sys and swapfile.sys content descriptions, Fast Startup behaviour, KAPE/Velociraptor/FTK Imager steps, Hibr2Bin and MemProcFS conversions, `--single-location`, WinDbg and strings advice, `ClearPageFileAtShutdown`, WER dump paths, and the SANS poster (no claims relied on it).

Method: docs-only read of cited pages, 2026-11-09
