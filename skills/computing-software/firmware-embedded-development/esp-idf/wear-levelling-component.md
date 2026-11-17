---
id: computing-software.firmware-embedded-development.esp-idf.wear-levelling-component
name: wear-levelling-component
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-storage, esp-wear-levelling, wl-mount, flash-endurance, fatfs-wl, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use the ESP-IDF wear levelling layer under FAT or raw sector storage: how it maps sectors, its RAM/flash overhead, endurance sizing and power-loss behaviour."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/wear-levelling.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/fatfs.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/wear_levelling/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wear levelling component

SPI flash sectors have a limited number of erase/modification cycles, and FAT rewrites its FAT and directory sectors on
every file update. The `wear_levelling` component distributes wear across sectors without user attention.

## Usage
Normally indirect, through `esp_vfs_fat_spiflash_mount_rw_wl()`. Direct use for custom
sector-based storage:
```c
#include "wear_levelling.h"
const esp_partition_t *p = esp_partition_find_first(ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_DATA_FAT, "storage");
wl_handle_t wl;
ESP_ERROR_CHECK(wl_mount(p, &wl));
size_t sec = wl_sector_size(wl);         /* 4096 or 512 per CONFIG_WL_SECTOR_SIZE; wl_size() gives the usable size */
wl_erase_range(wl, 0, sec);
wl_write(wl, 0, buf, sec);
wl_read(wl, 0, buf, sec);
wl_unmount(wl);
```

## Overhead and sizing
- The module uses some flash sectors for internal data. Per the FAT docs, the minimum layout with 4096-byte sectors is 32 KB:
  4 flash sectors reserved by wear levelling plus the 4-logical-sector minimum FAT; with 512-byte sectors the minimum is 20 KB
  in Performance mode and 28 KB in Safety mode (2 more reserved flash sectors).
- `CONFIG_WL_SECTOR_SIZE` is 4096 (default in Kconfig; most efficient, needs 4096 bytes of RAM per mounted FAT volume and per
  open file) or 512 (more flash operations, 512 bytes of RAM per volume and per open file).
- `CONFIG_WL_SECTOR_MODE` applies to 512-byte sectors: Performance mode keeps the erased sector's data in RAM, so power loss
  during the erase loses the whole 4096-byte flash sector; Safety mode (Kconfig default) saves it to flash first so it can be
  recovered. The component README text lists 512 bytes and Performance mode as defaults, which differs from the v6.1 Kconfig;
  check your menuconfig.
- The wear levelling layer does not cache data in RAM; writes and erases modify flash directly.

For an endurance estimate, take the erase-cycle rating from your flash datasheet and divide by the erases per day measured
from your write pattern (log a counter in testing). Bigger partitions spread wear over more sectors.

## Power loss
FAT on top can still lose the last write or leave lost clusters after power loss; in 512-byte Performance mode a power cut
during a sector erase loses that flash sector's data. Keep critical small values in NVS.

## Pitfalls
- Avoid the raw wear levelling functions when a filesystem helper exists (the README advises filesystem-specific functions);
  writing the partition directly with `esp_partition_write` bypasses the remapping.
- The sector size is compiled into the layout: after changing `CONFIG_WL_SECTOR_SIZE`, reformat or regenerate the image.
- Build-time FAT images for WL partitions must be generated with
  `fatfs_create_spiflash_image` (adds the WL layer), not a plain FAT image.

## Verify
- [ ] Usable FAT size checked against requirement after WL overhead.
- [ ] Power-cut test during writes over many cycles: mount succeeds every time.
- [ ] Lifetime estimate documented from measured erase rate.

## Checked

Checked against ESP-IDF v6.1 (components/wear_levelling README, Kconfig and wear_levelling.h; docs/en/api-reference/storage/fatfs.rst minimum-size table).
Confirmed: API (`wl_mount`, `wl_unmount`, `wl_erase_range`, `wl_write`, `wl_read`, `wl_size`, `wl_sector_size`), 4096 default in Kconfig with the RAM cost per volume and file, Performance versus Safety mode semantics and that mode only applies to 512-byte sectors, no RAM caching, minimum sizes (32 KB, 20 KB, 28 KB), `esp_vfs_fat_spiflash_mount_rw_wl` as the normal entry point, `fatfs_create_spiflash_image`. Removed unconfirmed claims: the 100k erase cycle figure, the 1 MB minus 20 KB example, redundant state surviving power loss, the corruption claim for mixing raw writes (kept only as advice to avoid bypassing the layer) and the 500 cycle test count.

Method: documentation only; no commands were run.
