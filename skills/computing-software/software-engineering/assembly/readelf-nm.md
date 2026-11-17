---
id: computing-software.software-engineering.assembly.readelf-nm
name: readelf-nm
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, readelf-nm, asm-binutils]
level: intro
status: docs-checked
description: "Inspect ELF files with GNU readelf, nm, size, strings and addr2line: headers, sections, symbols, dynamic section and address-to-line mapping."
sources:
  - https://sourceware.org/binutils/docs/binutils/readelf.html
  - https://sourceware.org/binutils/docs/binutils/nm.html
  - https://sourceware.org/binutils/docs/binutils/size.html
  - https://sourceware.org/binutils/docs/binutils/strings.html
  - https://sourceware.org/binutils/docs/binutils/addr2line.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# readelf, nm and friends
**Goal:** answer structural questions about a binary quickly.

```sh
readelf -h prog              # ELF file header
readelf -S -W prog           # section headers (wide output)
readelf -l prog              # program headers (segments)
readelf -s prog              # symbol tables
readelf -r foo.o             # relocations
readelf -d prog              # dynamic section
readelf -n prog              # notes
readelf -A prog              # architecture-specific information
nm -C -S --size-sort prog    # demangled symbols with sizes, sorted by size
nm -u foo.o                  # undefined symbols
nm -D libfoo.so              # dynamic symbols
size prog                    # text, data, bss, dec, hex totals
strings -a prog              # printable strings from the whole file
addr2line -f -C -e prog 0x401136   # address to function name and file:line
```
- `readelf -a` is equivalent to the long list of header, section, symbol, relocation, dynamic, notes and other options together.
- `nm` types: uppercase usually means global, lowercase local. `T/t` text (code), `D/d` initialised data, `B/b` BSS, `R/r` read-only data, `U` undefined, `W/w` weak, `V/v` weak object, `A` absolute.
- `size` prints Berkeley format by default (`-A` selects System V). Berkeley counts read-only data in the `text` column.
- `strings` by default shows printable sequences of at least 4 characters; for object files it scans only the data sections unless you pass `-a`.
- `addr2line` also reads addresses from standard input, so it can be used in a pipe. Line information needs a binary built with debug info.

## Self-check
Run `readelf -S -W` and `readelf -l` on a small binary and note which segment contains `.rodata`.

## Checked
Read the GNU binutils manual pages for readelf, nm, size, strings and addr2line. Removed: ldd, file and objdump -x advice, the ldd safety gotcha, the GNU property IBT/SHSTK/BTI and build-id claims for `readelf -n`, the NEEDED/RPATH/FLAGS list for `-d`, the stripped-binary `nm` message, and the refspecs.linuxfoundation.org source (not read).

Method: docs-checked 2026-11-09 against the GNU binutils manual pages for readelf, nm, size, strings and addr2line.
