---
id: computing-software.firmware-embedded-development.stm32.stm32cube-firmware-package-versions
name: stm32cube-firmware-package-versions
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-cube, stm32cube-firmware-package, stm32cubef4, hal-version-upgrade, cmsis-pack, stm32, firmware-embedded-development]
level: practitioner
status: draft
description: "Manage STM32Cube MCU firmware package versions (STM32CubeF4, CubeL4, CubeH7...): pinning, upgrading HAL safely, reading release notes and using the GitHub repos."
sources:
  - https://github.com/STMicroelectronics/STM32CubeF4
  - https://www.st.com/en/embedded-software/stm32cube-mcu-mpu-packages.html
  - https://wiki.st.com/stm32mcu/wiki/STM32CubeMX_basics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cube firmware package versions

Each series has an MCU package (`STM32CubeL4 V1.18.x`) containing HAL/LL drivers, CMSIS device
headers, BSP, middleware and examples. CubeMX downloads them to its repository folder.

## Where versions live
- `.ioc` file: `ProjectManager.FirmwarePackage=STM32Cube FW_L4 V1.18.0`.
- Drivers: `Drivers/STM32L4xx_HAL_Driver/Release_Notes.html` and `stm32l4xx_hal.c`
  `__STM32L4xx_HAL_VERSION`.
- GitHub: `github.com/STMicroelectronics/STM32CubeL4` with tags per release, plus separate
  `stm32l4xx_hal_driver` and `cmsis_device_l4` repos for submodule use.

## Pinning
Commit generated `Drivers/` into the repo (or use the GitHub driver repos as git submodules at a
tag). Then builds don't depend on whatever package each developer has installed.

## Upgrading
1. Read release notes between versions: look for "Fixed", "Known limitations", and API changes
   (e.g. UART `HAL_UARTEx_ReceiveToIdle_DMA` added, I2C timing changes, `HAL_xxx_RegisterCallback`).
2. In CubeMX: Project Manager > Firmware package > select new version > "Migrate".
3. Regenerate, diff `Drivers/` and generated init code, build with `-Wall -Werror`.
4. Rerun hardware regression tests, especially peripherals mentioned in release notes.

## Patches
Packages come in "V1.x.0" plus patch releases on GitHub (`V1.x.y`) that CubeMX may not offer
immediately. Patch releases fix bugs (e.g. USB, Ethernet) worth taking.

## Errata vs driver bugs
Silicon errata (ES documents) are separate from HAL bugs; HAL sometimes implements
workarounds. Read your part's errata sheet alongside driver notes.

## Verify
- [ ] Package version recorded in README and in the `.ioc`.
- [ ] CI builds from repo content only (no CubeMX repository path).
