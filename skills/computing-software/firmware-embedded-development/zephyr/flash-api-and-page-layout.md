---
id: computing-software.firmware-embedded-development.zephyr.flash-api-and-page-layout
name: flash-api-and-page-layout
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-flash-api, flash-erase, flash-write-block-size, flash-page-layout, flash-get-parameters, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Read, erase and write flash in Zephyr with the flash driver API: write-block alignment, erase page layout queries, erase value, explicit-erase vs RRAM devices, and safety rules."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/flash.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/storage/flash_map.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flash API and page layout

Most apps should use a higher layer (NVS/ZMS, settings, LittleFS, flash_map). Use the raw API for
bootloaders, custom logs, firmware staging, or when writing such a layer.

```c
#include <zephyr/drivers/flash.h>
#include <zephyr/storage/flash_map.h>

#define PART  storage_partition
const struct flash_area *fa;
flash_area_open(PARTITION_ID(PART), &fa);               /* flash_area calls take partition-relative offsets */
const struct device *flash = fa->fa_dev;                /* or DEVICE_DT_GET(DT_CHOSEN(zephyr_flash_controller)) */
```

## Geometry queries
```c
size_t wbs = flash_get_write_block_size(flash);         /* minimum write unit; offset and length must be multiples */
const struct flash_parameters *fp = flash_get_parameters(flash);
uint8_t erased = fp->erase_value;                        /* usually 0xff */

struct flash_pages_info pi;                             /* CONFIG_FLASH_PAGE_LAYOUT=y */
flash_get_page_info_by_offs(flash, fa->fa_off, &pi);    /* pi.start_offset, pi.size, pi.index */
size_t pages = flash_get_page_count(flash);
```
Pages can differ in size on one device. Always query.

## Erase and write
```c
flash_area_erase(fa, 0, pi.size);                        /* offsets relative to partition */
uint8_t rec[16] = { ... };                               /* length and offset multiples of wbs */
flash_area_write(fa, off, rec, sizeof rec);
flash_area_read(fa, off, buf, len);
```
Raw device calls (`flash_erase`, `flash_write`, `flash_read`) take absolute offsets.

## Rules
- Writes: offset and length must be multiples of the minimum write block size. The source buffer may be in RAM
  or SoC flash, with no alignment restriction on its address.
- Treat a location as writable once after erase unless the part's datasheet says otherwise.
- Erase offsets and sizes follow the hardware's page layout; erase only whole pages within your partition.
- Erasing or writing internal flash can stall the CPU on parts that execute from the same flash; check the SoC
  documentation for how your platform schedules flash operations.
- Devices without an explicit erase (for example non-volatile RAM types): `flash_params_get_erase_cap()` returns the
  `FLASH_ERASE_C_*` capabilities (0 when none, possibly because the driver disabled them). Call `flash_erase()` only
  on real explicit-erase devices; when you just need a region set to the erase value on any technology, call
  `flash_flatten()`.
- Write and erase protection is managed inside the driver's write and erase implementation.

## Verify
- [ ] Code queries write-block size and page layout instead of hardcoding.
- [ ] Partition boundaries align to erase pages (check DT `fixed-partitions` vs page info).
- [ ] Power-cut test during write does not corrupt data outside the target page.

## Checked

Checked 2026-10-26 against `include/zephyr/drivers/flash.h` and `include/zephyr/storage/flash_map.h` on Zephyr main:
`flash_get_write_block_size()`, `flash_get_parameters()` and `erase_value`, `struct flash_pages_info` fields,
`flash_get_page_info_by_offs()`, `flash_get_page_count()`, `CONFIG_FLASH_PAGE_LAYOUT`, `flash_write()` alignment and buffer
rules, `flash_erase()` vs `flash_flatten()` guidance, `flash_params_get_erase_cap()`, and the `flash_area_*` calls and
`struct flash_area` fields. Fixed: `FIXED_PARTITION_ID` is deprecated in favour of `PARTITION_ID`; the claim that some drivers
need the write buffer in RAM contradicts the current `flash_write()` documentation. Removed device-specific figures (STM32/nRF),
ECC remarks, the nRF radio-sync option and the SPI NOR unlock note, which no Zephyr document in this check confirms.

Method: documentation only; no commands were run.
