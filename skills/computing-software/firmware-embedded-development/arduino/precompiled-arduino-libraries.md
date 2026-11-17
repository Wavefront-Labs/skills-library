---
id: computing-software.firmware-embedded-development.arduino.precompiled-arduino-libraries
name: precompiled-arduino-libraries
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [precompiled-library, precompiled-true, ldflags, static-library, binary-distribution, mcu-subfolder, arduino, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Ship an Arduino library as precompiled .a files: precompiled=true/full, src/<build.mcu>/ folder naming, FPU variants, ldflags, and ABI/compiler-version pitfalls."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/library-specification.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Precompiled libraries

Use when distributing closed-source code (vendor algorithms, sensor fusion) or to cut build time.

## library.properties
```properties
precompiled=true      # source files are always compiled (mixed libraries: open sources + closed .a)
# precompiled=full    # sources are NOT compiled when a .a exists for the board, compiled as a fallback otherwise (CLI 0.11.0+)
ldflags=-lAcmeFusion  # linker flags; the static library is linked as an ldflag (libAcmeFusion.a)
```

## Folder layout
The `.a` files go in a subfolder of `src/` named after the board's `build.mcu` value, optionally
with FPU and float ABI variants:
```
AcmeFusion/
  library.properties
  src/
    AcmeFusion.h
    cortex-m4/fpv4-sp-d16-softfp/libAcmeFusion.a
    cortex-m4/libAcmeFusion.a          # fallback when no FPU folder matches
    cortex-m0plus/libAcmeFusion.a
```
The files are named `lib<name>.a` (or `.so`). The builder looks for
`src/{build.mcu}/{build.fpu}-{build.float-abi}/` (CLI 0.8.0 and later) and falls back to `src/{build.mcu}/`.
From CLI 1.6.0 the `build.fpu` and `build.float-abi` platform properties are used directly; otherwise the values
are detected from `-mfpu=` and `-mfloat-abi=` in the compile recipe. Check a board's values with
`arduino-cli compile -b <fqbn> --show-properties` (look at `build.mcu`, `build.fpu`, `build.float-abi`).

## Building the archives
Compile with the same toolchain and flags the core uses (take them from `--show-properties` or a
verbose build) and archive the objects into `lib<name>.a`. The floating-point flags (`-mfloat-abi`, `-mfpu`)
must match the folder you put the archive in.

## Pitfalls
- A board with no matching `src/{build.mcu}` folder has no binary to link: ship sources and use
  `precompiled=full` as the fallback, or document the supported MCUs and set `architectures=` accordingly.

## Verify
- [ ] Example sketch builds and links on every MCU folder shipped.
- [ ] Verbose compile output shows the `.a` from the correct folder being linked.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 library specification on master (commit 2026-10-22).

Confirmed: `precompiled=true` always compiles source files (for mixed libraries) and `precompiled=full` skips sources when a precompiled library exists for the board and compiles them as a fallback otherwise (full available from CLI 0.11.0); the binaries sit in `src/{build.mcu}` with an optional `{build.fpu}-{build.float-abi}` subfolder (CLI 0.8.0 and later) and fall back to `src/{build.mcu}`; file names start with `lib`; `ldflags` carries linker flags and the static library is linked as an ldflag; `build.fpu` and `build.float-abi` properties are used directly from CLI 1.6.0, otherwise detected from `-mfpu=` and `-mfloat-abi=` in the compile recipe. Fixed: the skill had the meanings of `true` and `full` reversed, gave the wrong CLI version for `full` and claimed the archive is linked automatically. Removed unconfirmed claims about GCC upgrades, LTO and Library Manager acceptance.

Method: documentation only; no commands were run.
