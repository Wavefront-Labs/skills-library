---
id: computing-software.firmware-embedded-development.zephyr.flash-map-partitions
name: flash-map-partitions
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-storage, flash-map, fixed-partitions, flash-area-open, storage-partition, mcuboot-slots, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Lay out Zephyr flash partitions in devicetree (fixed-partitions for MCUboot, slots, storage) and access them with the flash_area API, with alignment rules."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/storage/flash_map/flash_map.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/storage/flash_map.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/mtd/fixed-partitions.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/flash.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flash map partitions

## Define partitions in devicetree
```dts
&flash0 {
    partitions {
        compatible = "fixed-partitions";
        #address-cells = <1>;
        #size-cells = <1>;

        boot_partition: partition@0 {
            label = "mcuboot";
            reg = <0x00000000 0x00010000>;     /* 64 KiB */
            read-only;
        };
        slot0_partition: partition@10000 {
            label = "image-0";
            reg = <0x00010000 0x00070000>;
        };
        slot1_partition: partition@80000 {
            label = "image-1";
            reg = <0x00080000 0x00070000>;
        };
        storage_partition: partition@f0000 {
            label = "storage";
            reg = <0x000f0000 0x00010000>;
        };
    };
};
/ { chosen { zephyr,code-partition = &slot0_partition; }; };
```
- Erase offsets and sizes must respect the device's page layout (see `flash_get_page_info_by_offs()`), so
  partition boundaries should fall on erase-page boundaries; on devices with mixed page sizes check each
  boundary against the page layout.
- `zephyr,code-partition` decides where the app is linked. Without MCUboot, point it at a
  partition that starts at the beginning of flash, or omit it to link at the flash base.
- Board files define a default layout; override it in an overlay with `/delete-node/` on the
  partitions node and a fresh one.

## Access
```c
#include <zephyr/storage/flash_map.h>
const struct flash_area *fa;
int rc = flash_area_open(PARTITION_ID(storage_partition), &fa);
if (rc == 0) {
    flash_area_erase(fa, 0, fa->fa_size);          /* offsets are partition-relative */
    flash_area_write(fa, 0, buf, len);             /* len aligned to write-block-size */
    flash_area_read(fa, 0, out, len);
    flash_area_close(fa);
}
```
Compile-time macros take the devicetree node label: `PARTITION_ID(label)`, `PARTITION_OFFSET(label)`,
`PARTITION_SIZE(label)`, `PARTITION_DEVICE(label)`, `PARTITION_EXISTS(label)`. The `FIXED_PARTITION_*` names
are deprecated aliases (`flash_map.h` marks `FIXED_PARTITION_ID` with `__DEPRECATED_MACRO`). `PARTITION_ID()` also
accepts `zephyr,mapped-partition` nodes.

## Rules
- Write size and offset must be multiples of the device's minimum write block size
  (`flash_get_write_block_size(dev)`); the source buffer can be in RAM or flash without alignment restrictions.
- Erase before rewriting a location on devices with explicit erase.
- External flash partitions work the same with the partitions node under the SPI/QSPI flash node.
- If your SDK or vendor tooling generates its own partition layout, confirm which one is authoritative before editing devicetree.
- MCUboot slot sizes must match between bootloader and app builds.

## Verify
- [ ] `build/zephyr/zephyr.dts` shows non-overlapping partitions aligned to erase pages.
- [ ] App image size (`build/zephyr/zephyr.bin`) fits in slot0 with margin for MCUboot trailer.
- [ ] Erase/write/read round trip on the storage partition doesn't touch neighbouring partitions.

## Checked

Checked 2026-10-26 against Zephyr main on GitHub: `fixed-partitions` binding (`label`, `read-only`, `reg`), the flash_map guide
(partition IDs come from `PARTITION_ID()`, which also accepts `zephyr,mapped-partition`), `struct flash_area` (`fa_dev`, `fa_off`,
`fa_size`), `flash_area_open/erase/write/read/close`, and the `PARTITION_*` macros. Fixed: `FIXED_PARTITION_*` are the deprecated
names in current `flash_map.h`, not the replacement; the buffer-in-RAM restriction is not in the current `flash_write()` documentation.
Removed the STM32 sector sizes, example write-block sizes, the NOR bit-AND remark and the nRF Connect SDK partition-manager note.

Method: documentation only; no commands were run.
