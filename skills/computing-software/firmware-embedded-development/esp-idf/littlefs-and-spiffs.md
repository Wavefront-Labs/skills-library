---
id: computing-software.firmware-embedded-development.esp-idf.littlefs-and-spiffs
name: littlefs-and-spiffs
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-littlefs, spiffs, esp-vfs-littlefs-register, joltwallet-littlefs, partition-image, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Store files on ESP32 internal flash with LittleFS (registry component) or legacy SPIFFS: partition setup, mounting via VFS, build-time images and migration from SPIFFS."
sources:
  - https://github.com/joltwallet/esp_littlefs
  - https://components.espressif.com/components/joltwallet/littlefs
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/spiffs.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/partition-tables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LittleFS and SPIFFS

| | LittleFS | SPIFFS |
|---|---|---|
| Where | registry component `joltwallet/littlefs` | built into ESP-IDF |
| Directories | yes | no (flat, `/` is part of the name) |
| Power-loss safety | described by its authors as a fail-safe filesystem | power loss can corrupt it; `esp_spiffs_check` may recover it |
| Performance when full | measured in the component's README to degrade less | garbage collection can take up to several seconds per write |
| Usable space | no documented cap | reliably uses only about 75% of the partition (ESP-IDF docs) |

## LittleFS
```bash
idf.py add-dependency "joltwallet/littlefs^1.23"      # component manifest requires IDF >=5.0
```
`partitions.csv` (data subtype `littlefs` is 0x83; if no label is given the component mounts the first `littlefs` partition):
```
storage,  data, littlefs,  ,  1M
```
```c
#include "esp_littlefs.h"
esp_vfs_littlefs_conf_t conf = {
    .base_path = "/littlefs",
    .partition_label = "storage",
    .format_if_mount_failed = true,
    .dont_mount = false,
};                                       /* no max_files field: LittleFS has no open-file limit */
ESP_ERROR_CHECK(esp_vfs_littlefs_register(&conf));
size_t total, used;
esp_littlefs_info(conf.partition_label, &total, &used);

FILE *f = fopen("/littlefs/cfg/wifi.json", "r");   /* POSIX via VFS; mkdir() works */
```
Unmount with `esp_vfs_littlefs_unregister("storage")`.

Build-time image from a folder:
```cmake
littlefs_create_partition_image(storage ../flash_data FLASH_IN_PROJECT)
```

## SPIFFS (existing products)
```c
esp_vfs_spiffs_conf_t sc = { .base_path = "/spiffs", .partition_label = NULL,
                             .max_files = 5, .format_if_mount_failed = true };
ESP_ERROR_CHECK(esp_vfs_spiffs_register(&sc));
esp_spiffs_check(NULL);                 /* after unclean shutdown: consistency repair */
```
```cmake
spiffs_create_partition_image(storage ../spiffs_data FLASH_IN_PROJECT)
```
Keep SPIFFS well below ~75% full (its reliable limit); `CONFIG_SPIFFS_OBJ_NAME_LEN` (default 32) includes the
zero terminator, so names can be at most 31 characters, and SPIFFS has no directories (a path is just part of the name).

## Migrating SPIFFS to LittleFS in the field
The on-flash formats are incompatible. In the OTA that switches: mount SPIFFS, read the
files you need into RAM (or NVS), format the partition as LittleFS, write them back, set an
NVS flag so it runs once. Test power loss in the middle of the migration and make it
restartable.

## Gotchas
- `format_if_mount_failed = true` wipes data after any mount error, including ones caused by a
  wrong partition label. For user data, mount with false first and decide.
- Both are intended for SPI flash partitions; for SD cards the usual choice is FAT (the LittleFS component also has optional SD/MMC support behind a Kconfig option).
- Flash encryption: the LittleFS component's README documents testing on an `encrypted` partition, but a block-device mount rejects the `encrypted` flag; the ESP-IDF partition docs name SPIFFS as a filesystem that does not support encryption (the `ALWAYS_PLAINTEXT` option of the partition image helpers exists for such cases and must not be combined with an `encrypted` partition).

## Verify
- [ ] Mount, write, power cycle, read back works on a fresh and on a full partition.
- [ ] Free space monitored (`esp_littlefs_info`); SPIFFS kept well below 75% full.
- [ ] Image generation in CMake matches the partition label and size.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-reference/storage/spiffs.rst, partition-tables.rst, components/spiffs Kconfig and esp_spiffs.h) and the joltwallet/esp_littlefs repository (v1.23.1, last commit 2026-10-21; README and include/esp_littlefs.h).
Confirmed: SPIFFS has no directories, reliably uses about 75% of the partition, GC can take seconds, `esp_spiffs_check` recovery, `esp_vfs_spiffs_conf_t` fields (base_path, partition_label, max_files, format_if_mount_failed), `CONFIG_SPIFFS_OBJ_NAME_LEN` default 32 including terminator, `spiffs_create_partition_image`; partition subtype `littlefs` (0x83) in the partition table docs; LittleFS `esp_vfs_littlefs_conf_t` (no `max_files`, `dont_mount`, `format_if_mount_failed`), `esp_vfs_littlefs_register`/`unregister`, `esp_littlefs_info`, `littlefs_create_partition_image(<partition> <folder> FLASH_IN_PROJECT)`, SPIFFS being named as not supporting encryption in docs/en/api-reference/storage/partition.rst, component version 1.23.1 needing IDF >=5.0. Removed unconfirmed claims: SPIFFS being legacy or maintenance-only, the 70 and 80 percent figures and the statement that LittleFS cannot be used on SD cards.

Method: documentation only; no commands were run.
