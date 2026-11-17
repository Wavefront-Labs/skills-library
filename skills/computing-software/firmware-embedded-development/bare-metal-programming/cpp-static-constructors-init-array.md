---
id: computing-software.firmware-embedded-development.bare-metal-programming.cpp-static-constructors-init-array
name: cpp-static-constructors-init-array
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [init-array, startup-code, cpp-embedded, libc-init-array, static-initialization-order, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run C++ global constructors on bare-metal Cortex-M: .init_array in the ld script, calling the table from startup, and static init order and peripheral-access traps."
sources:
  - https://sourceware.org/binutils/docs/ld/Input-Section-Keep.html
  - https://sourceware.org/binutils/docs/ld/Input-Section-Wildcards.html
  - https://sourceware.org/binutils/docs/ld/Options.html
  - https://itanium-cxx-abi.github.io/cxx-abi/abi.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/C_002b_002b-Attributes.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Common-Function-Attributes.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/C_002b_002b-Dialect-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C++ static constructors and init_array

**Goal:** global and namespace-scope C++ objects (and C functions marked `constructor`) are
initialised exactly once, before `main`, in a controlled order.

## Link script
```ld
.init_array : {
    PROVIDE_HIDDEN(__init_array_start = .);
    KEEP(*(SORT(.init_array.*)))     /* per-priority sections, sorted by name */
    KEEP(*(.init_array*))
    PROVIDE_HIDDEN(__init_array_end = .);
} > FLASH
.fini_array : { ... } > FLASH       /* destructors: never run on firmware that never exits */
```
- The linker manual's `SORT_BY_INIT_PRIORITY` note says the section name carries the priority:
  in `.init_array.NNNNN` and `.fini_array.NNNNN`, NNNNN is the `init_priority` (in `.ctors.NNNNN`
  and `.dtors.NNNNN` it is 65535 minus the priority). `SORT` is an alias for `SORT_BY_NAME`.
- `KEEP()` around an input-section wildcard marks it not to be eliminated when `--gc-sections`
  is in use (the manual's examples are `KEEP(*(.init))` and `KEEP(SORT_BY_NAME(*)(.ctors))`).
  `--gc-sections` keeps the section holding the entry symbol and sections holding symbols
  undefined on the command line, then recursively whatever they reference through relocations.
  Nothing references the `.init_array` entries themselves, so without `KEEP` expect the table to
  be dropped: constructors never run and objects stay zero-initialised.

## Startup
Reset code must copy `.data`, zero `.bss`, set up clocks if constructors touch peripherals, then
call each function pointer from `__init_array_start` up to `__init_array_end` (symbols defined by
your own script above) before `main`. If your C library ships a routine that does this, make
sure the startup file and link options actually include it; check the map file.

## Traps
- **Static initialisation order fiasco:** Standard C++ guarantees order only within one
  translation unit; across units there is no guarantee. A global `Uart debug;` used inside
  another global's constructor may not be constructed yet. Use function-local statics
  (`Uart &debug() { static Uart u; return u; }`) or GCC's `init_priority` attribute: a constant
  integral expression currently bounded between 101 and 65535 inclusive, lower numbers meaning
  higher priority (earlier).
- **`constructor` attribute functions:** GCC runs them before `main`; a smaller priority number
  runs first and 0-100 are reserved. The relative order of C++ static objects and
  `constructor`-attribute functions is unspecified, and `init_priority` can impose an order in
  mixed declarations. On targets without support, the priority form is an error.
- **Thread-safe local statics:** the C++ ABI defines `__cxa_guard_acquire` and release for
  thread-safe initialisation of local statics. `-fno-threadsafe-statics` omits that extra code
  and GCC says to use it only for code that does not need to be thread-safe. With an RTOS, keep
  the guards and supply implementations that lock.
- **Touching hardware in constructors:** clocks may not be configured yet. Prefer constructors
  that only store config; do hardware in an `init()` called from `main`.
- **Destructors and atexit:** with `-fuse-cxa-atexit` GCC registers static destructors through
  `__cxa_atexit`, which your C library must provide. The Itanium ABI says it returns zero when
  registration succeeds, so a firmware that never exits can provide a stub returning 0.

## Verify
- [ ] `arm-none-eabi-objdump -h app.elf` shows an `.init_array` section with non-zero size.
- [ ] A global with a constructor that sets a flag reads true in `main`.
- [ ] `nm` shows no `__cxa_guard_acquire` on a bare-metal single-thread build (if intended).

## Checked
Checked 2026-11-08 against the binutils ld manual (Input Section and Garbage Collection,
Input Section Wildcards, Options for `--gc-sections`), the Itanium C++ ABI (guard routines,
`__cxa_atexit`), and GCC 14.2 C++ attributes (`init_priority`), Common Function Attributes
(`constructor`) and C++ Dialect Options (`-fno-threadsafe-statics`, `-fuse-cxa-atexit`).
Removed because no readable page states them: the `.preinit_array` output section, `__libc_init_array`
and its call order, the `_init` / `-nostartfiles` link failure, the `-fno-use-cxa-atexit` RAM
saving, and the constexpr-constructor advice. The `PROVIDE_HIDDEN` symbol names are the example
script's own.
Method: documentation only; no commands were run.
