---
id: computing-software.digital-forensics-incident-response.volatility.macos-memory-analysis-plugins
name: macos-memory-analysis-plugins
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [mac-memory-forensics, volatility3, macos, kdk, dwarf2json, mac-plugins, memory-forensics, dfir]
level: advanced
status: docs-checked
description: "Analyse a macOS memory image with Volatility 3 mac plugins: building symbols from the KDK, process, network, kext and hook checks, and their limits."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.mac.html", "https://github.com/volatilityfoundation/dwarf2json", "https://github.com/volatilityfoundation/volatility3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macOS memory plugins

**Goal:** run process, network, file and kernel-integrity checks on a macOS memory image.

## Symbols first
Volatility 3 needs a symbol table for the exact macOS kernel build:
1. Identify the kernel banner in the image with the `banners` plugin
   (`vol -f mem.raw banners.Banners`). The banner in the JSON must match the image exactly,
   down to the compilation date.
2. Obtain a kernel build with debug information for that exact kernel (a Kernel Debug Kit
   from Apple provides a `kernel.dSYM`).
3. `dwarf2json mac --macho <path>/kernel.dSYM/Contents/Resources/DWARF/kernel --macho-symbols <path>/kernel > mac-<build>.json`
4. Put the JSON (`.json`, `.json.gz` or `.json.xz`) under `volatility3/symbols/mac/`.

## Plugins
```bash
vol -f mem.raw mac.pslist ; vol -f mem.raw mac.pstree ; vol -f mem.raw mac.psaux
vol -f mem.raw mac.bash                 # bash history from bash process memory
vol -f mem.raw mac.lsof                 # open files per process
vol -f mem.raw mac.netstat ; vol -f mem.raw mac.ifconfig
vol -f mem.raw mac.mount ; vol -f mem.raw mac.list_files
vol -f mem.raw mac.lsmod                # loaded kernel modules
vol -f mem.raw mac.check_syscall ; vol -f mem.raw mac.check_sysctl ; vol -f mem.raw mac.check_trap_table
vol -f mem.raw mac.kauth_listeners ; vol -f mem.raw mac.kauth_scopes   # kauth callbacks (monitoring/hiding)
vol -f mem.raw mac.socket_filters ; vol -f mem.raw mac.trustedbsd      # kernel socket filters; trustedbsd modules
vol -f mem.raw mac.malfind ; vol -f mem.raw mac.proc_maps              # process memory ranges that may contain injected code
```

## Interpretation
- Unknown kexts, socket filters or kauth listeners not belonging to Apple or an installed
  security product are suspicious.
- Most current macOS malware lives in user space: focus on `pstree` parentage (launchd ->
  odd binary in `~/Library/` or `/tmp`), `psaux` arguments, `lsof`, `netstat`, `malfind`.

## Limits
- Acquisition is the hard part and is outside what the Volatility documentation covers;
  confirm you can obtain a usable image before relying on this approach, and keep disk
  artefacts and logs as a fallback.
- Plugin coverage trails Windows; a failing plugin often means a symbol/build mismatch
  (the banner in the JSON must match the image exactly).

## Self-check
Symbols match the exact build, and every user-space process with network activity or an
unusual path is explained.

## Checked

- Confirmed: all listed mac plugins exist; banners plugin identifies the kernel string, banner must match exactly; symbol files may be .json, .json.gz or .json.xz; dwarf2json mac --macho/--macho-symbols usage.

Method: docs-checked 2026-11-09 against volatility3 develop source plugins/mac/*.py, plugins/banners.py, doc/source/symbol-tables.rst and the dwarf2json README (Apple developer downloads page was unreadable and was dropped). Removed the KDK install path, sw_vers, System Extensions and SIP/Apple silicon acquisition claims as unconfirmed.
