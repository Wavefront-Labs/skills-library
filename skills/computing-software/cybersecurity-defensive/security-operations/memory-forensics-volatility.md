---
id: computing-software.cybersecurity-defensive.security-operations.memory-forensics-volatility
name: memory-forensics-volatility
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, volatility, volatility3, memory-forensics, memory-acquisition, winpmem, avml, process-injection, malfind, credential-theft]
level: advanced
status: docs-checked
description: "Acquire RAM and analyse it with Volatility 3: process trees, network connections, injected code and persistence that never touches disk."
sources: ["https://github.com/volatilityfoundation/volatility3", "https://volatility3.readthedocs.io/en/latest/getting-started-windows-tutorial.html", "https://volatility3.readthedocs.io/en/latest/getting-started-linux-tutorial.html", "https://volatility3.readthedocs.io/en/latest/symbol-tables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory forensics with Volatility 3

**Goal:** find what was running in memory (fileless malware, injected code, live C2
connections, credentials in use) that disk evidence cannot show.

## Acquire first (order of volatility)
- Windows: WinPmem (Velocidex), or the EDR's own memory collection.
- Linux: AVML (Microsoft, github.com/microsoft/avml).
- VMs: suspend and take the memory file, or a hypervisor snapshot with memory.
Hash the image, copy it off the host, note the exact OS build.

## Core Volatility 3 workflow (Windows)
```
vol -f host01.raw windows.info
vol -f host01.raw windows.pstree
vol -f host01.raw windows.cmdline
vol -f host01.raw windows.netscan
vol -f host01.raw windows.malware.malfind --dump
vol -f host01.raw windows.dlllist --pid 4321
vol -f host01.raw windows.svcscan
vol -f host01.raw windows.handles --pid 4321
```
Plugin names move between releases. In the current source tree the malware-hunting plugins live under
`windows.malware.*` (`malfind`, `ldrmodules`, `psxview`, `hollowprocesses`, `processghosting`, `svcdiff`,
`suspicious_threads`) and `windows.registry.*` (`hivelist`, `printkey`, `hashdump`, `userassist`). The old top-level
names such as `windows.malfind` are deprecated wrappers that are scheduled for removal, so use the new names and
run `vol -h` to list what your installed version offers.

What to look for:
- **pstree:** Office or browser spawning shells; `lsass.exe` with an unexpected parent;
  processes with no parent; names imitating system binaries (`svch0st.exe`), wrong paths in `cmdline`.
- **netscan:** established connections from processes that should not talk out; map to the process tree.
- **malfind:** private executable memory regions containing an MZ header or shellcode. Many JIT engines
  (browsers, .NET) produce false positives: validate with the dump and a YARA scan
  (`windows.vadyarascan --yara-file rules.yar`, or `--yara-string`).
- **svcscan:** services pointing to temp or user-writable paths.

Linux equivalents: `linux.pslist`, `linux.pstree`, `linux.bash`, `linux.sockstat`, and `linux.malware.malfind`
(plus `linux.malware.check_syscall`, `check_modules`, `hidden_modules`, `netfilter`). The old `linux.malfind` is a
deprecated wrapper.
Linux (and macOS) analysis needs a symbol table (ISF) for the exact kernel, built from a debug kernel with
`dwarf2json` (github.com/volatilityfoundation/dwarf2json) and placed in the symbols directory.

## Gotchas
- For Windows the ISF is generated automatically from PDB files downloaded from Microsoft servers, so offline
  analysis needs symbols staged beforehand.
- Smearing: acquisition on a busy host takes time and structures can be inconsistent;
  odd results may be acquisition artefacts.
- Credential material in memory dumps is sensitive: store and transfer the image as you would the credentials.

## Verify
- [ ] `windows.info` reports the expected build and time of capture.
- [ ] Each suspicious finding is corroborated by a second plugin or by disk/EDR evidence before reporting.

## Checked
2026-11-01. Confirmed in a shallow clone of volatilityfoundation/volatility3 (plugin tree, deprecation wrappers,
`vadyarascan`/`yarascan` options, `--dump` and `--pid` options) and its docs (WinPmem and AVML links, ISF and
dwarf2json text). Removed: executable names, Magnet RAM Capture, the unsupported kernel-module claim, and book and
NIST citations that were not re-read.
Method: documentation only; no commands were run.
