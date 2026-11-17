---
id: computing-software.firmware-embedded-development.stm32.cubemx-project-manager-options
name: cubemx-project-manager-options
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-cube, cubemx-project-manager, code-generator-options, toolchain-ide, peripheral-init-files, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Set STM32CubeMX Project Manager options for maintainable code: toolchain choice, per-peripheral .c/.h files, pinned firmware package, HAL vs LL and init order."
sources:
  - https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
  - https://wiki.st.com/stm32mcu/wiki/STM32CubeMX_basics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CubeMX Project Manager options

## Project tab
- **Toolchain/IDE**: STM32CubeIDE, CMake (CubeMX 6.11+), Makefile, EWARM, MDK-ARM. Choose CMake
  for VS Code/CI; CubeIDE for ST's debugger integration. Changing later regenerates build files.
- **Firmware package**: "Use latest" vs a specific version. Pin a version in team projects:
  different developers otherwise generate against different HAL versions.
- **Use default firmware location** off: point to a repo-relative copy if you vendor the package.
- Linker settings: minimum heap/stack sizes (`_Min_Heap_Size`, `_Min_Stack_Size`) are only a link-time check.

## Code Generator tab
| Option | Recommendation |
|---|---|
| Copy only necessary library files | yes (smaller repo) |
| Generate peripheral initialization as a pair of .c/.h per peripheral | yes: `usart.c`, `spi.c` instead of a giant main.c |
| Keep User Code when re-generating | yes |
| Delete previously generated files when not re-generated | yes, so disabled peripherals vanish |
| Set all free pins as analog | yes for low power |
| Enable Full Assert | yes in debug (`USE_FULL_ASSERT`), implement `assert_failed` |

## Advanced Settings tab
- **Driver selector**: HAL or LL per peripheral. LL for tight ISRs (USART, GPIO, TIM) while
  keeping HAL for complex ones (USB, SDMMC).
- **Generated function calls**: order of `MX_xxx_Init()` calls. DMA init must come before the
  peripherals that use DMA (older CubeMX versions generated it after, a classic bug: tick the
  order so MX_DMA_Init runs first).
- "Do not generate function call" lets you call `MX_xxx_Init` yourself later (e.g. only after a
  power rail is enabled). "Visibility (Static)" hides init functions.
- Register callbacks (`USE_HAL_xxx_REGISTER_CALLBACKS`) per peripheral.

## Version control
Commit the `.ioc` file and generated code together. Review diffs after regeneration: CubeMX
upgrades sometimes change init code. Record the CubeMX version in the README; the `.ioc`
stores it (`MxCube.Version`).

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Fresh clone + regenerate on another machine gives no diff.
- [ ] `MX_DMA_Init()` precedes DMA-using peripheral inits in `main.c`.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com, wiki.st.com); no readable alternative was found.

Method: documentation only; no commands were run.
