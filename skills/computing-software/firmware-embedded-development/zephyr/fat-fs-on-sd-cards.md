---
id: computing-software.firmware-embedded-development.zephyr.fat-fs-on-sd-cards
name: fat-fs-on-sd-cards
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-fatfs, fs-mount, fatfs-sd-card, ff-volume-strs, file-system-api, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Mount a FAT file system on an SD card in Zephyr: devicetree disk node, CONFIG_FAT_FILESYSTEM_ELM, mount point naming, file API use, and power-loss caveats."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/fs/fs.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/fs/Kconfig.fatfs
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/fs/fat_fs.c
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/sdhc/zephyr,sdhc-spi-slot.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/sd/zephyr,sdmmc-disk.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/subsys/fs/fs_sample/README.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FAT FS on SD cards

## Devicetree (SPI-mode SD)
```dts
&spi1 {
    status = "okay";
    cs-gpios = <&gpio0 4 GPIO_ACTIVE_LOW>;
    sdhc0: sdhc@0 {
        compatible = "zephyr,sdhc-spi-slot";
        reg = <0>;
        spi-max-frequency = <24000000>;
        mmc {
            compatible = "zephyr,sdmmc-disk";
            disk-name = "SD";
            status = "okay";
        };
    };
};
```
The SPI slot binding also offers `pwr-gpios` (card power) and `cd-gpios` (card detect). SoCs with a native SDHC/SDMMC
controller use that controller's compatible instead of the SPI slot; the `zephyr,sdmmc-disk` node then sits under the controller.

## Kconfig
```
CONFIG_DISK_ACCESS=y
CONFIG_SDMMC_SUBSYS=y            # selected by the disk driver in recent releases
CONFIG_FILE_SYSTEM=y
CONFIG_FAT_FILESYSTEM_ELM=y
CONFIG_FS_FATFS_LFN=y            # long file names (needs some RAM)
CONFIG_FS_FATFS_EXFAT=n
```

## Mount and use
```c
#include <zephyr/fs/fs.h>
#include <ff.h>

static FATFS fat;
static struct fs_mount_t mp = {
    .type = FS_FATFS,
    .fs_data = &fat,
    .mnt_point = "/SD:",          /* ELM FAT accepts only fixed names (see below) */
};

int sd_log(const char *line)
{
    int rc = fs_mount(&mp);
    if (rc && rc != -EBUSY) return rc;

    struct fs_file_t f;
    fs_file_t_init(&f);
    rc = fs_open(&f, "/SD:/log.txt", FS_O_CREATE | FS_O_WRITE | FS_O_APPEND);
    if (rc) return rc;
    fs_write(&f, line, strlen(line));
    fs_sync(&f);                   /* flush to card */
    return fs_close(&f);
}
```
Directory listing: `fs_opendir` / `fs_readdir`; free space: `fs_statvfs("/SD:", &st)`.
ELM FAT allows only these mount points: `/RAM:`, `/NAND:`, `/CF:`, `/SD:`, `/SD2:`, `/USB:`, `/USB2:`, `/USB3:`, or a single
digit such as `/0:` (custom names need `CONFIG_FS_FATFS_CUSTOM_MOUNT_POINTS`). The mount point must match the disk name.
`fs_mount()` returns `-EBUSY` if the structure or mount point is already mounted.
Alternatively declare the mount in DT with a `zephyr,fstab` entry (`compatible = "zephyr,fstab,fatfs"`) and `automount`;
FATFS fstab entries need `disk-access` and do not support `read-only` or `no-format` per entry (the build asserts).

## Formatting
Enable `CONFIG_FILE_SYSTEM_MKFS` (which makes `CONFIG_FS_FATFS_MKFS` default on), then
`fs_mkfs(FS_FATFS, (uintptr_t)"SD:", NULL, 0)`; the device id is passed straight to FatFs `f_mkfs()` as the volume path.
**Mount can format the card:** `CONFIG_FS_FATFS_MOUNT_MKFS` defaults to `y`, so if no file system is found `fs_mount()` attempts
to format the volume, destroying its data (the Kconfig help and the fs sample README both warn about this). Disable it
for removable cards that must not be reformatted, and format them elsewhere first.

## Gotchas
- Plan for power loss and card removal during a write: the volume may be left inconsistent. Call `fs_sync`
  after critical writes, keep files closed when idle, and consider LittleFS for critical data on internal flash.
- Card detect and hot removal: unmount before removal; the SPI slot binding offers `cd-gpios`.
- File names are limited to 8.3 unless `CONFIG_FS_FATFS_LFN` is enabled (which increases the working buffer size).

## Verify
- [ ] Card mounts at boot and after re-insertion; logs readable on a PC; an unformatted card behaves as you decided (mount-time format on or off).
- [ ] Power-cut test: worst case is loss of the last unsynced data, not a corrupted volume
      (or the risk is documented).

## Checked

Checked 2026-10-26 against Zephyr main on GitHub (`fs.h`, `subsys/fs/Kconfig.fatfs`, `subsys/fs/fat_fs.c`, the SDHC SPI-slot and
SDMMC disk bindings, and the fs sample README): allowed ELM FAT mount points, `fs_mount()` -EBUSY, `fs_mkfs()` signature and how FATFS
uses the device id, `CONFIG_FS_FATFS_MOUNT_MKFS` default and its destructive format-on-failed-mount behaviour, `CONFIG_FS_FATFS_LFN`,
`CONFIG_FS_FATFS_EXFAT`, `CONFIG_SDMMC_SUBSYS`, fstab FATFS restrictions, and binding properties (`pwr-gpios`, `cd-gpios`, `disk-name`).
Fixed: the skill said mount returns an error on unformatted cards (by default it formats them) and that the mount point is
"/" plus the disk name (only listed names are accepted). Removed the 400 kHz init-clock figure and the claim that paths are
case-insensitive, which these sources do not state.

Method: documentation only; no commands were run.
