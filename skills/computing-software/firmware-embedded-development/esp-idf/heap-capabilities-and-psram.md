---
id: computing-software.firmware-embedded-development.esp-idf.heap-capabilities-and-psram
name: heap-capabilities-and-psram
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-system, heap-caps, malloc-cap-dma, malloc-cap-spiram, psram, ext-ram-bss-attr, heap-integrity, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Allocate the right kind of memory on ESP32 with heap_caps (internal, DMA-capable, PSRAM, IRAM), configure PSRAM use, and monitor fragmentation and heap corruption."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/mem_alloc.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/external-ram.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/heap_debug.rst
  - https://github.com/espressif/esp-idf/blob/master/components/heap/include/esp_heap_caps.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_psram/Kconfig.spiram.common
  - https://github.com/espressif/esp-idf/blob/master/components/esp_common/include/esp_attr.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap capabilities and PSRAM

ESP32 memory isn't uniform: internal SRAM (fast, some DMA-capable), RTC memory, IRAM that
only allows 32-bit access, and optional external PSRAM (large, slower, cache-backed). `malloc`
picks for you; `heap_caps_malloc` lets you say what the buffer needs.

## Capabilities
```c
#include "esp_heap_caps.h"
uint8_t *dma_buf = heap_caps_malloc(4096, MALLOC_CAP_DMA | MALLOC_CAP_INTERNAL);
uint8_t *frame   = heap_caps_malloc(320 * 240 * 2, MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);
void    *fast    = heap_caps_malloc(1024, MALLOC_CAP_INTERNAL | MALLOC_CAP_8BIT);
uint8_t *aligned = heap_caps_aligned_alloc(64, 4096, MALLOC_CAP_DMA);
heap_caps_free(frame);                       /* free() also works */
```
| Cap | Meaning |
|---|---|
| `MALLOC_CAP_DMA` | accessible by DMA; use with `MALLOC_CAP_INTERNAL` (the external-RAM guide requires this) |
| `MALLOC_CAP_SPIRAM` | external PSRAM |
| `MALLOC_CAP_INTERNAL` | on-chip RAM that does not disappear when the flash/PSRAM cache is off |
| `MALLOC_CAP_8BIT` | allows 8/16-bit data accesses |
| `MALLOC_CAP_32BIT` | allows aligned 32-bit accesses (may return IRAM) |
| `MALLOC_CAP_EXEC` | executable |
Stacks, DMA descriptors, and buffers used while the flash cache is disabled must be internal.

## PSRAM configuration
```
CONFIG_SPIRAM=y
# also choose the PSRAM mode (quad/octal) that matches the module in the SPI RAM menu
CONFIG_SPIRAM_USE_MALLOC=y                   # malloc() may return PSRAM
CONFIG_SPIRAM_MALLOC_ALWAYSINTERNAL=16384    # allocations <= 16 KB stay internal
CONFIG_SPIRAM_MALLOC_RESERVE_INTERNAL=32768  # keep internal RAM for DMA/stacks
CONFIG_SPIRAM_ALLOW_BSS_SEG_EXTERNAL_MEMORY=y
```
```c
EXT_RAM_BSS_ATTR static uint8_t big_table[512 * 1024];   /* static buffer in PSRAM */
```
With `SPIRAM_USE_CAPS_ALLOC` instead, only explicit `MALLOC_CAP_SPIRAM` requests use PSRAM
(more predictable). Wi-Fi/LWIP buffers can go to PSRAM with `CONFIG_SPIRAM_TRY_ALLOCATE_WIFI_LWIP`.

PSRAM caveats: accesses go through the cache and are slower than internal RAM. On ESP32,
`xTaskCreate` always allocates task stacks internally and `xTaskCreateStatic` checks that the
buffer is internal unless a Kconfig option allows otherwise. The external-RAM guide says DMA to or
from external RAM is not supported in ESP-IDF on ESP32 and is limited on S3 (alignment and size
rules); keep DMA buffers internal (`MALLOC_CAP_DMA | MALLOC_CAP_INTERNAL`).

## Monitoring
```c
heap_caps_print_heap_info(MALLOC_CAP_INTERNAL);
size_t free_int  = heap_caps_get_free_size(MALLOC_CAP_INTERNAL);
size_t min_int   = heap_caps_get_minimum_free_size(MALLOC_CAP_INTERNAL);
size_t largest   = heap_caps_get_largest_free_block(MALLOC_CAP_DMA);
```
Large total free but small largest block means fragmentation: DMA allocations of a few KB fail.
Allocate long-lived DMA buffers at boot.

`heap_caps_register_failed_alloc_callback(cb)` invokes your callback on every failed allocation
(the docs example prints the function name, requested size and caps).

## Corruption
```
CONFIG_HEAP_POISONING_LIGHT=y          # or COMPREHENSIVE while hunting a bug
```
`heap_caps_check_integrity_all(true)` sprinkled around a suspect area finds the first corrupt
block. For leaks, see heap-tracing.

## Verify
- [ ] Minimum-ever free internal and DMA heap logged after a full soak test, with margin.
- [ ] No DMA or ISR buffers in PSRAM.
- [ ] Failed-alloc callback installed in all builds.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed in esp_heap_caps.h, Kconfig.spiram.common and the external-RAM guide: MALLOC_CAP_* meanings, heap_caps_aligned_alloc, failed-alloc callback, SPIRAM_USE_MALLOC / USE_CAPS_ALLOC, SPIRAM_MALLOC_ALWAYSINTERNAL (default 16384), SPIRAM_MALLOC_RESERVE_INTERNAL, SPIRAM_ALLOW_BSS_SEG_EXTERNAL_MEMORY and EXT_RAM_BSS_ATTR, SPIRAM_TRY_ALLOCATE_WIFI_LWIP, HEAP_POISONING_LIGHT, heap_caps_check_integrity_all. Wrong: "DMA from PSRAM works on S3" (guide says DMA to external RAM is unsupported in ESP-IDF on ESP32 and limited on S3); PSRAM task-stack advice replaced by the FreeRTOS Kconfig note. Removed the CONFIG_SPIRAM_MODE_OCT line (symbol not found in the shared Kconfig).
Method: documentation only; no commands were run.
