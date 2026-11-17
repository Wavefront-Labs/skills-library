---
id: computing-software.digital-forensics-incident-response.volatility.yara-scanning-memory
name: yara-scanning-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [yarascan, vadyarascan, yara, memory-forensics, volatility3, dfir]
level: practitioner
status: docs-checked
description: "Scan memory images with YARA in Volatility 3: windows.vadyarascan and yarascan, rule files vs strings, PID targeting, interpreting hits and dumping the matching regions."
sources: ["https://volatility3.readthedocs.io/en/latest/", "https://github.com/volatilityfoundation/volatility3/blob/develop/volatility3/framework/plugins/yarascan.py", "https://github.com/volatilityfoundation/volatility3/blob/develop/volatility3/framework/plugins/windows/vadyarascan.py", "https://github.com/volatilityfoundation/volatility3/blob/develop/volatility3/framework/plugins/linux/vmayarascan.py", "https://yara.readthedocs.io/en/stable/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# YARA scanning memory

**Goal:** find malware, tools or indicators in process and kernel memory, including fileless
and unpacked payloads that disk scans miss.

## Plugins (Volatility 3)
```bash
# process memory (VADs) of all or selected processes
vol -f mem.raw windows.vadyarascan --yara-file rules.yar
vol -f mem.raw windows.vadyarascan --yara-file rules.yar --pid 4242 5124
vol -f mem.raw windows.vadyarascan --yara-string "evil-c2.example"
# kernel memory
vol -f mem.raw yarascan.YaraScan --yara-file rules.yar
# Linux
vol -f mem.lime linux.vmayarascan --yara-file rules.yar     # VMAs of Linux processes (--pid to select)
```
Requires `yara-x` or `yara-python` in the Volatility environment (the plugin uses yara-x when it can be
imported and falls back to yara-python; without either it is unavailable). Rules can be given with
`--yara-file`, `--yara-string` or `--yara-compiled-file`; `--insensitive` and `--wide` adjust string matching.

## Interpreting hits
- A hit in a process's private, executable VAD (check with `windows.vadinfo --pid` at the
  offset) is stronger than in mapped data or heap.
- Hits in AV/EDR processes are often their signature databases: false positives.
- Strings rules (domains, mutexes) can match benign references (browser history in memory).

## Follow-up
```bash
vol -f mem.raw windows.vadinfo --pid 4242 --address 0x1f0000 --dump     # dump the VAD containing the hit
vol -f mem.raw windows.malware.malfind --pid 4242
```
Then analyse the dump (strings, PE reconstruction, YARA again, capa).

## Rules for memory
Write rules on **unpacked** payload strings/code; skip `uint16(0)==0x5A4D` anchors since
memory regions may have wiped headers; keep rules efficient (scans cover gigabytes).

## Verify
Each reported hit lists PID, process, VAD range and protection, and the dumped region's
hash; at least one hit is confirmed by an independent method (malfind, strings, disassembly).

## Checked

Checked 2026-10-25 against the Volatility 3 source (volatilityfoundation/volatility3 develop branch, last pushed 2026-10-12). Confirmed: `yarascan.YaraScan` (kernel memory) with `yara_string`, `yara_file`, `yara_compiled_file`, `insensitive`, `wide`, `max_size` options; `windows.vadyarascan` with a `--pid` list; `linux.vmayarascan` with `--pid`; `windows.vadinfo` with `--pid`, `--address` and `--dump`; `windows.malware.malfind`; yara-x or yara-python as the backend (pyproject lists both). Corrected: the Linux plugin name is stable (`linux.vmayarascan`) and the yarascan layer is kernel memory. Removed the unverified output column list.

Method: documentation only; no commands were run.
