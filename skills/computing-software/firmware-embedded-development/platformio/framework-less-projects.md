---
id: computing-software.firmware-embedded-development.platformio.framework-less-projects
name: framework-less-projects
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [no-framework, bare-metal-platformio, cmsis-only, custom-startup, linker-script, startup-file, platformio, firmware-embedded-development]
level: advanced
status: draft
description: "Build bare-metal PlatformIO projects with no framework: startup code, linker script, CMSIS headers, system init, while keeping size checks and debugging working."
sources:
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/platform/framework.html
  - https://docs.platformio.org/en/latest/platforms/creating_board.html
  - https://github.com/ARM-software/CMSIS_5
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Framework-less projects

Omit `framework` and PlatformIO builds only your sources with the platform's toolchain. You supply
everything a framework normally provides.

## Config
```ini
[env:bare_g0]
platform = ststm32
board = nucleo_g071rb
; no framework line
board_build.ldscript = linker/STM32G071RBTx_FLASH.ld
build_flags =
    -Iinclude/cmsis -Iinclude/device
    -DSTM32G071xx
    -ffunction-sections -fdata-sections
    -Wl,--gc-sections
    -nostartfiles                   ; only if your startup does not use crt0
    --specs=nano.specs --specs=nosys.specs
debug_tool = stlink
```

## What you provide
1. **Startup code**: vector table and `Reset_Handler` (copy `.data` from flash, zero `.bss`, call
   `SystemInit`, `__libc_init_array`, `main`). Use the vendor's `startup_stm32g071xx.s` (GCC version)
   in `src/` — PlatformIO compiles `.S` files; lowercase `.s` are assembled without the C
   preprocessor, rename to `.S` if they use `#define`.
2. **Linker script** with memory regions matching the chip and symbols the startup expects
   (`_sidata`, `_sdata`, `_edata`, `_sbss`, `_ebss`, `_estack`).
3. **CMSIS core + device headers** (`core_cm0plus.h`, `stm32g071xx.h`, `system_stm32g0xx.c`) in the
   project or as a library.
4. Optional newlib syscalls (`_write` for printf to UART, `_sbrk` for malloc).

## Keep platform features working
- Size check uses `board_upload.maximum_size`/`maximum_ram_size`; keep it consistent with the linker
  script.
- `pio debug` works because the board manifest's debug section is independent of frameworks.
- Upload uses the board's default protocol; the platform converts ELF to bin/hex as usual.

## Variants
- AVR without Arduino: `platform = atmelavr`, no framework, plain avr-libc `main()`; set
  `board_build.f_cpu`, use `-mmcu` from the board (automatic).
- RISC-V/others work the same when the platform supports framework-less builds.

## Gotchas
- Missing `-mthumb`/`-mcpu`: the platform adds them from the board's `build.cpu`; check `pio run -v`.
- Unused `--specs=nosys.specs` warnings about `_close`/`_lseek` in newer newlib are harmless; add
  stubs to silence them.
- C++ static constructors only run if startup calls `__libc_init_array`.

## Verify
- [ ] Blink from `main()` runs, vector table at the right address (`arm-none-eabi-objdump -h`).
- [ ] Map file shows no framework objects linked.
