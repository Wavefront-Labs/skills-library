---
id: computing-software.firmware-embedded-development.zephyr.littlefs-file-system
name: littlefs-file-system
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-storage, zephyr-littlefs, fs-mount, fstab, power-loss-resilient, file-system-api, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Mount and use LittleFS in Zephyr on internal or external flash: fstab automount, fs_* API, cache sizing, format-on-corruption behaviour and power-loss testing."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/fs/littlefs.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/fs/fs.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/fs/zephyr,fstab,littlefs.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/fs/Kconfig.littlefs
  - https://github.com/littlefs-project/littlefs/blob/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LittleFS file system

LittleFS is designed for power-loss resilience (copy-on-write guarantees) and dynamic wear leveling on flash, which
makes it a common choice for logs and files on NOR flash.

## Config
```
CONFIG_FLASH=y
CONFIG_FLASH_MAP=y
CONFIG_FILE_SYSTEM=y
CONFIG_FILE_SYSTEM_LITTLEFS=y
```

## Automount via devicetree fstab
```dts
/ {
    fstab {
        compatible = "zephyr,fstab";
        lfs1: lfs1 {
            compatible = "zephyr,fstab,littlefs";
            mount-point = "/lfs";
            partition = <&lfs_partition>;     /* fixed-partitions node, e.g. on SPI NOR */
            automount;
            read-size = <16>;                 /* all of these five are required */
            prog-size = <16>;
            cache-size = <64>;                /* multiple of read/prog size, factor of the block size */
            lookahead-size = <32>;            /* multiple of 8 */
            block-cycles = <512>;             /* non-positive disables wear leveling */
        };
    };
};
```
Or mount manually:
```c
FS_LITTLEFS_DECLARE_DEFAULT_CONFIG(lfs_data);
static struct fs_mount_t lfs_mnt = {
    .type = FS_LITTLEFS, .fs_data = &lfs_data,
    .storage_dev = (void *)PARTITION_ID(lfs_partition),
    .mnt_point = "/lfs",
};
int rc = fs_mount(&lfs_mnt);
```

## Using files
```c
struct fs_file_t f;
fs_file_t_init(&f);                                   /* required before open */
int rc = fs_open(&f, "/lfs/log.txt", FS_O_CREATE | FS_O_APPEND | FS_O_WRITE);
if (rc == 0) {
    fs_write(&f, line, strlen(line));
    fs_sync(&f);                                      /* durable point */
    fs_close(&f);
}
struct fs_statvfs st; fs_statvfs("/lfs", &st);       /* free = st.f_bfree * st.f_frsize */
```
Directory ops: `fs_mkdir`, `fs_opendir`/`fs_readdir`, `fs_unlink`, `fs_rename`. The littlefs README says
POSIX-like operations such as remove and rename are atomic even across power loss, so write a temp file and
rename for an atomic replace.

## Behaviour to know
- If mount finds no valid file system, Zephyr formats the partition unless the mount flag
  `FS_MOUNT_FLAG_NO_FORMAT` (devicetree: `no-format`) is set. Convenient for first boot, dangerous if a driver
  bug makes valid data look invalid. Set NO_FORMAT for data you can't lose and handle the error.
- File updates are not committed until `fs_sync` or `fs_close` is called on the file (littlefs README), so
  unsynced data can be lost on power loss.
- Caches: littlefs needs a read cache, a program cache and one more cache per open file (binding text), so RAM
  grows with open files (`CONFIG_FS_LITTLEFS_NUM_FILES`). Larger caches can improve performance.
- Call `fs_file_t_init()` on an `fs_file_t` before its first `fs_open()`.

## Verify
- [ ] Power-cut test during appends: mount always succeeds, files contain only complete synced records.
- [ ] NO_FORMAT decision documented; mount failure path tested.
- [ ] Free-space telemetry (`fs_statvfs`) and log rotation keep headroom; choose the threshold from your own full-disk tests.

## Checked

Checked 2026-10-26 against `include/zephyr/fs/littlefs.h`, `include/zephyr/fs/fs.h`, the `zephyr,fstab,littlefs` and fstab-common
bindings, `subsys/fs/Kconfig.littlefs` and the littlefs README on main: `FS_LITTLEFS_DECLARE_DEFAULT_CONFIG`, mount flags
(`FS_MOUNT_FLAG_NO_FORMAT`, automount, `no-format`), required fstab properties and their constraints, `fs_file_t_init()` before
first open, `fs_open` flags, `fs_statvfs` fields, `fs_sync`, `fs_mkdir`/`fs_opendir`/`fs_readdir`/`fs_unlink`/`fs_rename`, atomic
rename and sync/close commit semantics from the littlefs README, and `CONFIG_FS_LITTLEFS_NUM_FILES`. `FIXED_PARTITION_ID`
replaced with `PARTITION_ID`. Removed the "20% free" figure and the `-EBUSY` remark, which no source confirms.

Method: documentation only; no commands were run.
