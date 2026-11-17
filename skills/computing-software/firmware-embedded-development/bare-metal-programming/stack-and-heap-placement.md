---
id: computing-software.firmware-embedded-development.bare-metal-programming.stack-and-heap-placement
name: stack-and-heap-placement
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [stack-heap-placement, linker-script, main-stack, sbrk, heap-limit, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Reserve stack and heap space in a GNU ld script so over-committed RAM fails at link time, and write an _sbrk that honours a real heap limit; stack sizing with -fstack-usage."
sources:
  - https://sourceware.org/binutils/docs/ld/Scripts.html
  - https://sourceware.org/newlib/libc.html
  - https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack and heap size symbols and placement

**Goal:** a known stack and heap size, and a link failure when RAM is over-committed instead of a
field crash.

## Reserve space in the linker script
The linker script describes memory with a `MEMORY` command (regions with `ORIGIN` and `LENGTH`)
and places output sections into regions with `> region`. The linker reports an error if the
sections assigned to a region exceed its size, and it does not rearrange sections to make them
fit. That error is what turns an over-committed RAM budget into a build failure.

The location counter `.` can be advanced inside a section (`. = . + 1000;` or `. += 1000;`) to
reserve space; it cannot move backwards inside an output section. A `NOLOAD` section is marked
not loadable, so its contents are not loaded when the program runs.

```ld
_Min_Stack_Size = 0x800;
_Min_Heap_Size  = 0x1000;

SECTIONS {
  .stack (NOLOAD) : ALIGN(8) {
    . = . + _Min_Stack_Size;
    __StackTop = .;                 /* initial MSP goes in vector[0] */
  } > RAM
  .data : { ... } > RAM AT > FLASH
  .bss  (NOLOAD) : { ... } > RAM
  .heap (NOLOAD) : ALIGN(8) {
    __heap_start = .;
    . = . + _Min_Heap_Size;         /* reserve the minimum: link fails if RAM is short */
    __heap_end = .;
  } > RAM
}
```
`ORIGIN(RAM)` and `LENGTH(RAM)` can be used in expressions, for example to define a symbol at the
end of a region. Which end of RAM the stack sits at, and what happens when it overflows, depends
on the device's memory map: check the device reference manual (not covered by the pages cited here).

## _sbrk with a real limit
The newlib manual says `malloc` and related functions depend on `sbrk`, so a working
implementation is useful, and that on a bare board you must supply stubs to link with `libc.a`
(its list includes `sbrk`). Its example implementation uses the `_end` symbol defined by the GNU
linker. A limit-checking version using symbols from the script above:
```c
extern char __heap_start, __heap_end;
static char *brk = &__heap_start;
void *_sbrk(ptrdiff_t incr) {
    if (brk + incr > &__heap_end) { errno = ENOMEM; return (void *)-1; }
    char *prev = brk; brk += incr; return prev;
}
```
Whether to return `ENOMEM` follows the usual `sbrk` convention; the newlib page does not specify it.

## Sizing the main stack
- Static: GCC `-fstack-usage` writes a `.su` file (the dump name is the auxname with `.su`
  appended). Each entry is `static` (fixed frame) or `dynamic` (stack adjusted inside the body);
  `bounded` means the adjustment is bounded at compile time. `-fcallgraph-info=su` decorates the
  call graph with stack usage. Recursion and function pointers need a manual worst case.
- Dynamic: fill the stack with a known pattern in the reset handler, run worst-case tests, count
  untouched words.
- With nested interrupts, size the stack for the deepest nesting; exception frame sizes are in the
  Arm architecture manual for your core.

## Verify
- [ ] `arm-none-eabi-nm app.elf` shows `__StackTop` and `__heap_start`/`__heap_end` at the expected addresses.
- [ ] Increasing `_Min_Heap_Size` past free RAM makes the link fail with a region-overflow error.
- [ ] `malloc` returns NULL (not garbage) when the heap is exhausted.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the GNU ld manual (Scripts, MEMORY, Output Section Type, Location Counter), the newlib libc manual (system calls, sbrk) and the GCC manual (Developer Options: -fstack-usage, -fcallgraph-info). Removed because the Arm documentation pages could not be read: the claims that a stack at the bottom of RAM faults on overflow, the 8-byte MSP alignment rule, the 8-word and 26-word exception frame sizes, and the claim that vendor `_sbrk` implementations compare against the stack pointer. Removed the unsourced `GCC 10+` version, the `puncover` and `checkstack.pl` tool mentions, and the `. = ORIGIN(RAM) + LENGTH(RAM)` assignment inside a section, which the ld manual does not describe.
