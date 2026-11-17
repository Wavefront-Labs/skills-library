---
id: computing-software.firmware-embedded-development.bare-metal-programming.linker-defined-symbols-loadaddr-align
name: linker-defined-symbols-loadaddr-align
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [linker-symbols, linker-script, loadaddr, provide, gnu-ld, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Define and consume GNU ld symbols (LOADADDR, ADDR, SIZEOF, ALIGN, PROVIDE) from C correctly: copy tables, region bounds and why you take their address, not value."
sources:
  - https://sourceware.org/binutils/docs/ld/Builtin-Functions.html
  - https://sourceware.org/binutils/docs/ld/Source-Code-Reference.html
  - https://sourceware.org/binutils/docs/ld/PROVIDE.html
  - https://sourceware.org/binutils/docs/ld/Miscellaneous-Commands.html
  - https://sourceware.org/binutils/docs/ld/Output-Section-LMA.html
  - https://sourceware.org/binutils/docs/ld/Location-Counter.html
  - https://sourceware.org/binutils/docs/ld/Expression-Section.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linker-defined symbols with LOADADDR and ALIGN

**Goal:** firmware learns its own memory layout (where `.data` is stored in flash, where `.bss`
ends, how big the image is) from symbols the linker computes, with no hard-coded addresses.

## Defining symbols
```ld
.data : ALIGN(4) {
    _sdata = .;
    *(.data*)
    . = ALIGN(4);
    _edata = .;
} > RAM AT > FLASH
_sidata = LOADADDR(.data);          /* flash address of the initial values */

_image_end   = LOADADDR(.data) + SIZEOF(.data);
_image_size  = _image_end - ORIGIN(FLASH);
PROVIDE(_app_header_offset = 0x200);    /* defined only if code references it and nobody else defines it */
ASSERT(_image_size <= LENGTH(FLASH) - 0x4000, "image overlaps the settings sector")
```
Builtins: `ADDR(sec)` (VMA), `LOADADDR(sec)` (absolute LMA), `SIZEOF(sec)` (bytes, zero if the section
is not allocated), `ALIGN(n)` (the location counter rounded up to the next n boundary; it does not move
the counter), `ORIGIN(region)`, `LENGTH(region)`, `MAX/MIN`, `DEFINED(sym)`. `ASSERT(exp, message)`
fails the link when exp is zero. `AT>` sets the load address to the next free address in the named region.

## Consuming them in C: take the address
A linker symbol is an *address with no storage*. Declare it as an array (or char) and use the
symbol name itself as the address:
```c
extern uint32_t _sdata[], _edata[], _sidata[];
extern const char _image_size[];      /* the "value" is the address */

memcpy(_sdata, _sidata, (size_t)((char *)_edata - (char *)_sdata));
size_t sz = (size_t)_image_size;      /* NOT *_image_size */
```
Reading `extern uint32_t _image_size; x = _image_size;` dereferences address `_image_size`, which
returns whatever bytes sit there. Declaring as an array makes the misuse hard to write.

## Copy tables for several sections
Instead of one `memcpy` per section, emit a table the startup loops over:
```ld
.copy.table : ALIGN(4) {
    __copy_table_start__ = .;
    LONG(LOADADDR(.data))    LONG(ADDR(.data))    LONG(SIZEOF(.data) / 4)
    LONG(LOADADDR(.ramfunc)) LONG(ADDR(.ramfunc)) LONG(SIZEOF(.ramfunc) / 4)
    __copy_table_end__ = .;
} > FLASH
```
The table layout is your own convention: the startup code and the linker script must agree on it.

## Gotchas
- `ALIGN(4)` before an end symbol matters: the word-copy loop otherwise misses the last 1-3 bytes.
- Inside a section description `.` is a byte offset from the start of that section, and a symbol
  assigned from it is section-relative; use `ABSOLUTE(.)` to force an absolute value. `LOADADDR()`
  also forces an expression absolute. The LMA is not the location counter: `.` holds the VMA.
- ld treats an assignment outside any section as belonging to the previous output section, except
  an assignment to `.`. An orphan section the script does not mention can land between your start
  and end symbols; write `. = . ;` before a start symbol to keep it with the section that follows,
  or use `ADDR()`/`SIZEOF()`.
- `PROVIDE` treats a common symbol as defined, so it will not override one.

## Verify
- [ ] `arm-none-eabi-nm -n app.elf | grep -E '_s(i)?data|_edata|_image'` matches the map file.
- [ ] `ASSERT` fires when you deliberately bloat the image.
- [ ] Initialised globals hold their values after reset (copy loop uses the right LMA).

## Checked
2026-11-08. Confirmed in the GNU ld manual (Builtin Functions, Source Code Reference, PROVIDE, Miscellaneous
Commands, Output Section LMA, Location Counter, The Section of an Expression): LOADADDR, ADDR, SIZEOF, ALIGN,
ORIGIN, LENGTH, MAX, MIN, DEFINED, ASSERT, AT>, PROVIDE semantics, address-not-value rule for C access,
section-relative location counter, orphan-section behaviour. Removed: the CMSIS-Core copy-table claim (the CMSIS
startup page does not mention it) and the LTO/`-fdata-sections` claim (not in the cited pages).
Method: documentation only; no commands were run.
