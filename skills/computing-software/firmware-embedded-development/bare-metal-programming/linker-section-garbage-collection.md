---
id: computing-software.firmware-embedded-development.bare-metal-programming.linker-section-garbage-collection
name: linker-section-garbage-collection
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [gc-sections, function-sections, data-sections, keep, dead-code-elimination, print-gc-sections, gnu-ld, arm-none-eabi-gcc, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Strip unused code and data with -ffunction-sections, -fdata-sections and --gc-sections: KEEP for vectors and tables, --print-gc-sections, and debugging vanished symbols."
sources:
  - https://sourceware.org/binutils/docs/ld/Options.html
  - https://sourceware.org/binutils/docs/ld/Input-Section-Keep.html
  - https://sourceware.org/binutils/docs/ld/Input-Section-Wildcards.html
  - https://sourceware.org/binutils/docs/ld/Entry-Point.html
  - https://gcc.gnu.org/onlinedocs/gcc/Common-Attributes.html
  - https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Section garbage collection

**Goal:** only code and data reachable from the entry point and kept roots end up in flash.

## Flags
```sh
CFLAGS  += -ffunction-sections -fdata-sections
LDFLAGS += -Wl,--gc-sections
```
- The two compiler options place each function or data item in its own section, named after the
  function or item. `--gc-sections` can then drop each one independently; without the options a
  whole object file's code stays in one section and is kept or dropped together.
- Libraries (newlib, vendor HAL archives) only benefit if they were also built with these flags.
- GCC warns that the options make object and executable files larger, slow the assembler and
  linker, and prevent some intra-unit optimisations (for example relaxing calls to short call
  instructions). Measure the saving with `size` instead of assuming it.
- `--gc-sections` is ignored on targets that do not support it, and is off by default.

## Roots: what keeps a section alive
The entry symbol (`ENTRY(Reset_Handler)` or `--entry`), symbols forced with `-u`/`--undefined`
or `EXTERN()`, sections wrapped in `KEEP()`, and anything referenced from those. Things nothing
references must be `KEEP`'d:
```ld
.isr_vector : { KEEP(*(.isr_vector)) } > FLASH
.init_array : { KEEP(*(SORT(.init_array.*))) KEEP(*(.init_array)) } > FLASH
.cmd_table  : { __cmd_start = .; KEEP(*(.cmd_table*)) __cmd_end = .; } > FLASH
```
Linker-generated tables (shell commands, test registrations, device lists collected with
section attributes) are the usual victims: they compile fine and silently disappear.

## Diagnosing
- `-Wl,--print-gc-sections` lists every removed section on stderr; search it for a missing symbol.
- `-Wl,-Map=app.map,--cref` adds a cross-reference table to the map file: for each symbol, the
  file that defines it and the files that reference it.
- `arm-none-eabi-nm --size-sort -S app.elf | tail -30` for the largest survivors.
- A function only reached through a pointer stored in a removed table also vanishes:
  fix the table's `KEEP`, not the function.

## Gotchas
- `__attribute__((used))` makes the compiler emit a function or static variable even if it
  looks unreferenced; it does not protect the section from `--gc-sections`. GCC's `retain`
  attribute does that for GNU and FreeBSD ELF targets (it needs Binutils 2.36 or later);
  otherwise use `KEEP` or `-u symbol`.
- Data placed with `__attribute__((section(".foo")))` needs a matching `*(.foo*)` entry in the
  script. An orphan section (one the script does not mention) is placed by ld heuristics,
  after sections of the same attributes where it can; `--orphan-handling=warn` or `error`
  reports them.
- Debug info is not affected; size of the ELF on disk is not flash usage. Use
  `arm-none-eabi-size`.

## Verify
- [ ] `size` before/after shows the reduction.
- [ ] Vector table at flash origin is intact (`objdump -s -j .isr_vector`).
- [ ] Every linker-collected table has the expected entry count at runtime.

## Checked
2026-11-08. Confirmed in the GNU ld manual (Options: `--gc-sections`, `--print-gc-sections`, `--cref`, `-u`,
`--orphan-handling`; Input Section and Garbage Collection; Input Section Wildcards: `SORT` is an alias for
`SORT_BY_NAME`; Entry Point; Orphan Sections) and the GCC manual (`-ffunction-sections`/`-fdata-sections`, the
`used`, `retain` and `section` attributes). Removed: the 20-50 % saving figure, the claim that the ARM toolchain's
newlib is built with these flags, and the LTO remark (none appear in the cited pages). The nm, size and objdump
commands in the checklist were not checked against a manual.
Method: documentation only; no commands were run.
