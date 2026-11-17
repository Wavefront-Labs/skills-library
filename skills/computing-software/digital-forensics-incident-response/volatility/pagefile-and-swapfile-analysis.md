---
id: computing-software.digital-forensics-incident-response.volatility.pagefile-and-swapfile-analysis
name: pagefile-and-swapfile-analysis
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [pagefile-analysis, memory-image-formats, pagefile, memory-forensics, dfir]
level: advanced
status: docs-checked
description: "Extract evidence from pagefile.sys and swapfile.sys: what pages contain, string and YARA searches, carving, and combining with memory images in MemProcFS."
sources: ["https://github.com/ufrisk/MemProcFS", "https://github.com/ufrisk/MemProcFS/wiki/_CommandLine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pagefile.sys and swapfile.sys analysis

**Goal:** pages swapped out of RAM land in the pagefile, sometimes from days earlier. They contain
fragments of process memory: commands, URLs, credentials, decrypted malware configs.

## Files
- `pagefile.sys` and `swapfile.sys`; on a default Windows 10 system MemProcFS gives
  `pagefile.sys` index 0 and `swapfile.sys` index 1 (a non-default configuration with more or
  fewer page files may differ). Collect them with a raw-copy tool, as they are locked on a
  live system.
- Page files must be taken at about the same time as the memory dump: stale page files
  from a different point in time severely degrade the analysis with bad data.

## Approaches
1. **Unstructured search** (works always):
```bash
strings -a -n 8 pagefile.sys > pf_ascii.txt ; strings -a -el -n 8 pagefile.sys > pf_unicode.txt
yara -s -r rules/ pagefile.sys
bulk_extractor -o be_pf pagefile.sys       # feature extraction (URLs, emails and similar)
```
2. **Structured with the memory image**: MemProcFS accepts page files for a Windows 10 memory
   dump with `-pagefileX` (X is the page file index) to improve analysis quality:
```cmd
MemProcFS.exe -device mem.raw -pagefile0 pagefile.sys -pagefile1 swapfile.sys -forensic 1
```
3. **Carving**: carve known file types from the pagefile with a file carver.

## Compressed memory
A process's virtual memory may map to physical memory, to page files or to compressed
memory (MemProcFS documents this for `memory.vmem`). Plain strings over a raw page file
will not see compressed content; use a tool aware of the compression store.

## Gotchas
- No timestamps: content cannot be dated from the pagefile alone; corroborate.
- Fragments may come from any process; attribution to a specific process needs structured reconstruction.

## Verify
Key hits are confirmed in context (surrounding bytes) and, where possible, attributed via MemProcFS process reconstruction.

## Checked

- Confirmed: -pagefileX option, default index 0 and 1 for pagefile.sys and swapfile.sys, stale page files degrade results, virtual memory may map to page files or compressed memory.

Method: docs-checked 2026-11-09 against MemProcFS wiki _CommandLine (-pagefileX section), FS_Process and README (cloned repos). The Microsoft page-file article was unreadable and was dropped along with the ClearPageFileAtShutdown, swapfile-purpose, MemCompression and Volatility pagefile-layer claims. The strings, yara and bulk_extractor commands are generic tool usage not verified against their docs here.
