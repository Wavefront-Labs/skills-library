---
id: computing-software.firmware-embedded-development.bootloader-development.bootloader-flash-partitioning
name: bootloader-flash-partitioning
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [bootloader-architecture, flash-partitioning, memory-map, sector-alignment, image-slot, scratch-area, linker-script, flash-layout, firmware-embedded-development]
level: advanced
status: draft
description: "Lay out MCU flash for a bootloader, application slots, scratch and config storage: sector alignment, asymmetric sectors, growth margin and linker-script consistency."
sources:
  - https://docs.mcuboot.com/design.html
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bootloader flash partitioning

**Goal:** a flash map that survives years of firmware growth, where each region can be
erased independently and every image is linked for the address it runs from.

## Typical map (1 MB part, MCUboot-style A/B)
| Region | Size | Notes |
|---|---|---|
| Bootloader | 32-64 KB | at reset vector, write-protected in production |
| Slot 0 (primary, executes) | ~45 % | application linked here |
| Slot 1 (secondary, download) | same as slot 0 | |
| Scratch (swap-using-scratch only) | >= largest sector | |
| Config / NVS / logs | 2+ sectors | never inside an image slot |

## Rules
1. **Every boundary on an erase-sector boundary.** STM32F4 has 16/16/16/16/64/128... KB
   sectors: a 32 KB bootloader wastes nothing at 0x0800_0000-0x0800_7FFF (2 x 16 KB), but
   the config area wants the small sectors too. On asymmetric-sector parts, plan the small
   sectors first (bootloader + config) and give slots the 128 KB sectors.
2. **Slots the same size and sector geometry** for swap-based updates; MCUboot's swap
   algorithms require compatible sector layouts in both slots.
3. **Leave 25-40 % headroom** in the slot at first release. The image only grows; resizing
   slots in the field means a bootloader change, which is the riskiest update there is.
4. **Bootloader size with margin** for crypto (adding ECDSA verification adds ~10-20 KB).
5. **Keep config outside slots** so an update never erases calibration data.
6. **Dual-bank parts** (STM32G4/L4/H7 with BFB2/SWAP_BANK) can swap banks in hardware: one
   bank per slot, and the app is linked once for the bank-0 address.

## One source of truth
Define the map once (a header or a devicetree `fixed-partitions` node in Zephyr) and generate:
- bootloader constants (`SLOT0_ADDR`, `SLOT_SIZE`),
- application linker `MEMORY { FLASH (rx) : ORIGIN = 0x08010000, LENGTH = 448K }`,
- signing tool arguments (`imgtool sign --header-size 0x200 --slot-size 0x70000`).
Hand-copied numbers drift; a mismatch makes the bootloader reject valid images or jump into
garbage.

## The application side
- Linker origin = slot start + image header size (MCUboot uses a 0x200 header; the vector
  table must follow at the alignment the core needs, 128..512 bytes depending on vector count).
- Set `SCB->VTOR` to the app vector table (most startup code does this from a
  `VECT_TAB_OFFSET` define on STM32; set it).

## Verify
- [ ] Map file of each image fits its region with the stated headroom.
- [ ] A script asserts all region starts are sector-aligned and non-overlapping.
- [ ] Erasing the secondary slot leaves bootloader, primary and config intact (read back CRCs).
