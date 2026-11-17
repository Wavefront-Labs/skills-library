---
id: computing-software.digital-forensics-incident-response.volatility.dumping-linux-process-elfs-and-maps
name: dumping-linux-process-elfs-and-maps
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [linux-elfs, linux-proc-maps, volatility3, linux-memory-forensics, process-dumping, dfir]
level: practitioner
status: docs-checked
description: "Dump Linux process executables and memory mappings with Volatility 3 linux.elfs and linux.proc.Maps: listing mapped ELFs, extracting VMAs and analysing dumps."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.elfs.html", "https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.proc.html", "https://man7.org/linux/man-pages/man5/elf.5.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Dumping Linux process ELFs and maps

When attackers delete their binary after launching it, or run it from `memfd`, the memory image may hold the
only copy. `linux.elfs` lists all memory-mapped ELF files for all processes and can extract an ELF
(`elf_dump`); `linux.proc.Maps` lists all memory maps for all processes and can extract a VMA's data
(`vma_dump`).

## Plugins
```bash
vol -f mem.lime linux.elfs
vol -f mem.lime linux.proc.Maps
```
The plugin reference pages do not list command-line options. Use `vol linux.elfs -h` and
`vol linux.proc.Maps -h` for your version to find the PID filter and dump options; they have changed
across releases. A VMA dump is limited to a maximum size, defaulting to 1073741824 bytes (1 GiB).

## Working with dumps
1. Hash each dump and record it.
2. A dump is reconstructed from memory, so it may not match the on-disk original byte for byte; compare
   structure rather than relying on an exact hash. The ELF format (`elf(5)`) defines the header and section
   layout to compare against.
3. Analyse with standard tools (`readelf`, `strings`, YARA, a disassembler).

## Gotchas
- Dumping every process produces very large output; target PIDs from triage.
- Shared libraries appear in many processes; dump them once.

## Verify
For each recovered binary: PID, mapping range, dump hash and a static-analysis summary are in the case
notes, and on-disk absence is confirmed from the disk image or live response.

## Checked
2026-11-08. Read the linux.elfs and linux.proc plugin reference pages in full (descriptions, elf_dump,
vma_dump, default maximum size) and consulted the elf(5) man page for format structure. Removed
unconfirmed claims: PID and dump option names, map column list, interpretation rules for `(deleted)`,
`/memfd:` and library paths, zero-fill and relocation statements, package-hash comparison advice, Go/Rust/UPX
markers, and container path notes.
Method: documentation only; no commands were run.
