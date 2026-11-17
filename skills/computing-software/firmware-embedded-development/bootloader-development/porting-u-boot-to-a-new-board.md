---
id: computing-software.firmware-embedded-development.bootloader-development.porting-u-boot-to-a-new-board
name: porting-u-boot-to-a-new-board
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [u-boot-porting, u-boot, board-defconfig, board-directory, dram-config, firmware-embedded-development]
level: sme
status: draft
description: "Port U-Boot to a custom board based on a reference design: copy the closest board, defconfig and device tree, DRAM timing, console UART, MAINTAINERS, and step-by-step bring-up."
sources:
  - https://docs.u-boot.org/en/latest/develop/porting.html
  - https://docs.u-boot.org/en/latest/board/index.html
  - https://docs.u-boot.org/en/latest/develop/devicetree/control.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Porting U-Boot to a new board

Almost every custom board derives from a SoC vendor's evaluation board. Port by cloning the
closest supported board and changing only what differs.

## Files to create (example: i.MX8MP based "acme")
```
board/acme/imx8mp-acme/        Kconfig, Makefile, MAINTAINERS, imx8mp-acme.c (board init), spl.c, lpddr4_timing.c
configs/imx8mp_acme_defconfig
arch/arm/dts/imx8mp-acme.dts (+ -u-boot.dtsi for U-Boot-only properties)
include/configs/imx8mp_acme.h  (minimal; most config is Kconfig now)
arch/arm/mach-imx/imx8m/Kconfig: add TARGET_IMX8MP_ACME, source the board Kconfig
```
Newer U-Boot versions can use the upstream Linux DTS directly (`OF_UPSTREAM`,
`dts/upstream/src/arm64/...`) with only a `-u-boot.dtsi` overlay in U-Boot.

## Bring-up order
1. **Console UART** in SPL: correct UART instance and pinmux in the DT and
   `CONFIG_DEBUG_UART`/`CONFIG_SPL_SERIAL`. No output = nothing else to debug.
2. **DRAM**: generate timing with the vendor tool (NXP DDR Tool / config spreadsheet, ST
   STM32CubeMX DDR, Rockchip loader blobs) for your exact memory part and layout; run the vendor
   stress test. Most new-board failures are DRAM.
3. **Boot media**: eMMC/SD/QSPI pinmux and voltage (1.8 V vs 3.3 V signalling), boot offset the ROM
   expects.
4. **PMIC/regulators**: SPL often must configure the PMIC (voltages for DRAM/SoC) via I2C before DRAM init.
5. **Ethernet PHY**: PHY address, reset GPIO, RGMII delays (`phy-mode = "rgmii-id"`).
6. **Environment location** (`CONFIG_ENV_IS_IN_MMC`, offset) and `bootcmd`.
7. Board ID/revision detection, MAC address from fuses/EEPROM.

## Board file essentials
```c
int board_init(void) { /* GPIO resets, power enables */ return 0; }
int board_late_init(void) { env_set("board_rev", acme_rev_str()); return 0; }
```
Prefer driver model + DT over board code; most peripherals need no C code.

## Build
```sh
make imx8mp_acme_defconfig && make -j$(nproc) CROSS_COMPILE=aarch64-linux-gnu-
make savedefconfig && cp defconfig configs/imx8mp_acme_defconfig   # after menuconfig changes
```
i.MX additionally needs `flash.bin` assembled with TF-A and DDR firmware (`binman` does it).

## Upstreaming
Add MAINTAINERS entries, documentation in `doc/board/`, run `./tools/buildman` and
`scripts/checkpatch.pl`; upstream boards get refactored with the tree instead of rotting.

## Verify
- [ ] SPL banner, DRAM size correct, vendor DDR stress test passes over temperature.
- [ ] U-Boot proper boots Linux from each intended boot medium.
