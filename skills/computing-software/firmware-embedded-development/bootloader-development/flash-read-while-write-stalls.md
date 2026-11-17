---
id: computing-software.firmware-embedded-development.bootloader-development.flash-read-while-write-stalls
name: flash-read-while-write-stalls
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [flash-stall, read-while-write, dual-bank-flash, flash-erase-latency, bus-stall, ramfunc, partial-erase, iram, firmware-embedded-development]
level: advanced
status: draft
description: "Handle CPU and bus stalls during internal flash erase/program: which parts support read-while-write, running from RAM or the other bank, partial erases, watchdog and interrupt latency."
sources:
  - https://www.st.com/resource/en/reference_manual/dm00031020.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/nvmc.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/spi_flash/spi_flash_concurrency.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Read-while-write and bus stalls

**Goal:** writing internal flash (bootloader updates, data logging, settings) without missing
interrupts, tripping the watchdog or faulting.

## What actually happens
Most single-bank MCUs cannot read a flash bank while it is being erased or programmed. Any
instruction fetch or data read from that bank **stalls the bus** until the operation ends:
- STM32F4 128 KB sector erase: typ. ~1-2 s, max several seconds - the CPU executing from flash
  freezes for the whole time, including interrupt handlers and vector fetches.
- nRF52 NVMC page erase ~85 ms: CPU halted while executing from flash.
- ESP32 (external SPI flash): the flash cache is disabled during writes; code or data not in
  IRAM/DRAM faults ("Cache disabled but cached memory region accessed").

## Options
1. **Dual-bank / read-while-write parts** (STM32F42x/F43x with DB1M, L4 DUALBANK, G4, H7, many
   NXP/Microchip parts): run code from bank 1 while erasing bank 2. Design the partition map so
   writes go to the other bank. This is the clean solution - choose parts with it when field
   updates matter.
2. **Execute the write routine and everything that can interrupt it from RAM**: copy the vector
   table to RAM (`SCB->VTOR`), mark the flash routine and critical ISRs `ramfunc` (see
   `running-code-from-ram-ramfunc`). Everything else must be masked.
3. **Split the work**: erase the smallest units the part allows (pages instead of sectors), or
   use partial erase (nRF52 `ERASEPAGEPARTIAL` with `ERASEPAGEPARTIALCFG` in ms) to interleave
   flash work with time-critical activity.
4. **Schedule** erases when stalls are harmless: radio idle (nRF SoftDevice `sd_flash_*` and
   Zephyr's flash driver with `CONFIG_SOC_FLASH_NRF_RADIO_SYNC_*`), between control periods,
   or during a maintenance window.
5. **ESP-IDF**: mark ISRs `IRAM_ATTR` and register them with `ESP_INTR_FLAG_IRAM` so they keep
   running; others are deferred until the write ends.

## Watchdog and timing budget
- The independent watchdog keeps counting during the stall: its timeout must exceed the
  datasheet **max** erase time, or erase in smaller chunks and kick in between.
- Communication peripherals overrun during stalls: use DMA into RAM and hardware flow control,
  or protocol-level ACKs so the host waits for erase completion.
- Measure with a GPIO toggled by a timer ISR: gaps show actual stall length.

## Gotchas
- Reading constants from flash (lookup tables, string literals) inside the RAM routine stalls
  too; copy them first.
- Some parts raise a bus fault instead of stalling when reading a busy bank; check the RM.
- Option byte programming and mass erase have far longer times.

## Verify
- [ ] Timer-ISR GPIO shows no gaps (dual bank/RAM ISR) or gaps within budget during erase.
- [ ] Watchdog never resets during worst-case erase at low temperature (slowest).
