---
id: computing-software.firmware-embedded-development.zephyr.disk-access-and-sdmmc
name: disk-access-and-sdmmc
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [disk-access, disk-access-read, disk-access-ioctl, sdmmc-subsys, sdhc-api, ramdisk, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use Zephyr's disk access layer directly for raw block I/O on SD/eMMC/RAM disks: init, sector read/write, ioctl queries, and the SDHC/SDMMC driver stack underneath."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/storage/disk_access.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/disk.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/disk/zephyr,ram-disk.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/misc/zephyr,flash-disk.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/sdhc/sdhc.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/sdhc/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/disk/Kconfig.sdmmc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk access and SDMMC

## Layers
```
fs_* (FAT) / USB MSC / your code
    disk_access_*  (by disk name: "SD", "RAM", "NAND")
        disk drivers: zephyr,sdmmc-disk, zephyr,mmc-disk, zephyr,ram-disk, flash disk
            sdmmc subsystem (card init, CMD protocol)
                SDHC driver API (controller: native SDHC or SPI slot)
```

## Raw block I/O
```c
#include <zephyr/storage/disk_access.h>

static const char *disk = "SD";

int raw_io(void)
{
    uint32_t count, ssize;
    int rc = disk_access_ioctl(disk, DISK_IOCTL_CTRL_INIT, NULL);   /* disk_access_init() is the legacy call; both are reference counted */
    if (rc) return rc;

    disk_access_ioctl(disk, DISK_IOCTL_GET_SECTOR_COUNT, &count);
    disk_access_ioctl(disk, DISK_IOCTL_GET_SECTOR_SIZE, &ssize);   /* sector size in bytes */

    static uint8_t buf[512] __aligned(4);      /* size to the queried sector size */
    rc = disk_access_read(disk, buf, 0 /*start sector*/, 1 /*count*/);
    if (rc) return rc;
    rc = disk_access_write(disk, buf, 100, 1);
    disk_access_ioctl(disk, DISK_IOCTL_CTRL_SYNC, NULL);           /* flush caches */
    return rc;
}
```
`disk_access_status()` reports `DISK_STATUS_OK`, `DISK_STATUS_UNINIT`, `DISK_STATUS_NOMEDIA` or `DISK_STATUS_WR_PROTECT`.

## RAM disk for tests
```dts
/ {
    ramdisk0 {
        compatible = "zephyr,ram-disk";
        disk-name = "RAM";
        sector-size = <512>;
        sector-count = <128>;
    };
};
```
Useful for testing FAT or USB mass storage without a card.

## Flash disk
`compatible = "zephyr,flash-disk"` exposes a flash partition as a block device. Required properties: `partition`,
`disk-name` and `cache-size` (a statically allocated buffer that should be at least the erase-block size; `sector-size`
defaults to 512). It emulates a block device on flash, so consider wear and power-loss behaviour before using it for
frequently written data.

## SDHC details
- The generic `sdhc.yaml` binding carries `max-bus-freq`, `min-bus-freq`, `power-delay-ms`, `max-current-*` and
  `mmc-hs200-1_8v`; check your controller's binding for bus width and other properties.
- `CONFIG_SDHC_BUFFER_ALIGNMENT` (default 1) is raised by controllers whose DMA needs aligned data buffers; use
  buffers aligned to it.
- Card detect: `cd-gpios` is a property of the SPI SDHC slot binding; other controllers have their own binding.

## Gotchas
- Prefer multi-sector `disk_access_read()`/`disk_access_write()` calls (they take a sector count) over looping single sectors.
- Raw writes bypass any file system; don't mix raw writes with a mounted FS on the same disk.

## Verify
- [ ] Sector size/count queried, not assumed.
- [ ] Throughput test with multi-sector transfers meets the requirement.

## Checked

Checked 2026-10-26 against Zephyr main on GitHub (`disk_access.h`, `drivers/disk.h`, ram-disk, flash-disk and SDHC bindings,
`drivers/sdhc/Kconfig`, `drivers/disk/Kconfig.sdmmc`): `disk_access_*` functions and the note that `disk_access_init()` is the legacy
call (use `DISK_IOCTL_CTRL_INIT`) and is reference counted, `DISK_IOCTL_*` and `DISK_STATUS_*` names, ram-disk properties
(`disk-name`, `sector-size`, `sector-count`), flash-disk properties, `CONFIG_SDHC_BUFFER_ALIGNMENT`, `CONFIG_SDMMC_SUBSYS`, and the
`cd-gpios`, `max-bus-freq` and `mmc-hs200-1_8v` properties. Removed the 400 kHz init-clock figure, the `bus-width` property
name, the "bounced or rejected" buffer remark, the eMMC boot-partition remark and the throughput claim, none of which these
sources state.

Method: documentation only; no commands were run.
