---
id: computing-software.firmware-embedded-development.esp-idf.iram-attr-and-cache-disabled-code
name: iram-attr-and-cache-disabled-code
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-dual-core, iram-attr, dram-attr, cache-disabled, linker-fragments, flash-operations, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write ESP32 code that runs while the flash cache is disabled: IRAM_ATTR/DRAM_ATTR placement, linker fragment files, IRAM-safe driver options, and diagnosing cache-access panics."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/intr_alloc.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/memory-types.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/performance/ram-usage.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_gptimer/Kconfig
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_uart/Kconfig
  - https://github.com/espressif/esp-idf/blob/master/components/spi_flash/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IRAM_ATTR and cache-disabled code

Code and constants normally execute/read from external flash through a cache. During a flash
**write or erase** (NVS commit, OTA, file system write) the cache is disabled on both cores.
Anything that runs then (an IRAM-flagged ISR, or the other core if not stalled) must not touch
flash-mapped memory.

## Placement attributes
```c
void IRAM_ATTR fast_isr(void *arg) { ... }          /* code in internal IRAM */
DRAM_ATTR static const uint16_t lut[256] = { ... }; /* const data in DRAM, not flash .rodata */
static const char *msg = DRAM_STR("overflow");      /* string literal in DRAM */
```
Everything the IRAM function calls must also be in IRAM: your helpers (`IRAM_ATTR`), and IDF
functions only if documented IRAM-safe. Inline `static inline` helpers are usually fine.

## Driver options for IRAM-safe ISRs
Many drivers have Kconfig switches that move their ISR and control functions to IRAM, e.g.
`CONFIG_GPTIMER_ISR_CACHE_SAFE`, `CONFIG_GPIO_CTRL_FUNC_IN_IRAM`, `CONFIG_RMT_ISR_IRAM_SAFE`,
`CONFIG_SPI_MASTER_ISR_IN_IRAM`, `CONFIG_UART_ISR_IN_IRAM`. Enable them when the peripheral
must keep working during flash writes (motor control, audio, high-rate UART).

## Whole components into IRAM: linker fragments
`components/dsp/linker.lf`:
```
[mapping:dsp]
archive: libdsp.a
entries:
    filter_fast (noflash)        # one object file into IRAM
    * (default)
```
Register with `idf_component_register(... LDFRAGMENTS "linker.lf")`. `noflash` places code in
IRAM and rodata in DRAM.

## The failure modes
- ESP32: `Guru Meditation Error: Core 0 panic'ed (Cache disabled but cached memory region accessed)`.
- Newer chips: `Cache error` / `MMU entry fault` / illegal instruction at a flash address.
The backtrace points at the function that touched flash; it's either missing `IRAM_ATTR`, reads
a const table without `DRAM_ATTR`, or calls a non-IRAM IDF function.

## Budget
IRAM is limited. Check with:
```bash
idf.py size            # IRAM used/remaining
idf.py size-components # who uses it
```
"`iram0_0_seg` overflowed" at link means too much; move non-critical code back to flash,
or disable unused IRAM-placement Kconfig options (for example `CONFIG_RINGBUF_IN_IRAM`,
`CONFIG_ESP_WIFI_IRAM_OPT`, `CONFIG_ESP_WIFI_RX_IRAM_OPT`; see the RAM-usage guide).

## Alternatives
- Chips and flash parts that support it can use `CONFIG_SPI_FLASH_AUTO_SUSPEND`, which lets
  cached code run during flash operations (see the flash concurrency page).
- Defer: a non-IRAM ISR is simply delayed until the flash operation ends. If that latency
  is acceptable, you don't need IRAM.

## Verify
- [ ] Stress test: run the ISR at max rate while doing continuous NVS writes and an OTA download.
- [ ] `idf.py size` shows IRAM headroom recorded in release notes.
- [ ] Every function reachable from IRAM ISRs reviewed for IRAM placement.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed: IRAM-safe handler rules and ESP_INTR_FLAG_IRAM (interrupt allocation guide), DRAM_ATTR/DRAM_STR/IRAM_ATTR attributes (esp_attr.h), Kconfig GPIO_CTRL_FUNC_IN_IRAM, RMT_ISR_IRAM_SAFE, SPI_MASTER_ISR_IN_IRAM, UART_ISR_IN_IRAM, SPI_FLASH_AUTO_SUSPEND, RINGBUF_IN_IRAM and Wi-Fi IRAM options. Wrong: CONFIG_GPTIMER_ISR_IRAM_SAFE does not exist (current option is CONFIG_GPTIMER_ISR_CACHE_SAFE) and CONFIG_FREERTOS_PLACE_FUNCTIONS_INTO_FLASH / RINGBUF_PLACE_FUNCTIONS_INTO_FLASH were not found in Kconfig. Removed ESP_DRAM_LOGE advice, chip examples and IRAM size figure (not confirmed).
Method: documentation only; no commands were run.
