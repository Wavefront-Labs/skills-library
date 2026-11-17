---
id: computing-software.digital-forensics-incident-response.volatility.detecting-unbacked-memory-and-module-stomping
name: detecting-unbacked-memory-and-module-stomping
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [module-stomping, code-injection, process-injection, malfind, volatility3, dfir]
level: advanced
status: draft
description: "Detect unbacked executable memory, module stomping and phantom DLL hollowing in memory images by comparing VADs, PE headers and on-disk images."
sources: ["https://volatility3.readthedocs.io/en/latest/", "https://www.forrest-orr.net/post/masking-malicious-memory-artifacts-part-ii-insights-from-moneta", "https://github.com/hasherezade/pe-sieve"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Detecting unbacked memory and module stomping

**Goal:** modern loaders avoid the classic `malfind` signature (private RWX memory with an MZ header)
by writing code into legitimately loaded DLLs ("module stomping") or using image-backed memory
from transacted/deleted files ("phantom DLL hollowing").

## Categories
| Technique | Memory signature |
|---|---|
| Classic injection | Private (`VadS`), `PAGE_EXECUTE_READWRITE`, no file mapping -> malfind finds it |
| Unbacked executable | Executable private memory without MZ (shellcode, reflective loaders that wipe headers) |
| Module stomping | Image-backed VAD (DLL mapped from disk) whose in-memory `.text` differs from the file on disk |
| Phantom DLL hollowing | Image-backed VAD whose file was a TxF transaction or deleted file: VAD file object name missing or pointing to nothing on disk |

## Volatility 3 workflow
```bash
vol -f mem.raw windows.malware.malfind --pid 4120                 # private executable regions
vol -f mem.raw windows.vadinfo --pid 4120 > vad.txt        # protections, file object per VAD
vol -f mem.raw windows.malware.ldrmodules --pid 4120               # mapped images vs PEB lists
vol -f mem.raw windows.dlllist --pid 4120 --dump           # dump loaded modules
vol -f mem.raw windows.vadyarascan --pid 4120 --yara-file shellcode.yar
```
- Compare dumped DLL `.text` sections with the same DLL version from disk/symbol server (hash of
  section, or byte diff): differences in a signed Microsoft DLL = stomping.
- VADs with `PAGE_EXECUTE_*` and file object names absent or in unusual paths -> phantom hollowing candidate.
- Executable pages in VADs of type `Mapped` (not `Image`) are also suspicious.

## Live complement
PE-sieve / HollowsHunter on a live host detect patched modules and implants with `/imp` reconstruction; Moneta lists unbacked and modified image memory.

## Gotchas
- JIT engines (.NET, JavaScript in browsers) legitimately create private executable memory; baseline by process type.
- Hotpatching and security products modify module code; verify the vendor before calling it malicious.
- Paged-out pages make byte comparisons incomplete; note coverage.

## Verify
Each flagged region is dumped, disassembled or YARA-matched, and attributed to a loader/family or a benign cause.
