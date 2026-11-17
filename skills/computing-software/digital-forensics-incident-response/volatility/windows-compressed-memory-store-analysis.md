---
id: computing-software.digital-forensics-incident-response.volatility.windows-compressed-memory-store-analysis
name: windows-compressed-memory-store-analysis
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [memory-compression-store, windows-10-memory-compression, memcompression, memprocfs, memory-forensics, dfir]
level: advanced
status: docs-checked
description: "Account for the Windows 10 compressed memory store (MemCompression): what it hides from plugins and YARA, tools that decompress it, and how to report limits."
sources: ["https://github.com/mandiant/win10_volatility", "https://github.com/ufrisk/MemProcFS/wiki", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows compressed memory store

On Windows 10, a process's virtual memory may map to physical memory, to a page file or to compressed memory (the `MemCompression` process appears in MemProcFS process listings). Pages held in the compressed store are not directly readable by tools that only parse physical pages and page tables.

## Impact
- Strings, YARA and similar scans over the raw image can miss data inside compressed pages (practitioner inference).
- Per-process dumps and virtual-memory views can have holes where pages are not readable; MemProcFS zero-pads unreadable pages in `vmemd` and `memory.vmem`.

## Tools
- **win10_volatility** (Mandiant, a Volatility 2 fork): adds address spaces `Win10CompressedIA32PagedMemoryPae`, `Win10CompressedIA32PagedMemory` and `Win10CompressedAMD64PagedMemory` that let plugins read previously unreadable compressed data on supported Windows 10 profiles (1607 to 1809 are listed). Check that "AS Layer 1" in `imageinfo` reports one of them. Decompression relies on the address of `nt!SmGlobals`. A page it cannot read has likely been paged out and cannot be recovered. The README is Python 2 era.
- **MemProcFS**: virtual memory access includes Windows 10 compressed memory (`cache_paging_enable.txt` in the config file system enables virtual memory including Win10 compressed memory). Its API has a `FLAG_NOPAGING` option to skip paged-out and compressed retrieval. The `minidump` output is not generated for MemCompression itself.
- **Volatility 3**: no compressed-memory layer was found in the current develop source (layers and Windows plugins) when checked on 2026-11-09; re-check release notes before relying on it, and cross-check findings with MemProcFS.
- A page file can be supplied to MemProcFS with `-pagefileX` for additional paged-out content.

## Practice
1. Note the OS build (`windows.info`) and which tool was used.
2. For negative YARA results on a Windows 10 image, rerun with a tool that decompresses before concluding absence.
3. When dumping a suspicious process, compare dump completeness across tools.
4. Report the limitation explicitly when only non-decompressing tools were used.

## Verify
The analysis notes state which tools handled compressed pages, and key negative findings were checked with a decompressing tool.

## Checked

- Confirmed: win10_volatility address spaces, supported-profile table, imageinfo check, SmGlobals dependency; MemProcFS statements on compressed memory, cache_paging_enable, minidump limits; no compression layer in Volatility 3 source.

Method: docs-checked 2026-11-09 against the win10_volatility README and CHANGELOG, MemProcFS wiki (FS_Process, FS_Process_VMemD, FS_Process_Minidump, FS_Conf, API_Python_Base) and volatility3 develop source. The Mandiant blog returned only site boilerplate and the Microsoft page is unreadable here, so both were dropped along with the Xpress, Server 2016, Get-MMAgent, Disable-MMAgent and hibernation claims. Impact statements marked as inference are practitioner guidance.
