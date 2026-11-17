---
id: computing-software.digital-forensics-incident-response.volatility.dumping-processes-and-memory-regions
name: dumping-processes-and-memory-regions
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [memory-region-dump, procdump-plugin, volatility3, pslist-dump, memmap, process-dump, memory-forensics, dfir]
level: practitioner
status: docs-checked
description: "Dump process executables, DLLs, full address spaces and single VAD regions from a memory image with Volatility 3 and prepare them for static analysis."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.html", "https://volatility3.readthedocs.io/en/latest/vol2to3.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Dumping processes and memory regions for analysis

**Goal:** extract the right bytes for malware analysis: the main image, a specific DLL, an
injected region, or the whole address space, and keep their provenance.

## Volatility 3 dump options
| Need | Volatility 3 |
|---|---|
| Process executable (PE reconstructed from memory) | `windows.pslist --pid PID --dump` |
| Loaded DLLs | `windows.dlllist --pid PID --dump` |
| Every mapped page of a process | `windows.memmap --pid PID --dump` |
| One VAD region | `windows.vadinfo --pid PID --address 0x... --dump` (`--maxsize` skips larger regions) |
| Injected regions found by malfind | `windows.malware.malfind --pid PID --dump` |
| Kernel drivers | `windows.modules --dump` |
| File cache objects | `windows.dumpfiles --pid PID` / `--virtaddr` / `--physaddr` |

`-o` is a global option (`-o` / `--output-dir`) and goes before the plugin name: `vol -f mem.raw -o out/ windows.pslist --pid 4312 --dump`.

## Practical notes
- `pslist --dump` rebuilds the PE from the process image base address with the PE header
  reconstruction (`dos_header.reconstruct()`), so the file is a memory-layout reconstruction.
  Expect it not to match the disk hash and possibly not to run.
  Use it for strings, YARA and disassembly, not execution.
- For packed malware, the memory dump is often *better* than the disk file: it is unpacked.
  You may need to repair the headers before loading it in a disassembler.
- `memmap --dump` writes one `pid.<PID>.dmp` per process containing the mapped pages in
  virtual order (unreadable pages are padded); good for `strings`/`bulk_extractor`/YARA across the full space (URLs, keys, commands).
- Record for each dump: image hash, PID, process name, address, plugin and Volatility
  version. Hash the output (`sha256sum out/*`) into case notes.
- Alternatives: MemProcFS exposes a WinDbg-compatible `minidump.dmp` in each active
  user-mode process's `minidump` directory (not generated for System, Registry, LSASS or
  MemCompression) and a `vmemd` directory per process with one file per memory-map entry
  (unreadable pages are zero padded); open the minidump in WinDbg.

## Gotchas
- Dumping everything for every process produces gigabytes; dump targeted PIDs.
- Antivirus on the analysis box will quarantine dumps; work in an excluded, isolated folder.
- Paged-out regions are missing; acquire the pagefile and combine where the tooling supports it
  (MemProcFS `-pagefile0`).

## Self-check
Each dump on disk has a hash, a PID/address origin and a recorded plugin command.

## Checked

- Confirmed: dump options per plugin, output file naming for memmap, -o is a global output-dir option, MemProcFS -pagefile0 option.

Method: docs-checked 2026-11-09 against volatility3 develop source (plugins windows/pslist.py, dlllist.py, memmap.py, vadinfo.py, dumpfiles.py, modules.py, malware/malfind.py, doc vol2to3.rst) and MemProcFS wiki pages FS_Process_Minidump and FS_Process_VMemD plus README. Removed the Volatility 2 plugin-name column and the pe_unmapper/PE-bear tool claim (not confirmed); dropped the 'imports resolved' claim.
