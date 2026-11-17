---
id: computing-software.firmware-embedded-development.bare-metal-programming.multilib-selection-for-cortex-m
name: multilib-selection-for-cortex-m
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [multilib, arm-none-eabi-gcc, mcpu, mfloat-abi, libgcc-variant, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Make arm-none-eabi-gcc link the right multilib for your core and float ABI by passing the same -mcpu/-mfpu/-mfloat-abi flags at link time and checking with -print-multi-directory."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html
  - https://gcc.gnu.org/onlinedocs/gccint/Target-Fragment.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multilib selection for Cortex-M variants

A GCC toolchain for ARM builds the target libraries (libgcc.a at minimum) several times, once per supported combination of options, each in its
own directory.
GCC picks the directory by comparing the command-line options with the options each multilib
was built with, so the CPU and float flags must be on the **link** command as well as the
compile commands.

## Show what you get
```sh
arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard -print-multi-directory
arm-none-eabi-gcc -print-multi-lib
```
- `-print-multi-directory` prints the multilib directory selected by the other switches on the
  command line.
- `-print-multi-lib` prints the mapping from multilib directory names to the switches that
  enable them: the directory, then `;`, then each switch written with `@` instead of `-`.
- Run the first command with exactly your link flags. If the printed directory is `.` (the
  default), none of your options matched a Cortex-M multilib; compare against the
  `-print-multi-lib` list and fix the flags.

## Flags that matter
- `-mcpu=` names the core. `-mfpu=auto` is the default and derives the floating-point
  hardware from `-mcpu` and `-march`; an explicit `-mfpu=` overrides it.
- `-mfloat-abi=` selects the float ABI (`soft`, `softfp`, `hard`). The hard-float and
  soft-float ABIs are not link-compatible: compile and link the whole program with the same ABI.
- Extension suffixes switch features off on a named core: `-mcpu=cortex-m33+nofp` disables the
  floating-point instructions, `+nodsp` disables the DSP instructions, and `+nodp` disables
  double precision on `cortex-m7`.
- `-specs=nano.specs` and similar are driver specs files, processed after the standard specs;
  they change which libraries are linked, so check multilib output with them present too.

## CMake pattern
Put the CPU flags in both compile and link options:
```cmake
set(CPU_FLAGS -mcpu=cortex-m33 -mthumb -mfloat-abi=hard)
target_compile_options(app PRIVATE ${CPU_FLAGS})
target_link_options(app PRIVATE ${CPU_FLAGS})
```

## Verify
- [ ] `-print-multi-directory` with your exact link flags is not `.` and appears in `-print-multi-lib`.
- [ ] Every object and library in the image uses the same float ABI.

## Checked
Date: 2026-10-31.
Confirmed in the GCC manual (ARM Options, Developer Options) and GCC Internals (Target Fragment):
`-mfpu=auto` default behaviour, `-mfloat-abi=` values and ABI link compatibility, the `+nofp`/`+nodsp`/`+nodp` suffixes on the listed cores,
`-print-multi-directory` and `-print-multi-lib` semantics, `-specs=file` semantics, and that multilib selection
compares command-line options with the options each multilib was built with.
Removed as unconfirmed: specific directory names (`thumb/v7e-m+fp/hard` and others), the claim that
a `.` result means ARM-mode code and an INVSTATE fault, linker error text, GCC 11 version gate,
the `-print-multi-directory` clang statement, objdump/readelf verification tags, and the
`CMAKE_*_INIT` variable names.
Method: documentation only; no commands were run.
