---
id: computing-software.software-engineering.assembly.linker-scripts
name: linker-scripts
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, linker-scripts, asm-linking]
level: advanced
status: docs-checked
description: "Write GNU ld linker scripts: ENTRY, SECTIONS, location counter, output sections, symbols, MEMORY regions, load addresses and discarding sections."
sources:
  - https://sourceware.org/binutils/docs/ld/Location-Counter.html
  - https://sourceware.org/binutils/docs/ld/MEMORY.html
  - https://sourceware.org/binutils/docs/ld/Output-Section-LMA.html
  - https://sourceware.org/binutils/docs/ld/Output-Section-Discarding.html
  - https://sourceware.org/binutils/docs/ld/Input-Section-Basics.html
  - https://sourceware.org/binutils/docs/ld/PROVIDE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Linker scripts
**Goal:** control exact section placement for freestanding and embedded code.

```ld
ENTRY(_start)
SECTIONS
{
    . = 0x80000;                         /* load address */
    .text   : { *(.text.boot) *(.text*) }
    .rodata : { *(.rodata*) }
    . = ALIGN(4096);
    .data   : { *(.data*) }
    __bss_start = .;
    .bss    : { *(.bss*) *(COMMON) }
    __bss_end = .;
    /DISCARD/ : { *(.comment) *(.note*) }
}
```
Use: `ld -T link.ld boot.o main.o -o kernel.elf`
- `-T scriptfile` replaces ld's default linker script (unless the script contains `INSERT`), so the script must describe the whole output.
- `.` is the location counter. Assigning to it moves it forward and never backwards inside an output section. Inside an output section description it is an offset from the start of that section, not an absolute address; outside one (directly in `SECTIONS`) it acts as an absolute address.
- `ALIGN(n)` returns the location counter rounded up to the next multiple of `n`; the single-argument form does not move the counter by itself, so assign it (`. = ALIGN(4096);`) to move.
- `*(COMMON)` collects common symbols, which the linker treats as an input section named `COMMON`; they normally go in `.bss`.
- Input sections are placed in the order the patterns appear: `*(.text) *(.rdata)` puts all `.text` first, while `*(.text .rdata)` interleaves them in input order. Both file names and section names may be wildcard patterns.
- A symbol assigned in the script (such as `__bss_start`) has the value of that address; C code declares it `extern char __bss_start;` and uses `&__bss_start` (the manual's ROM example does this with `_etext`, `_bstart`, `_bend`).
- `MEMORY { ROM (rx) : ORIGIN = 0, LENGTH = 256K }` describes regions; the optional attribute letters are R, W, X, A, I, L and `!` to invert. An output section is directed to a region with `> ROM`. `ORIGIN(mem)` and `LENGTH(mem)` read a region.
- `AT(addr)` sets an output section's load address (LMA) apart from its run address (VMA); `AT>region` takes the next free address in a region. The location counter holds the VMA, not the LMA. This is the basis of ROM images where initialised data is copied to RAM at start-up.
- `KEEP(*(.init))` protects an input section from `--gc-sections` garbage collection.
- `PROVIDE(sym = .)` defines the symbol only if it is referenced but not defined by any object in the link.
- `/DISCARD/` as an output section name drops the input sections assigned to it.
- Empty output sections are not created; `. = .` inside the script forces one.
- `readelf -l` (`--program-headers`, also `--segments`) shows the program headers; `-Map=file` shows what went where.

## Gotchas
- Moving `.` backwards (for example forcing a smaller section than its contents) is an error.
- Symbols that capture `.` outside an output section can land in surprising places when the linker places orphan sections; assign `. = .;` before such a symbol to group it with the following section.
- Without `/DISCARD/` or `--gc-sections` (off by default), unused sections stay in the image.

## Self-check
Zero `.bss` using the script's symbols, then verify with a debugger that the range is zero.

## Checked
2026-11-08. Checked against the GNU ld manual pages: The Location Counter, MEMORY Command, Output Section LMA, Output Section Discarding, Input Section Basics, Input Section for Common Symbols, Input Section and Garbage Collection, PROVIDE, Builtin Functions (ALIGN, ORIGIN, LENGTH), Options (-T, --gc-sections, -Map) and the binutils readelf page. Removed: the claim that the boot section must come first because the CPU jumps to a fixed address (ordering rules are as above; the hardware reason is not in the pages), and the assembly snippets `ldr x0, =__bss_start` and `lea rdi, [rel __bss_start]` (the manual shows C access instead).

Method: documentation only; no commands were run.
