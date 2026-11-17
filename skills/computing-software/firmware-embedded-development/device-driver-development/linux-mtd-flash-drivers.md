---
id: computing-software.firmware-embedded-development.device-driver-development.linux-mtd-flash-drivers
name: linux-mtd-flash-drivers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [mtd, linux-driver-subsystem, spi-nor, nand-flash, ubi, mtd-utils, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Work with raw flash in Linux through MTD: SPI-NOR and SPI-NAND in DT, fixed-partitions, mtd-utils (flash_erase, nandwrite), UBI/UBIFS on NAND, and bad block handling."
sources:
  - https://docs.kernel.org/driver-api/mtd/index.html
  - https://docs.kernel.org/driver-api/mtd/spi-nor.html
  - https://docs.kernel.org/filesystems/ubifs.html
  - https://github.com/sigma-star/mtd-utils
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MTD flash drivers

MTD (Memory Technology Devices) exposes raw flash (erase blocks, no FTL) as `/dev/mtdN`. eMMC
and SD cards are block devices, not MTD.

## Device tree
```dts
&qspi {
    flash@0 {
        compatible = "jedec,spi-nor";          /* SFDP/JEDEC ID detection */
        reg = <0>;
        spi-max-frequency = <50000000>;
        spi-rx-bus-width = <4>;
        partitions {
            compatible = "fixed-partitions";
            #address-cells = <1>; #size-cells = <1>;
            partition@0      { label = "u-boot";     reg = <0x000000 0x100000>; read-only; };
            partition@100000 { label = "u-boot-env"; reg = <0x100000 0x010000>; };
            partition@110000 { label = "rootfs";     reg = <0x110000 0xef0000>; };
        };
    };
};
```
SPI-NAND: `compatible = "spi-nand"`. Parallel NAND uses the SoC's NAND controller binding.
Partitions can also come from the command line (`mtdparts=`) when `CONFIG_MTD_CMDLINE_PARTS` is set.

## mtd-utils
```sh
cat /proc/mtd                      # dev, size, erasesize, name
mtdinfo -a
flash_erase /dev/mtd2 0 0          # erase whole partition
flashcp -v image.bin /dev/mtd2     # erase/write only differing blocks (NOR), -v shows progress
nandwrite -p /dev/mtd3 rootfs.ubi  # NAND: skips bad blocks, pads pages
nanddump -f out.bin /dev/mtd3
```
Never `dd` onto NAND: it ignores bad blocks and OOB.

## NAND: use UBI
NAND has bad blocks, bit flips (ECC), read disturb and limited erase cycles. UBI provides wear
levelling and bad block management; UBIFS is the filesystem on top:
```sh
ubiformat /dev/mtd3                       # -e/--erase-counter sets the counter value for all blocks
ubiattach -m 3                            # creates /dev/ubi0
ubimkvol /dev/ubi0 -N rootfs -m           # max size
mount -t ubifs ubi0:rootfs /mnt
```
Images built on the host with `mkfs.ubifs` (`-m` min I/O size, `-e` LEB size, `-c` max LEB count)
plus `ubinize`; take the geometry from `mtdinfo`. For NOR, JFFS2 or UBIFS-on-NOR, or squashfs for read-only.

## Driver-level notes
- New SPI-NOR chips usually work via SFDP; quirks go in `drivers/mtd/spi-nor/<vendor>.c`.
- Write protection: `read-only` partitions and the flash's block protection bits (`flash_lock`; the SPI NOR
  documentation notes that block protection is not covered by SFDP tables).
- ECC strength for NAND must match what the bootloader/ROM uses, or the boot loader can't read
  pages Linux wrote.

## Verify
- [ ] `/proc/mtd` matches the partition plan; flashed content reads back identical (`nanddump`/`cmp`); UBI attaches with sane erase counters.
- [ ] Power-cut test during writes on UBIFS: filesystem mounts cleanly afterwards.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/driver-api/mtd/spi-nor.rst: SFDP-based parameter discovery with compatible "jedec,spi-nor", quirks and block protection not covered by SFDP. Confirmed in jedec,spi-nor.yaml and spi-nand.yaml bindings: compatible strings. Confirmed in partition.yaml: label property. Confirmed in drivers/mtd/Kconfig: MTD_CMDLINE_PARTS. Confirmed in Documentation/filesystems/ubifs.rst: volumes mounted as ubiX:NAME or ubiX_Y. Confirmed in mtd-utils source (git.infradead.org clone on GitHub, sigma-star/mtd-utils): flash_erase count 0 erases to end of device, nandwrite skips bad blocks by default with -p padding and -N to disable skipping, nanddump -f, ubiattach -m, ubimkvol -N and -m, ubiformat -e, mtdinfo -a, mkfs.ubifs -m/-e/-c. flashcp only rewrites blocks that differ and -v is progress output (the old "verify" wording was corrected). Removed: the claim that ubiformat preserves erase counters, and the ECC strength statement about bootloaders was left as general guidance.

Method: documentation only; no commands were run.
