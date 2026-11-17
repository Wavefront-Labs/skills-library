---
id: computing-software.firmware-embedded-development.esp-idf.vfs-and-fat-file-system
name: vfs-and-fat-file-system
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-vfs, fatfs, wear-levelling, esp-vfs-fat-spiflash-mount-rw-wl, sdmmc, fatfs-image, esp-idf, firmware-embedded-development, esp-sdmmc]
level: practitioner
status: docs-checked
description: "Use FAT through the ESP-IDF VFS on SPI flash (with wear levelling) or SD cards: mounting, partition entries, POSIX file I/O, build-time images and the common pitfalls."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/fatfs.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/vfs.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/wear-levelling.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/fatfs/vfs/esp_vfs_fat.h
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VFS and FAT file system

The VFS layer maps path prefixes (`/spiflash`, `/sdcard`) to drivers, so ordinary
`fopen`/`fread`/`stat` work. FAT is the choice when a PC must read the medium (SD card) or you
need FAT compatibility; for internal flash logs LittleFS is usually more robust (see
littlefs-and-spiffs).

## Internal flash with wear levelling
`partitions.csv`:
```
# Name,   Type, SubType, Offset, Size
storage,  data, fat,     ,       1M
```
```c
#include "esp_vfs_fat.h"
static wl_handle_t wl;
esp_vfs_fat_mount_config_t cfg = {
    .format_if_mount_failed = true,
    .max_files = 4,
    .allocation_unit_size = 0,                       /* default; sets the cluster size used when formatting */
};
ESP_ERROR_CHECK(esp_vfs_fat_spiflash_mount_rw_wl("/spiflash", "storage", &cfg, &wl));

FILE *f = fopen("/spiflash/log.txt", "a");
fprintf(f, "boot %d\n", boots);
fclose(f);                                   /* or fflush + fsync(fileno(f)) */
```
Raw FAT on NOR flash without wear levelling would erase the FAT sectors to death; always use
the `_rw_wl` variant for writable flash. Read-only images: `esp_vfs_fat_spiflash_mount_ro`.

## SD card
```c
sdmmc_host_t host = SDMMC_HOST_DEFAULT();            /* or SDSPI_HOST_DEFAULT() over SPI */
sdmmc_slot_config_t slot = SDMMC_SLOT_CONFIG_DEFAULT();
slot.width = 4;
sdmmc_card_t *card;
ESP_ERROR_CHECK(esp_vfs_fat_sdmmc_mount("/sdcard", &host, &slot, &cfg, &card));
sdmmc_card_print_info(stdout, card);
```
Set `format_if_mount_failed` false for user cards, since mount-time auto-formatting erases the volume. Read-only
SPI flash partitions mounted with `esp_vfs_fat_spiflash_mount_ro` cannot be reformatted on the target.

## Build-time image
```cmake
fatfs_create_spiflash_image(storage ${CMAKE_CURRENT_SOURCE_DIR}/fatfs_image FLASH_IN_PROJECT)
```
`idf.py flash` then writes the image with the app.

## Config knobs
- `CONFIG_FATFS_LONG_FILENAMES` choice: `CONFIG_FATFS_LFN_NONE` (8.3 names only), `CONFIG_FATFS_LFN_HEAP` (default) or
  `CONFIG_FATFS_LFN_STACK`; long names use up to 255 characters and extra directory entries.
- `CONFIG_FATFS_VOLUME_COUNT` (default 2), `max_files` (each simultaneously open file costs RAM).
- `CONFIG_FATFS_IMMEDIATE_FSYNC` calls `f_sync` after each write, pwrite, link, truncate and ftruncate (safer, slower).
- `CONFIG_VFS_SUPPORT_DIR` (default y) for `opendir`/`readdir`.

## Pitfalls
- Power loss during a write can corrupt FAT. Keep writes short, close/sync files, and keep
  critical config in NVS instead.
- Close open files before unmounting with the matching helper (`esp_vfs_fat_spiflash_unmount_rw_wl` for the wear-levelled mount).
- Use the full mount prefix in paths (`/spiflash/x`); a path without the registered prefix is not routed to the filesystem.

## Verify
- [ ] `fopen` on a long filename works (LFN enabled, the default) or names are kept 8.3 when `CONFIG_FATFS_LFN_NONE` is chosen.
- [ ] Power-cycle during writes: mount still succeeds; data loss bounded to the last unsynced write.
- [ ] Free space is checked and reported by the application.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-reference/storage/fatfs.rst, wear-levelling README, components/fatfs Kconfig and vfs/esp_vfs_fat.h, vfs Kconfig, esp_driver_sdmmc legacy default-config header, sdmmc_cmd.h).
Confirmed: `esp_vfs_fat_spiflash_mount_rw_wl`, `_unmount_rw_wl`, `esp_vfs_fat_spiflash_mount_ro` (read-only, no wear levelling), `esp_vfs_fat_sdmmc_mount`, `esp_vfs_fat_mount_config_t` fields (format_if_mount_failed, max_files, allocation_unit_size default 0), `SDMMC_HOST_DEFAULT`, `SDMMC_SLOT_CONFIG_DEFAULT`, `SDSPI_HOST_DEFAULT`, `sdmmc_card_print_info`, `fatfs_create_spiflash_image(<partition> <dir> FLASH_IN_PROJECT)`, FATFS LFN choice (default HEAP, so long names work by default), `CONFIG_FATFS_VOLUME_COUNT` default 2, `CONFIG_FATFS_IMMEDIATE_FSYNC` behaviour, `CONFIG_VFS_SUPPORT_DIR` default y. Corrected: long file names are enabled by default (the skill said 8.3 only). Removed unconfirmed claims: SD pull-up resistor values, `esp_vfs_fat_info`, unmounting before OTA or deep sleep, ISR and cache-disabled access and the ENOENT behaviour of a missing leading slash.

Method: documentation only; no commands were run.
