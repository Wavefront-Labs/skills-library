---
id: computing-software.digital-forensics-incident-response.volatility.unlinked-dll-detection-with-ldrmodules
name: unlinked-dll-detection-with-ldrmodules
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [ldrmodules, volatility3, dll-injection, unlinked-dll, peb-ldr, reflective-loading, memory-forensics, dfir]
level: practitioner
status: docs-checked
description: "Use Volatility ldrmodules to find DLLs hidden from the PEB loader lists or loaded without a backing file, and separate true injection from benign false positives."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.html", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Unlinked DLL detection with ldrmodules

**Goal:** find modules that exist as mapped images in a process (VAD) but have been removed
from one or more of the three PEB loader lists, which is how DLL-hiding malware evades
`dlllist`-style tools.

## How it works
The PEB keeps three doubly-linked lists: **InLoadOrder**, **InInitializationOrder**,
**InMemoryOrder**. `ldrmodules` walks every VAD of the process whose start address holds an `MZ` header
(file-backed or not) and checks whether that base address appears in each list. Unlinking from all three hides a DLL from
Toolhelp32/`dlllist`; it cannot remove the VAD without unmapping the memory.

```bash
vol -f mem.raw windows.malware.ldrmodules --pid 2280
vol -r csv -f mem.raw windows.malware.ldrmodules > ldr.csv
# columns: Pid Process Base InLoad InInit InMem MappedPath
```

## Reading the output
| Pattern | Meaning |
|---|---|
| all True, path normal | normally loaded module |
| all False, path present | DLL unlinked from every list: strong hiding indicator |
| all False, **no MappedPath** | region starting with an `MZ` header but with no mapped file name: reflective / manual-mapped code, or module-stomping remnant |
| InInit False only, the process EXE | normal: the main executable is never in the init-order list |
| InInit False for `.mui`/`.fon`/data-mapped files | benign: mapped as data/resources, not initialised |
| path in `\Temp\`, `\AppData\`, `\ProgramData\`, `\Users\Public\` | suspicious even if linked |

## Workflow
1. Filter `ldr.csv` for rows where InLoad/InMem are False and the path is not the process
   image or a resource file.
2. For each hit, `windows.vadinfo --pid <pid> --address <base>` to read protection and file
   object; `windows.malware.malfind --pid <pid>` for RWX regions nearby.
3. Dump the region (`windows.dlllist --pid <pid> --dump` misses unlinked ones, so use
   `windows.vadinfo --pid <pid> --address <base> --dump`) and hash/YARA it.
4. Compare the mapped path with the on-disk file (hash mismatch suggests hollowing/stomping).

## Gotchas
- A manually mapped DLL whose first bytes are not an `MZ` header (erased or stomped headers)
  is skipped by ldrmodules; use `malfind` and `vadinfo` for those.
- WoW64 processes have 32- and 64-bit loader data; expect some benign oddities.

## Self-check
Every all-False row is either explained (resource/data mapping) or dumped, hashed and
attributed to a technique.

## Checked

- Confirmed: columns Pid Process Base InLoad InInit InMem MappedPath; three PEB list lookups keyed by DllBase.

Method: docs-checked 2026-11-09 against volatility3 develop source plugins/windows/malware/ldrmodules.py (the SANS poster source was unreadable and was dropped). Corrected the walk description: it considers VADs starting with an MZ header, not only file-backed ones, and removed the wrong private-VAD gotcha and the Volatility 2 -v line. The InInit/resource-file benign patterns and suspicious-path list are practitioner guidance.
