---
id: computing-software.firmware-embedded-development.device-driver-development.qspi-nor-flash-driver
name: qspi-nor-flash-driver
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [qspi-flash, spi-nor, sfdp, quad-spi, octospi, write-enable, page-program, sector-erase, memory-mapped-mode, firmware-embedded-development]
level: advanced
status: draft
description: "Write an SPI/QSPI NOR flash driver: JEDEC ID and SFDP, write-enable/status polling, page program boundaries, erase sizes, quad enable, memory-mapped XIP, and power/reset handling."
sources:
  - https://www.jedec.org/standards-documents/docs/jesd216
  - https://docs.kernel.org/driver-api/mtd/spi-nor.html
  - https://www.st.com/resource/en/application_note/an4760-quadspi-interface-on-stm32-microcontrollers-and-microprocessors-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SPI/QSPI NOR flash driver

**Goal:** reliable read/program/erase of serial NOR flash (W25Q, MX25, IS25, GD25...) over
SPI or QSPI, including execute-in-place where the controller supports it.

## Command basics (common across vendors)
| Op | Cmd | Notes |
|---|---|---|
| Read JEDEC ID | 0x9F | manufacturer + type + capacity; check at init |
| Read SFDP | 0x5A | JESD216 parameter table: erase sizes, quad enable method, 4-byte addressing |
| Write enable | 0x06 | required before every program/erase/status write; auto-clears after |
| Read status 1 | 0x05 | bit0 WIP/BUSY, bit1 WEL |
| Page program | 0x02 / 0x32 (quad) | max 256 bytes, **must not cross a page boundary** - wraps within the page |
| Sector erase 4K | 0x20 | 4 KB, ~45-400 ms |
| Block erase | 0x52 (32K) / 0xD8 (64K) | |
| Fast read | 0x0B / quad 0xEB | dummy cycles per datasheet/SFDP |
| Reset | 0x66 then 0x99 | recover from unknown mode at boot |

## Program sequence
```c
for each chunk not crossing a 256-byte page:
    cmd(WREN);
    cmd_addr_data(PP, addr, data, n);
    while (status() & WIP) { yield(); }      /* poll; or use autopolling (QSPI APMS) */
```
Erase before program: NOR programs 1->0 only; an erased byte is 0xFF. Verify after write by
reading back (or CRC) for critical data.

## Quad and addressing
- Quad mode needs the **QE bit** set; its location differs (SR2 bit1 on Winbond via 0x31,
  SR bit6 on Macronix). SFDP's Basic Flash Parameter Table says which method.
- Devices >16 MB need 4-byte addressing: 4-byte opcodes (0x13/0x12/0x21) or enter 4-byte mode
  (0xB7) - and a bootloader/ROM that expects 3-byte mode after reset will fail if you leave
  it in 4-byte mode. Prefer 4-byte opcodes.

## Memory-mapped / XIP
QSPI/OSPI controllers (STM32 QUADSPI/OCTOSPI, NXP FlexSPI, RP2040 XIP) map flash into the
address space for reads. While mapped, indirect commands (erase/program) are not allowed: exit
memory-mapped mode, run the command from RAM code, re-enter. Invalidate caches over the region
after writes.

## Robustness
- At boot, issue reset (0x66/0x99) in case the MCU reset mid-command; wait tRST.
- Deep power-down (0xB9) saves µA; release (0xAB) and wait tRES1 before access.
- Protect bootloader areas with block protection bits (BP0-BP3/TB/SEC) and status register lock.
- Power loss during erase/program leaves partial data: use a filesystem or journalling
  (littlefs, wear-levelled KV store) on top.
- Timeouts per op from the datasheet max values (chip erase can exceed 100 s).

## Verify
- [ ] JEDEC ID matches the part; SFDP signature "SFDP" read correctly.
- [ ] Write across a page boundary test: data intact at both pages.
- [ ] Power-cycle during erase: driver recovers and reports the sector as needing erase.
