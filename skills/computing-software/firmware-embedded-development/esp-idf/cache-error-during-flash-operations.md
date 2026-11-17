---
id: computing-software.firmware-embedded-development.esp-idf.cache-error-during-flash-operations
name: cache-error-during-flash-operations
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-dual-core, cache-error, cache-disabled-access, flash-write-crash, iram-safe-isr, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Debug ESP32 cache errors and IllegalInstruction crashes that happen during flash writes: what disables the cache, finding the offending ISR or data, and IRAM-safe fixes."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/spi_flash/spi_flash_concurrency.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/fatal-errors.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache errors during flash operations

While the SPI flash is erased or written (NVS commit, OTA, file system writes), the flash cache is
disabled on both cores. Any code or constant fetched from flash in that window faults.

## Signatures
```
Guru Meditation Error: Core 0 panic'ed (Cache disabled but cached memory region accessed)
Guru Meditation Error: Core 1 panic'ed (Cache error)  ... (other chips report "Cache error")
Guru Meditation Error: Core 0 panic'ed (IllegalInstruction)  (sometimes on ESP32)
```
Often intermittent: only when an interrupt fires during an NVS write.

## Usual culprits
1. ISR registered with `ESP_INTR_FLAG_IRAM` (or driver ISR-IRAM-safe Kconfig enabled) whose
   handler or callees live in flash.
2. IRAM function reading a `const` table or string literal (rodata is in flash). Use `DRAM_ATTR`
   on the table and `DRAM_STR("...")` for strings.
3. ESP_LOGx inside an IRAM ISR (format string in flash): use `ESP_DRAM_LOGx` / `ESP_EARLY_LOGx`.
4. Calling a function that is not IRAM-safe (your own helpers, or library code placed in flash).
5. Accessing PSRAM-backed data on ESP32 while cache is off.

## Find it
- Decode the backtrace (`idf.py monitor` does it) and check whether the PC is in a flash-resident function.
- `EXCVADDR` shows the data address accessed; look it up in the map file to find the variable.
- `CONFIG_SPI_FLASH_DANGEROUS_WRITE_*` (aborts, fails, allowed) governs writes to protected regions and is unrelated.

## Fixes
- Mark the handler and every callee `IRAM_ATTR`; data `DRAM_ATTR`.
- Or do not flag the ISR as IRAM: non-IRAM ISRs are simply deferred until the flash operation ends
  (the cost is latency, often fine).
- Driver options: `CONFIG_UART_ISR_IN_IRAM`, `CONFIG_GPTIMER_ISR_CACHE_SAFE` (renamed from `CONFIG_GPTIMER_ISR_IRAM_SAFE`),
  `CONFIG_GPIO_CTRL_FUNC_IN_IRAM` etc. only when latency during flash writes matters.
- Move flash writes out of time-critical windows.

## Prevent
Add a stress test: one task writes NVS in a loop while every interrupt source fires at max rate.
A long run makes intermittent faults likely to show.

## Verify
- [ ] Stress test runs for a long soak period with no panic.
- [ ] `nm` on the ELF confirms IRAM addresses for all IRAM-flagged handlers and callees.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed: caches disabled during SPI1 flash operations, only IRAM-safe interrupts run, ESP_INTR_FLAG_IRAM, IllegalInstruction or garbage data when code or constants are in flash, ESP_DRAM_LOGx for ISR logging, DRAM_ATTR and DRAM_STR, PSRAM access also faults, UART_ISR_IN_IRAM and GPIO_CTRL_FUNC_IN_IRAM, the 'Cache disabled but cached memory region accessed' message (ESP32 source). Wrong: CONFIG_GPTIMER_ISR_IRAM_SAFE is a deprecated name for CONFIG_GPTIMER_ISR_CACHE_SAFE. Removed unconfirmed memcpy, 0x400Dxxxx flash address and per-chip panic wording claims.
Method: documentation only; no commands were run.
