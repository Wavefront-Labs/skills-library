---
id: computing-software.firmware-embedded-development.stm32.x-cube-expansion-packs
name: x-cube-expansion-packs
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [x-cube-packs, stm32cubemx, software-packs, cmsis-pack, x-cube-mems1, x-cube-ai, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Add ST X-CUBE expansion packages (sensors, AI, connectivity, middleware) to an STM32CubeMX project: install, select components, configure, and keep versions reproducible."
sources:
  - https://www.st.com/resource/en/user_manual/um1718-stm32cubemx-for-stm32-configuration-and-initialization-c-code-generation-stmicroelectronics.pdf
  - https://www.st.com/en/embedded-software/stm32cube-expansion-packages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X-CUBE expansion packs

X-CUBE packages are CMSIS-Pack-format bundles that plug middleware and board support into
CubeMX: X-CUBE-MEMS1 (ST MEMS sensor drivers and algorithms), X-CUBE-AI (neural networks),
X-CUBE-SUBG2, X-CUBE-NFC, X-CUBE-CRYPTOLIB, X-CUBE-TOF1 and many more, plus partner packs.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Install
CubeMX: **Help > Manage embedded software packages** (Alt+U), tab *STMicroelectronics* (or a
partner tab), tick the pack and version, *Install*. Offline: *From Local...* with a `.pack`
file. Packs land in the repository folder (default `<home>/STM32Cube/Repository/Packs/<vendor>/<pack>/<version>`).

## Add to the project
1. **Software Packs > Select Components** (Alt+O).
2. Expand the pack, pick components (e.g. *Board Part > AccGyr > LSM6DSO / I2C*,
   *Device Application > DataLogExtended*). Dependencies show as warnings until satisfied.
3. Back in *Pinout & Configuration*, the pack appears under *Middleware and Software Packs*.
   Enable it, set parameters, and map **platform settings** (which I2C/SPI instance, which
   GPIOs/EXTI lines the component uses).
4. Generate code. Pack sources go under `Middlewares/` and `<pack>/Target/` glue
   (`custom_mems_conf.h`, BSP bus functions); application templates may add `app_<pack>.c`
   with `MX_<PACK>_Init()` / `MX_<PACK>_Process()` calls in `main.c`.

## Reproducibility
- The `.ioc` records the pack name and **version**. Another machine without that version
  installed gets a prompt (or silently migrates). Document required packs/versions in the README.
- Commit the generated pack sources so CI doesn't need CubeMX at all.
- Upgrading a pack is a code change: regenerate on a branch, diff `Middlewares/` and glue
  files, retest.

## Working with generated glue
- Platform glue files (`*_conf.h`, `*_bus.c`) contain the instance mapping; edits outside
  `USER CODE` blocks are lost on regeneration. Change mappings in CubeMX instead.
- Some application templates poll in `MX_<PACK>_Process()` from the main loop; with an RTOS,
  move that into a task and make sure the pack's bus functions are thread-safe (wrap shared I2C
  with a mutex).
- License: packs carry their own licence terms (often SLA0044 or BSD-3); check before
  shipping, especially for algorithm libraries delivered as binaries.

## Without CubeMX
Packs are zip files: you can unpack and add sources to CMake manually, but you lose the
platform-settings generation. Usually only worth it for a single driver.

## Verify
- [ ] Required packs and versions listed in the README; `.ioc` opens without migration prompts.
- [ ] Generated pack code committed; CI builds without CubeMX installed.
- [ ] Pack components' bus access is safe under the project's concurrency model.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
