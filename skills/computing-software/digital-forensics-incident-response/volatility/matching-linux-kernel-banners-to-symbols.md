---
id: computing-software.digital-forensics-incident-response.volatility.matching-linux-kernel-banners-to-symbols
name: matching-linux-kernel-banners-to-symbols
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [linux-banners, dwarf2json, symbol-tables, linux-memory-forensics, volatility3, dfir]
level: advanced
status: docs-checked
description: "Identify the exact kernel in a Linux memory image with banners.Banners, then find or build the matching ISF symbol file from a debug kernel with dwarf2json."
sources: ["https://volatility3.readthedocs.io/en/latest/symbol-tables.html", "https://github.com/volatilityfoundation/dwarf2json", "https://github.com/Abyss-W4tcher/volatility3-symbols"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching Linux kernel banners to symbols

**Goal:** Volatility 3 needs an ISF symbol table that exactly matches the kernel build. The banner
string in memory identifies it.

## Identify the kernel
```bash
vol -f mem.lime banners.Banners
```
The banner must match the ISF file's banner exactly, down to the compilation date. The
`isfinfo` plugin lists the ISF files Volatility knows about and the banner each searches for
(it can be slow with many files). Record the banner during acquisition on the live host too.

## Get symbols
1. **Prebuilt ISF**: the community repository Abyss-W4tcher/volatility3-symbols indexes ISF
   files by banner (a `banners_plain.json` mapping) and publishes `.json.xz` files as release
   assets. Place the file under `volatility3/symbols/linux/` (create the folder if missing).
2. **Build** from a kernel with debug symbols. Standard distribution kernels are stripped;
   the debug kernel is in a separate package that you must acquire matching the banner.
   ```bash
   dwarf2json linux --elf /path/to/vmlinux --system-map /path/to/System.map > kernel.json
   xz kernel.json
   ```
   `--elf` extracts symbols and types; `--system-map` adds symbol offsets and has the highest
   precedence if sources conflict. `--elf-symbols` and `--elf-types` extract only one kind.
3. Copy the JSON into `[symbols directory]/linux`. Volatility caches the banner to file
   mapping, so file names do not matter.
4. Custom or self-compiled kernels: you need the target's own debug kernel; collect it during
   incident response or rebuild with identical config.

## Verify the match
Run a Linux plugin (for example `linux.pslist`) and check the process list is sensible
(systemd as PID 1, kthreadd as PID 2). A symbol or requirement error indicates a mismatch.

## Gotchas
- Same version string with different build numbers are different kernels.
- Pre-stage symbols for your fleet's kernels as part of IR readiness.

## Checked
2026-11-01. Confirmed in the Volatility 3 symbol-tables page (exact banner match, dwarf2json
generation, debug kernel in a separate package, `isfinfo`, copy to `symbols/linux`), the
dwarf2json README (`--elf`, `--elf-symbols`, `--elf-types`, `--system-map` and precedence) and the
Abyss-W4tcher README (banner index, `.json.xz` releases, `symbols/linux/`). Removed: distro
debug package names and paths, example banner and build numbers, cloud kernel suffixes, and the
`-s ./symbols` form and error text, which the fetched docs do not confirm.
Method: documentation only; no commands were run.
