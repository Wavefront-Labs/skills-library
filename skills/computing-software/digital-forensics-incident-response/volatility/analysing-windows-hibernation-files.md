---
id: computing-software.digital-forensics-incident-response.volatility.analysing-windows-hibernation-files
name: analysing-windows-hibernation-files
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [hibernation-file-analysis, hiberfil, volatility3, hibr2bin, fast-startup, compressed-memory, memory-forensics, dfir]
level: advanced
status: draft
description: "Decompress and analyse hiberfil.sys as a historical memory image: format by Windows version, Fast Startup caveats, Hibr2Bin and Volatility 3 layers."
sources: ["https://github.com/volatilityfoundation/volatility3", "https://github.com/comaeio/Hibr2Bin", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/setup-upgrade-and-drivers/disable-and-re-enable-hibernation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analysing hibernation files

**Goal:** turn `hiberfil.sys` from a disk image into a usable memory image of the machine at
the time it last hibernated (or shut down with Fast Startup).

## What it contains
- Full hibernate: compressed RAM contents at hibernate time (user and kernel).
- **Fast Startup** (Windows 8+ default on many client builds): only the kernel session after
  user logoff, so expect drivers, services and kernel objects but few user processes.
- Compression: Xpress (LZ77) or Xpress Huffman on Windows 8+; the format changed
  substantially from Windows 7 to 8, so tooling must match the version.

## Is it worth parsing?
Read the first 4 bytes: `HIBR`/`hibr` = valid hibernation data; `wake`, `RSTR` or a zeroed
header on Windows 8+ usually means the system resumed and the header was invalidated, though
compressed pages may still be recoverable by carving. Note the file's $SI times to date the
snapshot.

## Conversion and analysis
```bash
# Windows 8/10/11: Hibr2Bin (Comae) -> raw image
Hibr2Bin.exe /PLATFORM X64 /MAJOR 10 /MINOR 0 /INPUT hiberfil.sys /OUTPUT hiber.raw
vol -f hiber.raw windows.info ; vol -f hiber.raw windows.pslist

# Volatility 3 (2.28.2) has no hibernation layer or windows.hibernation.* plugins: convert first with Hibr2Bin or MemProcFS

# Windows XP-7: Volatility 2
vol.py -f hiberfil.sys --profile=Win7SP1x64 imagecopy -O hiber.raw
```
Then treat the raw image like any memory capture: pslist/psscan, netscan, malfind, hashdump,
filescan, yarascan. Also run `strings`/`bulk_extractor` directly on the decompressed image.

## Investigative value
- Evidence of processes, network connections and injected code from days or weeks before
  the incident response capture, including malware since removed.
- Encryption keys (BitLocker FVEK) may be recoverable from hibernation data.

## Gotchas
- Collect `hiberfil.sys` with a raw-copy tool (KAPE, FTK Imager, `RawCopy`); it is locked on
  a live system.
- Only one snapshot exists; it is overwritten at the next hibernate.
- Always record the Windows build: the wrong version parameters produce garbage.

## Self-check
You dated the snapshot, confirmed the header state and know whether it is a full hibernate or
a Fast Startup kernel-only image before drawing conclusions about user activity.
