---
id: computing-software.firmware-embedded-development.bootloader-development.multi-stage-boot-chains
name: multi-stage-boot-chains
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [multi-stage-boot, bootloader-architecture, rom-bootloader, spl, bl1-bl2, firmware-embedded-development]
level: advanced
status: draft
description: "Design and debug multi-stage boot chains (ROM, first stage, second stage, app or OS) on MCUs and SoCs: what each stage owns, handoff data, where boots fail."
sources:
  - https://docs.u-boot.org/en/latest/usage/spl_boot.html
  - https://trustedfirmware-a.readthedocs.io/en/latest/design/firmware-design.html
  - https://trustedfirmware-m.readthedocs.io/en/latest/design_docs/booting/bl1.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-stage boot chains

## Typical chains
| System | Chain |
|---|---|
| Simple MCU | ROM (optional system bootloader) -> custom bootloader -> app |
| MCU with MCUboot | ROM -> MCUboot -> app (or TF-M secure image -> NS app) |
| TF-M (Armv8-M) | ROM -> BL1 (immutable, in ROM/OTP) -> BL2 (MCUboot) -> TF-M SPE -> NSPE app |
| ESP32 | ROM -> 2nd-stage bootloader (flash 0x0/0x1000) -> app selected from partition table |
| Arm Cortex-A SoC (i.MX, STM32MP, Rockchip) | ROM -> SPL/TF-A BL2 (DRAM init) -> TF-A BL31 (secure monitor) + OP-TEE BL32 -> U-Boot BL33 -> Linux |

## Why stages exist
- **ROM** is fixed: it can only load a small image into on-chip SRAM from a fixed location.
- **First stage** (SPL, BL2, TF-A BL2): initialise clocks and DRAM, then load the larger next
  stage into DRAM. Must fit the SRAM limit (often 64-256 KB).
- **Security**: immutable early stages anchor the chain of trust; later updatable stages are
  verified by earlier ones.
- **Separation of duties**: secure monitor/TEE stays resident; the general-purpose loader (U-Boot)
  exits.

## Handoff data
Each stage passes information forward: boot device and slot, reset reason, measured boot hashes,
DRAM size, device tree address (r0-r2 on ARM32, x0 on ARM64 for the DT pointer to Linux), image
version. Use a defined structure at a fixed address, registers, or a standard format (TF-A uses
`bl_params`, Firmware Handoff spec `transfer_list`; MCUboot shared data TLVs to TF-M).

## Where boots fail and how to see it
- ROM stage: nothing on the console. Check boot-mode pins/fuses, the image header format the ROM
  expects (i.MX IVT/container, STM32 header v2, Rockchip idbloader), and the offset on the media.
  Many ROMs fall back to USB serial download mode: `uuu` (NXP), `STM32CubeProgrammer` (USB DFU),
  `rkdeveloptool`.
- First stage: early UART output (enable debug UART in SPL: `CONFIG_SPL_SERIAL`); DRAM training
  failures show as hangs right after "DDR" messages.
- Signature failures: each secure stage logs a reason code if a console is enabled; in production
  builds, map error codes to LED patterns or retained registers.

## Design rules
- Keep early stages minimal and well tested; they are hardest to update.
- Version the handoff structures.
- Measure boot time per stage (GPIO toggles or timestamps passed forward).

## Verify
- [ ] Each stage prints (in dev builds) its version and the next image it selects.
- [ ] Corrupting each later stage in turn produces a defined fallback, not a silent hang.
