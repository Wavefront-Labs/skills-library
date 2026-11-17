---
id: computing-software.firmware-embedded-development.hardware-debugging.gdb-multiple-symbol-files
name: gdb-multiple-symbol-files
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [add-symbol-file, symbol-file, bootloader-debugging, gdb, relocation, section-offsets, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Debug bootloader plus application (or relocated code) in one GDB session with add-symbol-file, section offsets and remove-symbol-file."
sources:
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Files.html
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Symbols.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loading multiple symbol files in GDB

**Use when:** stepping from a bootloader into the app, debugging code copied to RAM, or an image linked at one address
and run at another.

## Bootloader + application
`add-symbol-file filename [-readnow | -readnever] [-o offset] [textaddress] [-s section address ...]` reads extra
symbols for a file that was loaded into the running target by some other means. The new symbols are kept in addition
to the old, and the command can be used any number of times.
```gdb
file build/bootloader.elf
add-symbol-file build/app.elf <text-address>
break app_main
continue                               # bootloader jumps, breakpoint in the app hits
```
- `textaddress` is the address where the file's text section is loaded. Add `-s section address` pairs for other
  sections; omitted sections use the default addresses found in the file.
- `info files` lists the target and the files symbols were loaded from; `maint info sections` also shows flags and
  file offsets of each section.

## Relocated or PIC images
An image linked at one address and executed at another:
```gdb
add-symbol-file app_pic.elf -o <offset>                          # added to every section start
add-symbol-file app.elf <text-address> -s .data <data-address>   # per-section addresses
```
With `-o offset`, the offset is added to the start address of each section except those whose address you gave
explicitly. Any address can be an expression.

Relocatable `.o` files only work if their symbols refer only to symbols defined in that file, every section has
actually been loaded as it appears in the file, and you supply every section's load address. Linking a relocatable
file normally can differ from loading its symbols this way.

## Removing and switching
- `remove-symbol-file app.elf` or `remove-symbol-file -a <address>` (any address inside that file's range).
- `symbol-file` with no argument clears GDB's symbol table information, and forgets the contents of some breakpoints
  and auto-display expressions that referred to it.
- `file other.elf` and `symbol-file filename` replace the main symbol file. `-readnow` forces reading the full
  symbol table instead of the default two-stage scan.

## Gotchas
- If both images define the same symbol (for example a handler or init function), a name breakpoint can resolve to the
  wrong image or to both; check with `info breakpoints` and prefer `file:line` or an address.
- `add-symbol-file`, `remove-symbol-file` and `symbol-file` do not repeat on RET.

## Verify
- [ ] `info symbol $pc` names the correct image on both sides of the jump.
- [ ] Breakpoints in the app hit when started from the bootloader.

## Checked
Method: docs-checked 2026-11-09 against the GDB manual pages Commands to Specify Files (Files.html, read in full for the symbol-file, add-symbol-file, remove-symbol-file, info files and maint info sections entries). Symbols.html was fetched but only used for general context. Removed unconfirmed claims: GDB 9/10 version gates, load command behaviour, .ramfunc and hbreak advice, symbol-pick order, debug-file-directory, VTOR notes.
