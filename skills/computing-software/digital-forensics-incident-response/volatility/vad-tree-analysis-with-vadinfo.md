---
id: computing-software.digital-forensics-incident-response.volatility.vad-tree-analysis-with-vadinfo
name: vad-tree-analysis-with-vadinfo
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [vadinfo, vadwalk, vad-tree, volatility3, memory-protection, injected-code, memory-forensics, dfir]
level: advanced
status: draft
description: "Walk a process VAD tree with Volatility vadinfo and vadwalk to find private executable regions, mapped files and injected code by protection and tag."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.html", "https://www.memoryanalysis.net/amf"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VAD tree analysis (vadinfo, vadwalk)

**Goal:** understand every allocated region in a suspect process: what backs it (file or
private), its initial protection, and whether it looks like injected code.

## Commands
```bash
vol -f mem.raw windows.vadinfo --pid 3520                    # every VAD node: start/end, tag, protection, file
vol -f mem.raw windows.vadinfo --pid 3520 --address 0x1f0000 # one region
vol -f mem.raw windows.vadinfo --pid 3520 --address 0x1f0000 --dump -o out/
vol -f mem.raw windows.vadwalk --pid 3520                     # tree structure (left/right/parent)
vol -f mem.raw windows.malware.malfind --pid 3520                     # pre-filtered: private + executable + content preview
vol -f mem.raw windows.vadyarascan --pid 3520 --yara-file rules.yar
```

## Fields that matter
- **Tag:** `VadS` (short VAD, private allocations: VirtualAlloc), `Vad`/`Vadl`
  (mapped files/images). Private + executable = where shellcode lives.
- **Protection:** the *initial* protection at allocation time (`PAGE_EXECUTE_READWRITE`
  is the classic injection tell). Later VirtualProtect changes are recorded in page tables,
  not the VAD; a region allocated RW then flipped to RX shows RW here. Check page-level
  protections with `windows.memmap` or MemProcFS when the VAD looks benign.
- **CommitCharge / PrivateMemory:** private, committed, executable regions that are not
  images are the shortlist.
- **File:** mapped path for image/file-backed regions; an image region whose file is a
  legitimate DLL but whose bytes differ from disk indicates module stomping.

## Triage routine
1. `vadinfo` the process; filter `VadS` with any EXECUTE protection.
2. Read the first bytes (malfind preview): `MZ` = PE dropped in memory; `fc 48 83 e4 f0`
   (x64 Cobalt Strike-style stub) or other prologues = shellcode; zeros = possibly wiped header
   (search deeper for a PE `PE\0\0` signature).
3. Dump, then scan with YARA, `strings -el`, and load into a disassembler at the region base.
4. Compare with a clean instance of the same binary to dismiss JIT engines (.NET CLR,
   browsers, JavaScript engines) that legitimately create private RWX regions.

## Gotchas
- JIT-heavy processes (browsers, PowerShell/.NET, Java) are noisy; triage by unusual parent,
  network connection (`windows.netscan`) or YARA hits rather than RWX alone.
- Large dumps: dump specific addresses, not the whole process.

## Self-check
For each executable private region, you have a dump, a classification (PE, shellcode, JIT)
and a reason.
