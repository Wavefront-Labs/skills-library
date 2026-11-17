---
id: computing-software.firmware-embedded-development.bootloader-development.u-boot-spl-bringup
name: u-boot-spl-bringup
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [u-boot, u-boot-spl, secondary-program-loader, ddr-init, sram-limits, falcon-mode, tpl, boot-rom, firmware-embedded-development]
level: sme
status: docs-checked
description: "Understand and bring up U-Boot SPL: what runs in on-chip SRAM, DDR initialisation, loading U-Boot proper or ATF, size limits and Falcon mode direct kernel boot."
sources:
  - https://docs.u-boot.org/en/latest/usage/spl_boot.html
  - https://docs.u-boot.org/en/latest/develop/spl.html
  - https://docs.u-boot.org/en/latest/develop/falcon.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# U-Boot SPL bring-up

**Goal:** get from the SoC boot ROM to DRAM-resident U-Boot (or straight to Linux) on a new
board, knowing which stage does what.

## Boot chain (typical ARM SoC)
1. **Boot ROM** (mask ROM) loads a small image from eMMC/SD/SPI/USB into on-chip SRAM.
2. **SPL** (U-Boot's Secondary Program Loader, built from the same tree with `CONFIG_SPL`)
   runs in SRAM: sets clocks, PMIC, pinmux for the boot device and console, **initialises
   DDR**, then loads the next stage into DRAM.
3. On arm64: SPL loads **TF-A (BL31)** and U-Boot proper, then launches BL31, which invokes
   U-Boot as BL33.
4. **U-Boot proper** loads kernel + DTB.
Some SoCs add a **TPL** before SPL when SRAM is tiny.

## Bring-up order
- Serial console first (`CONFIG_SPL_SERIAL`, early UART pinmux in board `spl.c`), then DDR.
- DDR timing: use the SoC vendor's DDR configuration tool output for the exact memory part and
  PCB. Run a DDR stress test before anything else: marginal DDR causes random kernel crashes
  weeks later.
- Many SoCs need vendor **firmware blobs** for DDR PHY training; they are packaged alongside SPL
  by the board's build.

## Size and constraints
- SPL must fit SRAM including stack, BSS and malloc pool: check the generated `u-boot-spl.map`
  and drop unused drivers with `CONFIG_SPL_*` options.
- Driver model in SPL uses only DT nodes marked `bootph-all` or `bootph-pre-ram` (TPL:
  `bootph-pre-sram`). Missing tags = "device not found" in SPL only.

## Falcon mode
SPL loads the kernel and DTB directly, skipping U-Boot proper, for fast boot.
Prepare args once with `spl export fdt [kernel_addr] [initrd_addr] [fdt_addr]` from U-Boot, store
them, and set `CONFIG_SPL_OS_BOOT`. Keep a way back to full U-Boot (key pressed, GPIO, env var) for
maintenance.

## Verify
- [ ] SPL banner and DRAM size print on console.
- [ ] Vendor DDR stress test passes across temperature range.
- [ ] `u-boot-spl.bin` size well under SRAM limit (map file reviewed).

## Checked
2026-10-31. Confirmed against the U-Boot SPL, Booting from TPL/SPL and Falcon mode pages: TPL/SPL phases, BL31 launching U-Boot as BL33, u-boot-spl.bin/.map outputs, bootph-all/pre-ram/pre-sram, CONFIG_SPL_SERIAL, CONFIG_SPL_OS_BOOT, `spl export fdt` arguments. Removed the SRAM size range, the ~1 s saving, EL2, `u-boot.itb`, vendor DDR file names, `mtest`, binman, SPL_SYS_MALLOC_SIMPLE, OF_PLATDATA and the old `u-boot,dm-*` property names, none of which the fetched pages state.
Method: documentation only; no commands were run.
