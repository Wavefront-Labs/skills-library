---
id: computing-software.firmware-embedded-development.zephyr.nvs-and-zms-storage
name: nvs-and-zms-storage
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-storage, zephyr-nvs, zms, nvs-mount, flash-wear, garbage-collection, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Store records directly in flash with Zephyr NVS or ZMS: mounting on a partition, sector sizing, ID design, garbage collection and wear-life calculation."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/storage/nvs/nvs.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/storage/zms/zms.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/kvss/nvs.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/kvss/zms.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/storage/flash_map.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NVS and ZMS storage

Both are log-structured ID/data stores in a flash partition. NVS (non-volatile storage) is the
long-standing one with 16-bit IDs. ZMS (Zephyr Memory Storage, newer) uses 32-bit IDs by default (64-bit with
`CONFIG_ZMS_ID_64BIT`) and also supports memories without an erase operation (RRAM, MRAM). Use the settings subsystem on top
when you want named keys; use them directly for fixed records or high-rate counters.

## Mount NVS
```c
#include <zephyr/kvss/nvs.h>               /* <zephyr/fs/nvs.h> is a deprecated wrapper */
#include <zephyr/storage/flash_map.h>
#include <zephyr/drivers/flash.h>

static struct nvs_fs fs;

int storage_init(void)
{
    struct flash_pages_info info;
    fs.flash_device = PARTITION_DEVICE(storage_partition);
    if (!device_is_ready(fs.flash_device)) return -ENODEV;
    fs.offset = PARTITION_OFFSET(storage_partition);
    int rc = flash_get_page_info_by_offs(fs.flash_device, fs.offset, &info);
    if (rc) return rc;
    fs.sector_size  = info.size;      /* multiple of the erase page size and a power of 2 */
    fs.sector_count = 3;              /* at least 2; one sector is always kept empty for copying */
    return nvs_mount(&fs);
}
```
```c
#define ID_BOOT_COUNT 1
uint32_t boots = 0;
nvs_read(&fs, ID_BOOT_COUNT, &boots, sizeof(boots));   /* bytes read, or a negative errno */
boots++;
nvs_write(&fs, ID_BOOT_COUNT, &boots, sizeof(boots));  /* bytes written; 0 if identical data is already stored */
nvs_delete(&fs, ID_BOOT_COUNT);
```
ZMS is similar: `<zephyr/kvss/zms.h>`, `struct zms_fs`, `zms_mount`, `zms_read`, `zms_write`, `zms_delete`
(`zms_mount_force` wipes and reinitialises the partition if the first mount fails). Its sectors are
`sector_size`/`sector_count` with a minimum of 2 sectors.

## How it wears
Elements are appended to a sector until it is full; then the next sector is prepared (erased), after
checking that id-data pairs still in use in the sectors being recycled are copied. Each element is stored as
8 bytes of metadata (the ATE, written from the end of the sector) plus data. Lifetime estimate from the NVS docs:
```
life_minutes = SECTOR_COUNT * SECTOR_SIZE * PAGE_ERASES / (NS * (DS + 8))
```
where NS is storage requests per minute, DS the data size in bytes and PAGE_ERASES the rated erase cycles of a page
(from the flash datasheet; the guide's example uses about 20,000 for an nRF51822). To lengthen life, increase
`SECTOR_COUNT` or `SECTOR_SIZE`. Many tiny writes waste space because of the 8-byte metadata.

## Design rules
- Allocate IDs in one header; never reuse an ID for a different struct layout. Add a version
  field or a new ID.
- Keep per-record data small; `nvs_sector_max_data_size()` reports the largest record a sector can hold.
- Write on change with debouncing, not periodically.
- Writes and garbage collection involve flash erase and are slow; don't write from latency-critical threads.
- `nvs_calc_free_space()` reports free bytes but is time consuming, especially on SPI flash; use it sparingly.
- Test power loss during writes on your hardware.

## Verify
- [ ] Power-cut test (relay cycling during writes, thousands of cycles): every read returns old or new value, never garbage.
- [ ] Wear-life computed from measured write rate meets product lifetime with margin.
- [ ] Partition defined in devicetree and not overlapping app or MCUboot slots.

## Checked

Checked 2026-10-26 against the Zephyr NVS and ZMS guides and `include/zephyr/kvss/nvs.h`, `zms.h` on main: 16-bit NVS ids,
32-bit ZMS ids (64-bit option), 8-byte metadata per element, sector size (multiple of erase size and power of two), sector count
(at least 2, one kept empty), `nvs_write()` return value (0 when identical data is rewritten), `nvs_read()`, `nvs_delete()`,
`nvs_calc_free_space()` cost, `nvs_sector_max_data_size()`, ZMS mount functions, and the NVS lifetime formula. Fixed: the
skill's lifetime formula was not the documented one; `<zephyr/fs/nvs.h>` is now a deprecated wrapper for `<zephyr/kvss/nvs.h>`;
`FIXED_PARTITION_*` replaced by `PARTITION_*`. Removed the erase-cycle, erase-duration and power-loss-guarantee statements that
the documents do not give.

Method: documentation only; no commands were run.
