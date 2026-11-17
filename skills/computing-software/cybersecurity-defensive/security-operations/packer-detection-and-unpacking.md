---
id: computing-software.cybersecurity-defensive.security-operations.packer-detection-and-unpacking
name: packer-detection-and-unpacking
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [malware-analysis, packer-detection, upx, entropy, unpacking, detect-it-easy, memory-dump, pe-sieve]
level: advanced
status: draft
description: "Recognise packed malware (entropy, imports, section names, DIE signatures) and get to the payload: UPX -d, memory dumps with PE-sieve, and debugger-based unpacking basics."
sources: ["https://github.com/horsicq/Detect-It-Easy", "https://github.com/hasherezade/pe-sieve", "https://upx.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Packer detection and basic unpacking

Packed or crypted samples hide strings, imports and code; static triage of the packed file tells
you little beyond "it is packed".

## Recognise packing
- **Detect It Easy (DIE)**: signatures for UPX, MPRESS, Themida, VMProtect, ASPack, .NET obfuscators
  (ConfuserEx, SmartAssembly) and installers (NSIS, Inno). `diec sample.exe`.
- **Entropy**: section entropy > ~7.2 suggests compression/encryption (DIE and pestudio show it).
- **Imports**: very few imports, mostly `LoadLibraryA`, `GetProcAddress`, `VirtualAlloc`,
  `VirtualProtect`: the unpacker resolves the real ones at runtime.
- **Sections**: names like `UPX0/UPX1`, `.MPRESS1`, random names; raw size 0 with large virtual size.
- **Strings**: almost none, or only the stub's.

## UPX
```
upx -d sample.exe -o unpacked.exe
```
Malware often modifies UPX headers so `-d` fails ("not packed by UPX"); restoring `UPX!` magic and
section names sometimes fixes it, otherwise unpack dynamically.

## Dynamic: let it unpack itself, then dump
In the isolated lab:
1. Run the sample (or under a debugger with a breakpoint on `VirtualProtect`/`VirtualAlloc`,
   `WriteProcessMemory`, `ResumeThread`, `CreateProcessInternalW` for process hollowing).
2. Dump the payload from memory:
   - `pe-sieve.exe /pid <pid> /imp 3` scans the process for implanted/hollowed PEs and dumps them with
     reconstructed imports; `hollows_hunter` does all processes.
   - Process Hacker/System Informer: memory regions with RWX protection and an `MZ` header.
3. Fix the dump if needed (unmap with PE-bear, rebuild imports with Scylla) and analyse statically.
Many crypters inject into a child process (e.g. spawned `RegAsm.exe`, `InstallUtil.exe`); dump that child.

## .NET
Obfuscated .NET: `de4dot sample.exe` handles many obfuscators; then decompile with dnSpyEx/ILSpy.
Payloads loaded with `Assembly.Load(byte[])` can be dumped with dnSpyEx breakpoints or ExtremeDumper.

## Gotchas
- Packed is not malicious by itself (commercial software uses protectors), but packed + unsigned +
  odd location is suspicious.
- Anti-debug and anti-VM checks stop unpacking; use ScyllaHide or a commercial sandbox memory dump.
- Hashes of the packed file change per build; YARA on the unpacked payload or memory is far more durable.

## Verify
The dumped payload shows meaningful imports and strings (C2 config, mutex names) and its capa
output lists real capabilities rather than only the loader's.
