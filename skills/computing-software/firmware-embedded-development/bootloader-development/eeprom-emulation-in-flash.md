---
id: computing-software.firmware-embedded-development.bootloader-development.eeprom-emulation-in-flash
name: eeprom-emulation-in-flash
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [eeprom-emulation, flash-programming, wear-levelling, log-structured-storage, page-transfer, firmware-embedded-development]
level: advanced
status: draft
description: "Store small variables in MCU flash with EEPROM emulation: two-page log-structured records, page transfer, power-loss safe states, endurance maths, libraries."
sources:
  - https://www.st.com/resource/en/application_note/an4894-eeprom-emulation-techniques-and-software-for-stm32-microcontrollers-stmicroelectronics.pdf
  - https://docs.zephyrproject.org/latest/services/storage/nvs/nvs.html
  - https://github.com/littlefs-project/littlefs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EEPROM emulation in flash

MCUs without data EEPROM keep settings and counters in flash. Flash erases whole pages (2-128 KB)
and endures ~10k cycles; naive "erase page, rewrite all" on every change wears it out and loses
data on power cuts.

## Classic two-page scheme (ST AN4894 style)
- Two (or more) pages; one **ACTIVE**, one **ERASED**.
- Each update appends a record `{virtual address (id), value, CRC}` to the next free slot of the
  active page. Reading scans backwards for the latest record with that id (or uses a RAM index).
- When the active page is full: mark the other page **RECEIVING**, copy the latest value of every
  id into it, mark it **ACTIVE**, erase the old page.
- Page state words are written in a sequence that lets boot-time recovery decide what to do after
  a power cut at any step (e.g. both pages valid -> finish transfer; RECEIVING + ACTIVE -> redo copy).

## Endurance maths
`writes_per_variable = (pages x page_size / record_size / number_of_variables) x cycles`.
Example: 2 pages x 2 KB, 8-byte records, 20 variables -> each page holds 256 records; one page
cycle per ~(256 - 20) updates; with 10k cycles per page and 2 pages: ~4.7M updates total, i.e.
~236k per variable if evenly updated. Add pages for higher write rates. Log every-minute counters
in RAM and persist hourly, plus on power-fail interrupt (PVD) if available.

## Platform notes
- **ECC flash** (L4/G4/U5/H7): records must be full double/quad words, written once. Records grow
  to 8/16/32 bytes; status words likewise. ST's newer X-CUBE-EEPROM handles this.
- **Read-while-write**: erasing a page in the same bank stalls execution for ~20-40 ms; schedule
  page transfers when timing allows, or use a second bank.
- **Interrupted page erase** can leave a page partially erased (reads look valid but programming
  fails): verify erased state, re-erase if not all 0xFF.

## Ready-made options
- Zephyr **NVS** / **ZMS** (id-value storage with wear levelling, power-loss safe).
- ESP-IDF NVS, Nordic FDS (nRF5 SDK), ST X-CUBE-EEPROM.
- littlefs for file-like data (directories, larger blobs).
Prefer these over rolling your own unless you have unusual constraints.

## Verify
- [ ] Power-cut test rig: thousands of random power cuts during writes and page transfers, values always readable and either old or new, never corrupt.
- [ ] Endurance calculation documented for the product's write rate and lifetime.
