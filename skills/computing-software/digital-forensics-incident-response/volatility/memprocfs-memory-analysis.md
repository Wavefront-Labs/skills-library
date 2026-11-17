---
id: computing-software.digital-forensics-incident-response.volatility.memprocfs-memory-analysis
name: memprocfs-memory-analysis
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [memprocfs, memory-forensics, memory-image-formats, fuse, forensic-mode, dfir]
level: practitioner
status: docs-checked
description: "Analyse memory images with MemProcFS: mounting as a virtual file system, forensic mode outputs, timelines, process and registry views, and YARA, as a complement to Volatility."
sources: ["https://github.com/ufrisk/MemProcFS", "https://github.com/ufrisk/MemProcFS/wiki"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MemProcFS memory analysis

**Goal:** browse a memory image as files and folders and get fast, broad forensic output that
complements Volatility's plugin-by-plugin approach.

## Run
```bash
# Linux (FUSE) or Windows (Dokany)
memprocfs -device mem.raw -mount /mnt/mem -forensic 1        # forensic mode 1 = in-memory only SQLite database
memprocfs -device mem.raw -mount M -forensic 1 -license-accept-elastic-license-2-0
```
The `-device` option accepts raw dump files, Microsoft full crash dump files, ELF full core
dumps (VirtualBox), live memory via DumpIt or WinPMEM, and PCILeech FPGA hardware. On Windows
mounting needs the Dokany driver (mounts as `M:` by default); on Linux, FUSE, and `-mount`
takes the mount path. Hyper-V virtual machines are parsed natively (64-bit builds only);
native VMware/VirtualBox hypervisors are not parsed as VMs.

## Layout highlights
- `/name/` and `/pid/<pid>/`: per-process `memory.vmem`, `win-cmdline.txt`,
  `win-environment.txt`, `memmap` (`vad.txt`, `pte.txt`), `modules/<dll>/pefile.dll`
  (best-effort reconstructed module), `pedump`, `handles`, `threads`, `files`, `vmemd`
  (virtual memory regions as files), `minidump`.
- `/sys/`: `net/netstat.txt`, `proc/proc.txt` (tree), `proc/proc-v.txt` (with image path and
  command line), `services`, `users`.
- `/registry/`: registry information.
- `/forensic/` (forensic mode): `csv/` (process.csv, net.csv, findevil.csv, timeline_*.csv,
  timeline_all.csv), `timeline/` (timeline_all.txt and per-source timelines),
  `findevil/findevil.txt` (detections such as PE_INJECT, PE_NOLINK, PE_PATCHED), `ntfs/`
  (files and folders recovered from MFT records in memory), `yara/` (with
  `-forensic-yara-rules rules.yar`).

## Workflow
1. Read `forensic/findevil/findevil.txt` and `sys/proc/proc-v.txt`.
2. Open `forensic/csv/timeline_all.csv` in Timeline Explorer.
3. Pull suspect process modules/VADs from `pid/<pid>/` for malware analysis.
4. Confirm key findings with Volatility 3 (independent tool).

## Gotchas
- Forensic mode reads the whole dump in one pass and can take a while; wait for
  `forensic/progress_percent.txt` = 100. It is not recommended for live memory (smear).
- Licence: the source is AGPL v3. FindEvil's built-in Yara rules come from Elastic Security
  and stay disabled until you accept the Elastic License 2.0 with
  `-license-accept-elastic-license-2-0`.

## Verify
Process list and network connections agree with Volatility `windows.pslist`/`netscan`
output for the same image.

## Checked

- Confirmed: forensic mode values 1-4, forensic_enable.txt and progress_percent.txt, csv/timeline/findevil/ntfs/yara outputs, Dokany/FUSE mounting, -device and -pagefile options, Elastic licence flag.

Method: docs-checked 2026-11-09 against MemProcFS README.md and wiki pages FS_Root, FS_Process, FS_Process_MemMap, FS_Process_Modules, FS_Process_PEDump, FS_Process_Minidump, FS_Process_VMemD, FS_Forensic, FS_Forensic_CSV, FS_Forensic_Timeline, FS_Forensic_Ntfs, FS_Forensic_Yara, FS_FindEvil, FS_SysInfo*, VM, _CommandLine (cloned wiki repo). Removed hibernation-file and VMware .vmem support claims and per-process findevil/tasks entries (not confirmed); corrected licence note.
