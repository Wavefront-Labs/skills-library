---
id: computing-software.digital-forensics-incident-response.volatility.recovering-files-from-memory-with-filescan-and-dumpfiles
name: recovering-files-from-memory-with-filescan-and-dumpfiles
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [filescan, dumpfiles, memory-artefacts, volatility3, file-objects, dfir]
level: practitioner
status: docs-checked
description: "Recover files cached in RAM with Volatility 3 windows.filescan and windows.dumpfiles: finding FILE_OBJECTs, dumping by virtual or physical address, and interpreting output."
sources: ["https://volatility3.readthedocs.io/en/latest/", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovering files from memory with filescan and dumpfiles

**Goal:** extract executables, documents, scripts, registry hives and logs that were cached in
memory, including malware deleted from disk.

## Find file objects
```bash
vol -q -f mem.raw -r csv windows.filescan > filescan.csv
grep -i -E '\\(temp|appdata|programdata|users\\public)\\.*\.(exe|dll|ps1|bat|js|vbs)' filescan.csv
```
Columns: `Offset` and `Name` (the offset locates the `_FILE_OBJECT`; pass it to `--physaddr`).

## Dump
```bash
mkdir out
vol -f mem.raw -o out windows.dumpfiles --physaddr 0x1e4f2a3b0     # one file object (from filescan)
vol -f mem.raw -o out windows.dumpfiles --virtaddr 0xfa8001234560
vol -f mem.raw -o out windows.dumpfiles --pid 4242                 # all files mapped by a process
vol -f mem.raw -o out windows.dumpfiles --filter "Temp" --ignore-case   # regular expression on file name; cannot be combined with --virtaddr/--physaddr
```
Output file extensions: `.dat` (DataSectionObject = cached data view), `.img`
(ImageSectionObject = mapped executable image) and `.vacb` (SharedCacheMap).

## Interpretation
- **ImageSectionObject** of an EXE/DLL is the in-memory mapped image: sections aligned to
  pages; hashes will not normally match the on-disk file. Compare by imphash, strings or
  fuzzy hashing.
- **DataSectionObject** files are often partial: only cached pages present, others zero.
- Good targets: registry hives (`windows.registry.hivelist` is better), event logs
  (`.evtx`), browser databases, PowerShell scripts in Temp.

## Gotchas
- Plugin options differ by Volatility 3 release; check `vol windows.dumpfiles -h`.
- Large dumps can include thousands of files; filter first.

## Verify
Open the dumped file with the appropriate parser (PE parser, EVTX tool); note partial content,
and record the source address and section type for each recovered file.

## Checked

- Confirmed: --pid, --virtaddr, --physaddr, --filter options; dat/img/vacb outputs map to DataSectionObject, ImageSectionObject, SharedCacheMap.

Method: docs-checked 2026-11-09 against volatility3 develop source plugins/windows/dumpfiles.py and filescan.py. Corrected filescan columns (Offset, Name), the --filter semantics (regular expression, with --ignore-case, not combinable with address options) and removed the MFTECmd and imports-resolved claims.
