---
id: computing-software.firmware-embedded-development.bare-metal-programming.link-time-optimization-pitfalls
name: link-time-optimization-pitfalls
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [link-time-optimization, lto, flto, gcc-ar, used-attribute, weak-symbols, interrupt-handlers, arm-none-eabi-gcc, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Enable -flto on bare-metal firmware without breaking it: asm-referenced symbols, gcc-ar archives, fat objects, mixed non-LTO objects, option consistency, debugging."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html
  - https://gcc.gnu.org/wiki/LinkTimeOptimization
  - https://gcc.gnu.org/onlinedocs/gccint/LTO.html
  - https://gcc.gnu.org/onlinedocs/gcc/Common-Attributes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Link-time optimisation pitfalls

**Goal:** get LTO's whole-program inlining and dead-code removal while avoiding the classic
embedded breakages. Measure the size and speed effect on your own firmware.

## Enabling
```sh
CFLAGS  += -O2 -flto
LDFLAGS += -O2 -flto            # optimisation options must also be passed at link time
AR = arm-none-eabi-gcc-ar       # wrapper that passes the linker plugin to ar
```
- GCC applies LTO to any object that carries bytecode, so `-flto` on the compile line is enough
  to trigger it; link with the GCC driver (not `ld` directly) so the optimiser runs.
- Compile every file in the link with the same options and repeat them at link time. Giving `-O`
  only at link time is generally ineffective: unoptimised compiles skip passes that gather
  information for link time. With no `-O` at link time, GCC uses the highest level used when
  compiling the objects.
- `-flto=auto` runs the link-time work in parallel (GNU make job server if present, otherwise
  the detected CPU thread count).
- To build static libraries LTO can see inside, use `gcc-ar` and `gcc-ranlib` (and `gcc-nm` to
  list symbols) instead of `ar`, `ranlib` and `nm`; they need plugin support. The link needs
  `-fuse-linker-plugin` so the archive's bytecode takes part in the optimisation.

## What breaks and the fix
| Symptom | Likely cause | Fix |
|---|---|---|
| Function used only from inline asm vanishes, "undefined reference" | LTO saw no C caller | `__attribute__((used))` (documented for functions referenced only in inline assembly) or `-Wl,-u,symbol` |
| Without the linker plugin, symbols used by non-LTO objects (vector table in assembly) look unreferenced | the compiler lacks used/exported symbol information | use a linker with plugin support and `-fuse-linker-plugin`; `-fwhole-program` is the fallback without it, and it assumes nothing outside the unit needs the symbols |
| Linker-collected table empty | section-attribute objects removed | `used` on the object plus `KEEP()` in the script |
| Options set at assembler level ignored or inconsistent | `-Wa`/`-Xassembler` options must match on all units | compile such units with `-fno-lto`, or use the same assembler options everywhere |

The GCC manual notes that C-linkage objects declared with incompatible types in different
translation units are undefined behaviour that LTO may diagnose; separate compilation hid such
bugs. Treat new failures after enabling LTO as real bugs first.

## Mixing
- GCC applies LTO only to files that contain bytecode, so you can mix LTO objects with
  ordinary objects and libraries (startup assembly, vendor binaries). `-fno-lto` on a file or
  on the link line turns LTO off for it.
- Bytecode is versioned with a strict version check: bytecode from one GCC version does not
  work with an older or newer one. A library intended for both LTO and normal links is built
  with `-flto -ffat-lto-objects`; fat objects hold bytecode plus final code. With
  `-fno-fat-lto-objects` (the default when the linker plugin is supported) a regular non-LTO link
  of those objects is not possible.

## Debugging LTO builds
- Pass `-g` at compile time; any object built with debug info enables it at link time. GCC
  says LTO does not work well with debug info outside ELF plus DWARF.
- `-flto-partition=1to1` is documented as a workaround for various code-ordering issues;
  `one` uses a single partition. The default is `balanced`.
- Inlining across files makes stepping jumpy; keep a non-LTO build to compare against and test both.

## Verify
- [ ] Every vector table entry resolves to the intended handler (`nm` + `objdump -s -j .isr_vector`).
- [ ] Full regression tests on the LTO image, not just the debug one.

## Checked
2026-11-08. Confirmed in the GCC manual (Optimize Options: `-flto`, `-flto=auto`, `-flto-partition`,
`-ffat-lto-objects`, `-fno-lto`, `-fuse-linker-plugin`, `-fwhole-program`, gcc-ar/gcc-ranlib/gcc-nm; Common
Attributes: `used`), the GCC internals LTO chapter and the GCC wiki LTO page. Removed: the 5-15 % size figure, the
CMake interprocedural-optimisation line, table rows about delay loops, MMIO reordering, `.ramfunc` inlining and
linker-script symbol aliasing, the `.lto_priv` map-file note and the `-flto-partition=one` determinism claim, none
of which the cited pages support. The nm and objdump commands were not checked against a manual.
Method: documentation only; no commands were run.
