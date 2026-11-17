---
id: computing-software.digital-forensics-incident-response.volatility.memory-image-triage-with-volatility3
name: memory-image-triage-with-volatility3
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [volatility, volatility3, vol, memory-forensics, ram-analysis, dfir, incident-response, windows-memory, linux-memory, pslist, psscan, pstree, malfind, netscan, cmdline, dlllist, handles, svcscan, symbol-tables, isf, process-hollowing, code-injection, winpmem, lime, memory-dump, windows-info]
level: practitioner
status: docs-checked
description: "Triage a Windows RAM image with Volatility 3: symbols, process listing vs scanning, cmdlines, network state, malfind for injected code, and dumping suspects."
sources: ["https://volatility3.readthedocs.io/", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Memory image triage with Volatility 3

**Goal:** in the first hour with a RAM capture, find the suspicious process(es), how
they were launched, what they talk to and whether code was injected — and produce
hashes and dumped artefacts you can hand on.

## Setup
```bash
python3 -m venv vol && . vol/bin/activate
pip install volatility3            # or clone the repo for the newest plugins
vol -h                             # entry point is `vol` (or `python3 vol.py` from a clone)
sha256sum memory.raw > memory.raw.sha256   # hash BEFORE you touch it, work on a copy
```
- Volatility 3 has **no profiles** (that was Volatility 2). It identifies the Windows
  kernel and downloads the matching symbol table (PDB → ISF JSON) from Microsoft's
  symbol server on first use. On an offline analysis box, pre-download the Windows
  symbol pack from the Volatility Foundation and drop it in `volatility3/symbols/`.
- Linux and macOS images need an ISF built for the **exact kernel** (`dwarf2json`
  against the kernel's debug symbols). No ISF = no results; this is the most common
  "Volatility doesn't work" cause on Linux.
- Run `vol -f memory.raw windows.info` first. If it fails, everything else will: check
  the image format (raw, crash dump, VMware `.vmem` with its `.vmss`/`.vmsn` alongside).

## Triage order
```bash
V="vol -q -f memory.raw -r csv"     # -r csv / -r json for greppable output; save every run
$V windows.info        > info.csv
$V windows.pslist      > pslist.csv   # walks the active process list (EPROCESS links)
$V windows.psscan      > psscan.csv   # pool-tag scan: finds unlinked/terminated processes too
$V windows.pstree      > pstree.csv
$V windows.cmdline     > cmdline.csv
$V windows.netscan     > netscan.csv  # TCP/UDP endpoints + owning PID (netstat on newer builds)
$V windows.malware.malfind     > malfind.csv
$V windows.svcscan     > svcscan.csv
```
1. **pslist vs psscan diff.** A PID in psscan but not pslist is either exited (has an
   exit time) or **unlinked by a rootkit** (no exit time) — the second is a big finding.
2. **Parent/child sanity (pstree).** Known-good shape: `wininit.exe` → `services.exe`
   → `svchost.exe`; `winlogon.exe` → `userinit.exe` → `explorer.exe`. Red flags:
   `svchost.exe` not parented by `services.exe`, more than one `lsass.exe`, Office or a
   browser spawning `cmd.exe`/`powershell.exe`, `rundll32.exe` with no arguments,
   lookalike names (`scvhost.exe`, `lsass.exe` running from outside `System32`).
3. **cmdline.** Look for `-enc`/`-EncodedCommand`, `IEX`, `DownloadString`, paths in
   `%TEMP%`, `AppData`, `ProgramData`, `\Users\Public`.
4. **netscan.** Map foreign IPs to PIDs; note `ESTABLISHED` sessions from processes
   that shouldn't talk to the internet. Pivot the IPs into your log analysis.
5. **malfind.** Flags process VAD regions that are both executable and writable
   (e.g. `PAGE_EXECUTE_READWRITE`), plus executable-only regions with dirty pages; it
   skips empty regions and file-mapped `PAGE_EXECUTE_WRITECOPY`. An `MZ` header or a clear
   shellcode prologue in the hexdump is strong; many hits in JIT-heavy processes
   (browsers, .NET, Java) are **false positives** — judge by process and content.

## Dig into a suspect PID
```bash
$V windows.dlllist --pid 4242
$V windows.handles --pid 4242          # mutexes, files, registry keys it holds
vol -f memory.raw -o out/ windows.pslist --pid 4242 --dump     # process executable
vol -f memory.raw -o out/ windows.malware.malfind --pid 4242 --dump    # injected regions
sha256sum out/*
```
Also useful: `windows.filescan` + `windows.dumpfiles` (recover cached files),
`windows.registry.hivelist` / `printkey` (registry keys), `windows.vadinfo`, and
`timeliner` (its `--create-bodyfile` option) to fold memory timestamps into your
super-timeline (see
computing-software.digital-forensics-incident-response.disk-memory-forensics.super-timeline-with-plaso).
Plugin names do change between releases — check `vol -h` on your installed version.

## Gotchas
- Dumped executables are **not** byte-identical to the file on disk (relocated,
  sections in memory layout), so their hash won't match threat-intel hashes. Use
  imphash, YARA (`windows.vadyarascan` / `yarascan`) or strings instead.
- Smear: memory acquired from a live system changes during capture; occasional
  broken structures are normal, not proof of tampering.
- Never run dumped samples on your analysis host; move them to the malware lab
  (computing-software.digital-forensics-incident-response.malware-analysis.static-and-dynamic-triage).

## Verify
- [ ] Image hash recorded before analysis; analysis done on a copy.
- [ ] `windows.info` resolves symbols cleanly.
- [ ] pslist/psscan diff explained for every extra PID.
- [ ] Each suspect PID has: parent chain, cmdline, network endpoints, malfind verdict.
- [ ] Dumped artefacts hashed and noted in the case log with the command that produced them.

## Checked

- Confirmed: pip package and vol entry point, symbol packs and Microsoft PDB download, Linux/macOS need dwarf2json symbols, -q/-r/-o options, plugin flags --pid and --dump.

Method: docs-checked 2026-11-09 against volatility3 repo README.md, pyproject.toml, doc/source/symbol-tables.rst, cli/__init__.py, cli/text_renderer.py, layers/vmware.py and plugins windows/malware/malfind.py, pslist, psscan, memmap, dlllist, vadinfo, dumpfiles, timeliner (develop branch source). Corrected the malfind description and dropped the unsupported hibernation-file image claim; pstree parent/child heuristics are general practice, not from the cited docs.
