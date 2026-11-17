---
id: computing-software.firmware-embedded-development.bare-metal-programming.firmware-code-size-optimization
name: firmware-code-size-optimization
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [code-size-optimization, os-optimization, oz, flash-footprint, puncover, bloaty, map-file, printf-size, arm-none-eabi-gcc, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Shrink firmware flash usage systematically: measure with size/nm/map files and bloaty, then -Os/-Oz, gc-sections, nano libc, printf and float removal, and code hygiene."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Optimize-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Common-Function-Attributes.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Warning-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/C_002b_002b-Dialect-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Link-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
  - https://sourceware.org/binutils/docs/binutils/nm.html
  - https://sourceware.org/binutils/docs/binutils/size.html
  - https://sourceware.org/binutils/docs/ld/Options.html
  - https://github.com/google/bloaty
  - https://github.com/HBehrens/puncover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code size optimisation

**Goal:** fit the image in flash (or leave room for A/B slots) by attacking the biggest
contributors first, guided by measurement rather than folklore.

## Measure first
```sh
arm-none-eabi-size -A app.elf                         # per-section sizes
arm-none-eabi-nm --size-sort -S -C app.elf            # symbols sorted by size, biggest last
bloaty app.elf -d compileunits                        # who owns the bytes
```
- `size -A` selects the System V style output (`-B` is Berkeley; the default is a one-line
  Berkeley-like format).
- `nm --size-sort` sorts by size; `-S` (`--print-size`) prints the size alongside the value for the
  bsd output style; `-C` demangles C++ names.
- Bloaty is a size profiler for binaries (ELF among others) with data sources such as
  `compileunits`, symbols and sections, hierarchical profiles, and size diffs that suit CI.
- Ask the linker for a map file: `-Wl,-Map=app.map` (GCC passes it to GNU ld; ld also has
  `--print-map-discarded` for what was dropped) to see what pulled in library objects.
- puncover analyses an ELF for code size, static variables and stack usage, with a browsable
  report; stack numbers need `-fstack-usage` (`.su` files) and `--build_dir`. It can save a JSON
  report (`--generate-report --non-interactive --report-type json`) for CI.

## Big wins, roughly in order
1. **`-Os`** (optimise for size: `-O2` minus the optimisations that often grow code) or
   **`-Oz`** (more aggressive; GCC warns it may execute more instructions if they encode in fewer
   bytes). Keep `-O2` only on hot files via per-file flags or
   `__attribute__((optimize("O2")))` (GCC's `optimize` attribute behaves as if its arguments were
   appended to the command line).
2. **`-ffunction-sections -fdata-sections -Wl,--gc-sections`**: each function/data item gets its
   own section, and `--gc-sections` lets the linker drop unused input sections (see
   `linker-section-garbage-collection`).
3. **newlib-nano**: a smaller C library; see `newlib-nano-and-syscall-stubs` for the flags and
   the syscalls you must supply. Check the map file for the printf implementation that was linked.
4. **Drop printf entirely**: a tiny formatter, or deferred logging that sends format IDs
   instead of strings, removes the library formatter and the format strings from flash.
   Measure with the map file.
5. **Avoid double on single-precision FPUs**: GCC's `-Wdouble-promotion` text says a CPU with
   a 32-bit single-precision unit implements `float` in hardware but emulates `double` in
   software, and floating-point literals are implicitly `double`. Use the warning and `f`
   suffixes, and check the map file for soft-float helpers.
6. **LTO** (`-flto`): the link-time optimiser instantiates all function bodies as if in one
   translation unit. GCC recommends passing the same options at compile and link time. Measure
   the size change yourself; see `link-time-optimization-pitfalls`.
7. **C++**: `-fno-rtti` drops run-time type information for classes with virtual functions
   (exception handling still generates what it needs); `-fno-threadsafe-statics` omits the
   guard code for local statics where thread safety is not needed. Avoid iostream and
   `std::function`; templates instantiated per type add up.
8. **HAL bloat**: vendor HAL init functions handle every mode; LL drivers or direct
   register writes are usually smaller for hot paths. Compare symbol sizes with `nm`.

## Smaller wins
- `assert` messages: replace file/line strings with a PC-only assert (`__builtin_return_address`).
- Lookup tables in flash (`const`), not built at runtime in RAM.
- Duplicate inlined code from large `static inline` functions in headers.
- `-mslow-flash-data` (ARMv7 M-profile only, off by default) minimises literal loads for
  performance, and `-mpure-code` keeps constant data out of code sections; neither is a size
  option, so leave them off unless you have a reason.
- Compressed images and bootloader-side decompression only as last resort.

## Gotchas
- `-Os` and `-Oz` can be slower; measure critical loops (DWT) after switching.
- For debug builds GCC recommends `-Og` over `-O0`: it keeps a good debugging experience while
  optimising, and `-O0` is the default when no level is given.

## Verify
- [ ] Size budget check in CI fails the build on regression above a threshold.
- [ ] Functional tests still pass after optimisation-level changes.

## Checked
Checked 2026-11-08 against GCC 14.2 Optimize Options (`-Os`, `-Oz`, `-Og`, `-O0`, `-flto`,
`-ffunction-sections`), Common Function Attributes (`optimize`), Warning Options
(`-Wdouble-promotion`), C++ Dialect Options (`-fno-rtti`, `-fno-threadsafe-statics`), Link
Options (`-Wl,`), the GCC ARM Options page (`-mslow-flash-data`, `-mpure-code`), binutils `nm`
and `size`, the ld manual (`--gc-sections`, map options), and the bloaty and puncover READMEs.
Removed because no readable page states them: `--specs=nano.specs` and `-u _printf_float` with its
~10 KB cost, named tiny printf libraries and the 5-20 KB saving, `__aeabi_d*` helper names, the
5-15 % LTO gain, `-fno-exceptions`, the "GCC 12+" version gate for `-Oz`, the "2-3x larger"
figure for `-O0` builds, and the `.data` load-address note.
Method: documentation only; no commands were run.
